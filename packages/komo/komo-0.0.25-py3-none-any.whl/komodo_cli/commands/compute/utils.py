import json
import os
import subprocess
import sys
import uuid
from collections import defaultdict
from typing import Dict, List, Tuple

import boto3
import click
from loguru import logger

import komodo_cli.printing as printing

# disabling eks for now
SUPPORTED_COMPUTE_SERVICES = ["aws"]  # ["aws", "eks"]
KOMODO_TERRAFORM_STATE_S3_BUCKET_PREFIX = "komodo-terraform-state"
KOMODO_TERRAFORM_LOCK_DYNAMODB_TABLE = "komodo-terraform-state-lock"


def run_cmd(cmd, print_stdout=True) -> Tuple[int, str, str]:
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )

    if print_stdout:
        for line in iter(proc.stdout.readline, ""):
            click.echo(line)

    stdout, stderr = proc.communicate()
    exit_code = proc.returncode

    return exit_code, stdout, stderr


def get_compute_dir() -> str:
    komo_dir = os.environ.get(
        "KOMODO_DIR",
        os.path.join(os.path.expanduser("~"), ".komo"),
    )

    compute_dir = os.path.join(komo_dir, "compute")
    return compute_dir


def get_vars_filepath() -> str:
    return os.path.join(get_compute_dir(), "komodo.tfvars")


def print_clusters():
    cmd = [
        "terraform",
        f"-chdir={get_compute_dir()}",
        "output",
        "-json",
        "|",
        "jq",
    ]
    exit_code, stdout, stderr = run_cmd(" ".join(cmd), print_stdout=False)
    if exit_code != 0:
        logger.error(stderr)
        printing.error("Error listing compute", bold=True)
        sys.exit(1)

    outputs = json.loads(stdout.strip())
    clusters = defaultdict(dict)
    for k, v in outputs.items():
        s = k.split("_")
        cluster_type = s[0]
        var = ""
        if cluster_type == "eks":
            var = "_".join(s[2:])
        elif cluster_type == "awsbatch":
            var = "_".join(s[1:])
        else:
            cluster_type = "info"
            var = "_".join(s)

        clusters[cluster_type][var] = v

    for cluster_type, cluster_values in clusters.items():
        if "id" in cluster_values and cluster_values["id"]["value"] != "":
            click.echo(
                f"{click.style(cluster_type, bold=True)} - {click.style(cluster_values['id']['value'], fg='green', bold=True)}"
            )
            cluster_values.pop("id")

        for k, v in cluster_values.items():
            if not v["value"]:
                continue
            click.echo(f"{click.style(k, fg='yellow')}: {v['value']}")


def dict_to_txt_file(d: Dict, output_path: str):
    with open(output_path, "w") as file:
        for k, v in d.items():
            if isinstance(v, list) or isinstance(v, dict):
                v = json.dumps(v).replace(":", "=")
            elif isinstance(v, bool):
                v = str(v).lower()
            else:
                if not v.startswith('"') and not v.endswith('"'):
                    v = f'"{v}"'

            file.write(f"{k} = {v}\n")


def txt_to_dict(input_path: str) -> Dict:
    output = {}
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip()
                v = v.replace("=", ":")

                if v.startswith("[") and v.endswith("]"):
                    v = json.loads(v)
                if v.startswith("{") and v.endswith("}"):
                    v = json.loads(v)

                output[k] = v
    return output


def get_vars(no_exist_ok=False):
    compute_dir = get_compute_dir()
    vars_path = os.path.join(compute_dir, "komodo.tfvars")

    if not os.path.exists(vars_path):
        if no_exist_ok:
            return {}
        raise FileNotFoundError(f"Variables file not found at {vars_path}")
    else:
        return txt_to_dict(vars_path)


def update_vars(new_vars: Dict):
    compute_dir = get_compute_dir()
    vars_path = os.path.join(compute_dir, "komodo.tfvars")
    dict_to_txt_file(new_vars, vars_path)


def bucket_exists_with_prefix(s3_client, prefix):
    response = s3_client.list_buckets()
    for bucket in response["Buckets"]:
        if bucket["Name"].startswith(prefix):
            return True, bucket["Name"]
    return False, ""


def ensure_terraform_state_resources(aws_profile: str):
    session = boto3.Session(profile_name=aws_profile, region_name="us-east-2")
    s3_client = session.client("s3")
    retval_bucket_name = ""
    retval_dynamodb_table_name = KOMODO_TERRAFORM_LOCK_DYNAMODB_TABLE
    # check if komodo-terraform-state bucket exists, if not create
    komodo_terraform_state_bucket_exists, bucket_name = bucket_exists_with_prefix(
        s3_client=s3_client, prefix=KOMODO_TERRAFORM_STATE_S3_BUCKET_PREFIX
    )
    if komodo_terraform_state_bucket_exists:
        retval_bucket_name = bucket_name
        printing.success(
            f"Terraform state bucket {bucket_name} found.",
            bold=True,
        )
    else:
        printing.warning(
            "Terraform state bucket not found. Creating terraform state bucket."
        )
        unique_suffix = str(uuid.uuid4())
        new_bucket_name = f"{KOMODO_TERRAFORM_STATE_S3_BUCKET_PREFIX}-{unique_suffix}"
        try:
            s3_client.create_bucket(
                Bucket=new_bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "us-east-2"},
            )
            s3_client.put_bucket_versioning(
                Bucket=new_bucket_name,
                VersioningConfiguration={"Status": "Enabled"},
            )
            printing.success(
                f"Terraform state bucket {new_bucket_name} created successfully.",
                bold=True,
            )
        except Exception as e:
            logger.error(e)
            printing.error(
                f"Error creating terraform state bucket.",
                bold=True,
            )
            sys.exit(1)

        retval_bucket_name = new_bucket_name

    dynamodb_client = session.client("dynamodb")
    # check if komodo-terraform-state-lock table exists, if not create
    try:
        dynamodb_client.describe_table(TableName=KOMODO_TERRAFORM_LOCK_DYNAMODB_TABLE)
        printing.success(
            f"Terraform state locking table {KOMODO_TERRAFORM_LOCK_DYNAMODB_TABLE} found.",
            bold=True,
        )
    except Exception as e:
        printing.warning(
            "Terraform state locking table not found. Creating terraform state locking table."
        )
        try:
            dynamodb_client.create_table(
                TableName=KOMODO_TERRAFORM_LOCK_DYNAMODB_TABLE,
                KeySchema=[
                    {"AttributeName": "LockID", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "LockID", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 20,
                    "WriteCapacityUnits": 20,
                },
            )
            printing.success(
                f"Terraform state locking table ${KOMODO_TERRAFORM_LOCK_DYNAMODB_TABLE} created successfully.",
                bold=True,
            )
        except Exception as e:
            logger.error(e)
            printing.error(
                f"Error creating terraform state locking table.",
                bold=True,
            )
            sys.exit(1)

    return retval_bucket_name, retval_dynamodb_table_name

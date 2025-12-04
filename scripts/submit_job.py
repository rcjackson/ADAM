import os
import yaml
import logging
import subprocess
from datetime import datetime

import os
import argparse
import os
import subprocess
import yaml
import logging
from datetime import datetime

def create_job_file(directions, nodes, ip, username, password, south, job_path="./jobs", job_name=None):
    """
    Create a job YAML file for Mobotix job submission.

    Parameters:
        directions (list): List of direction strings.
        nodes (list): List of node names.
        ip (str): Camera IP address.
        username (str): Camera username.
        password (str): Camera password.
        south (str): South parameter value.
        job_path (str): Directory to save the job file.
        job_name (str, optional): Custom job name.

    Returns:
        str: Path to the created job YAML file.
    """
    # Compose the job name
    if job_name:
        name = job_name
    else:
        name = f"sdl-mobo-{datetime.now().strftime('%Y%m%d-%H%M%S') }"
    filename = os.path.join(job_path, name + ".yaml")

    # Compose nodes as a dict with True values
    nodes_dict = {n: True for n in nodes}

    # Compose plugin args
    directions_str = ",".join(directions)
    plugin_args = [
        "--ip", ip,
        "--mode", "direction",
        "-south", str(south),
        "-pt", directions_str,
        "-u", username,
        "-p", password
    ]

    job = {
        "name": name,
        "nodes": nodes_dict,
        "plugins": [
            {
                "name": name,
                "pluginSpec": {
                    "args": plugin_args,
                    "image": "registry.sagecontinuum.org/bhupendraraut/mobotix-scan:0.24.8.16"
                }
            }
        ],
        "scienceRules": [f'schedule({name}): cronjob("{name}", "* * * * *")'],
        "successCriteria": []
    }

    with open(filename, "w") as f:
        yaml.dump(job, f, sort_keys=False)
    logging.info(f"Job file {filename} created successfully.")
    return filename

def parse_nodes(nodes_str):
    """
    Parse a comma-separated string of node names into a list.

    Parameters:
        nodes_str (str): Comma-separated node names.

    Returns:
        list: List of node names.
    """
    return [n.strip() for n in nodes_str.split(",")]

def edit_and_submit_job(job_id, job_file, dry_run=False):
    """
    Edit and submit an existing job using the sesctl CLI.

    Parameters:
        job_id (str): Existing job ID to edit and submit.
        job_file (str): Path to the job YAML file.
        dry_run (bool): If True, perform a dry-run (no actual submission).

    Raises:
        ValueError: If required environment variables are not set.
        subprocess.CalledProcessError: If sesctl CLI commands fail.
    """
    token = os.environ.get('SES_USER_TOKEN')
    host = os.environ.get('SES_HOST')
    if not token or not host:
        raise ValueError("SES_USER_TOKEN or SES_HOST not set in environment")
    logging.info(f"Editing job {job_id} with file {job_file}")
    edit_cmd = [
        "./sesctl-darwin-amd64", "edit", str(job_id),
        "-f", job_file,
        "--token", token, "--server", host
    ]
    if dry_run:
        edit_cmd.append("--dry-run")
    result = subprocess.run(edit_cmd, check=True, capture_output=True, text=True)
    print("[sesctl edit output]")
    print(result.stdout)
    logging.info(f"Job edit response: {result.stdout}")
    logging.info(f"Submitting job {job_id}")
    submit_cmd = [
        "./sesctl-darwin-amd64", "submit", "-j", str(job_id),
        "--token", token, "--server", host
    ]
    if dry_run:
        submit_cmd.append("--dry-run")
    result = subprocess.run(submit_cmd, check=True, capture_output=True, text=True)
    print("[sesctl submit output]")
    print(result.stdout)
    logging.info(f"Job submission response: {result.stdout}")

if __name__ == "__main__":
    """
    Main script for editing and submitting an existing Mobotix job to the Waggle scheduler.

    Usage:
        python submit_job.py --job-id <ID> [--directions <str>] [--nodes <str>] [--ip <str>] [--username <str>] [--south <str>] [--job_path <str>] [--job_name <str>] [--dry-run]

    Arguments:
        --job-id: Existing job ID to edit and submit (required)
        --directions: Comma-separated directions list (default: "NEH,NEB,NEG")
        --nodes: Comma-separated node names (default: "V032")
        --ip: Camera IP (default: "camera-mobotix-thermal")
        --username: Camera username (default: "admin")
        --south: South parameter value (default: "15")
        --job_path: Path to save job file (default: "./jobs")
        --job_name: Custom job name (optional)
        --dry-run: Only edit and submit the job in dry-run mode

    Environment Variables:
        SES_USER_TOKEN: User token for sesctl authentication
        SES_HOST: Server URL for sesctl
        SES_MOBO_PASSWORD: Camera password
    """

    #5346 
    parser = argparse.ArgumentParser(description="Edit and submit an existing Mobotix job to Waggle scheduler")
    parser.add_argument('--job-id', type=str, default="5346", help='Existing job ID to edit and submit')
    parser.add_argument('--directions', type=str, default="NEH,NEB,NEG", help='"NEH", "NEB", "NEG", "EH", "EB", "EG", "SEH", "SEB", "SEG", "SH", "SB", "SG", "SWH", "SWB", "SWG"')
    parser.add_argument('--nodes', type=str, default="V032", help='Comma-separated node names')
    parser.add_argument('--ip', type=str, default="camera-mobotix-thermal", help='Camera IP')
    parser.add_argument('--username', type=str, default="admin", help='Camera username')
    parser.add_argument('--south', type=str, default="15", help='South parameter value')
    parser.add_argument('--job_path', type=str, default="./jobs", help='Path to save job file')
    parser.add_argument('--job_name', type=str, default=None, help='Custom job name (optional)')
    parser.add_argument('--dry-run', action='store_true', help='Only edit and submit the job in dry-run mode')

    args = parser.parse_args()

    directions = [d.strip() for d in args.directions.split(",")]
    nodes = parse_nodes(args.nodes)
    ip = args.ip
    username = args.username
    south = args.south
    job_path = args.job_path
    job_name = args.job_name
    os.makedirs(job_path, exist_ok=True)

    # Read password from environment variable
    password = os.environ.get('SES_MOBO_PASSWORD')
    if not password:
        raise ValueError("SES_MOBO_PASSWORD not set in environment")

    job_file = create_job_file(directions, nodes, ip, username, password, south, job_path=job_path, job_name=job_name)
    edit_and_submit_job(args.job_id, job_file, dry_run=args.dry_run)

# Mobotix Job Edit & Submission with sesctl

A Python script to edit and submit Mobotix camera jobs to the Waggle Edge Scheduler using the `sesctl` CLI. It is designed for dynamic, event-driven job management, such as triggering IR scans based on weather model or radar analysis.

[Mobotix Scanner documentation](https://portal.sagecontinuum.org/apps/app/bhupendraraut/mobotix-scan) for understanding scan types and job submission script.

## Overview

- Dynamically generates a YAML job file for Mobotix IR scanning, with directions and other parameters as arguments.
- Edits and submits an existing job to the scheduler using `sesctl` and a provided job ID.
- All credentials and configuration are handled securely via environment variables.
- Prints sesctl CLI output for transparency and debugging.

## Workflow

1. **Event Detection**: A model or analyzer (e.g., running on HPC) detects a weather event.
2. **Job Preparation**: The script generates a YAML job file with the required scan directions and parameters.
3. **Job Edit & Submission**: The script edits and submits the job using `sesctl`, with all credentials provided via environment variables.
4. **Automation**: The main script can be integrated with event triggers (e.g., `scan_event` variable, environment, or thread) to automate job submission.

## Setting Up `sesctl`

### 1. Download `sesctl`
- Go to the [Waggle Edge Scheduler Releases](https://github.com/waggle-sensor/edge-scheduler/releases/) page.
- Download the appropriate executable for your OS:
  - **macOS**: [sesctl-darwin-amd64](https://github.com/waggle-sensor/edge-scheduler/releases/download/0.27.2/sesctl-darwin-amd64)
  - **Linux**: [sesctl-linux-amd64](https://github.com/waggle-sensor/edge-scheduler/releases/download/0.27.2/sesctl-linux-amd64)
- Place the executable in your project directory (e.g., `code/Python/self-scan/`).
- Make it executable:
  ```sh
  chmod +x sesctl-darwin-amd64  # or sesctl-linux-amd64
  ```

### 2. Set Up Environment Variables
- In your terminal, set the following variables (add to your `.bashrc`, `.zshrc`, or use a `.env` file with `python-dotenv`):
  ```sh
  export SES_HOST=https://es.sagecontinuum.org
  export SES_USER_TOKEN=<<YOUR_VALID_TOKEN>>
  export SES_MOBO_PASSWORD=<<CAMERA_PASSWORD>>
  ```
- You can obtain your SES user token from the Waggle portal or your system administrator.

### 3. Verify sesctl Installation
- Test the CLI:
  ```sh
  ./sesctl-darwin-amd64 --help
  # or
  ./sesctl-linux-amd64 --help
  ```

## Usage

Run the script from the `self-scan` directory:

```sh
python submit_job.py --job-id <EXISTING_JOB_ID> --ip <CAMERA_IP> [--directions <DIRS>] [--nodes <NODES>] [--username <USER>] [--south <VAL>] [--dry-run]
```

- Example:
  ```sh
  python submit_job.py --job-id 5346 --ip 130.202.23.119 --directions NEH,NEB,NEG --dry-run
  ```
- The script will print sesctl output for both edit and submit steps.

## YAML Job File Format

The script generates a job YAML file in the format required by sesctl:

```yaml
name: sdl-mobo-20251204-133930
nodes:
  V032: true
plugins:
  - name: sdl-mobo-20251204-133930
    pluginSpec:
      args:
        - --ip
        - 130.202.23.119
        - --mode
        - direction
        - -south
        - '15'
        - -pt
        - NEH,NEB,NEG
        - -u
        - admin
        - -p
        - wagglesage
      image: registry.sagecontinuum.org/bhupendraraut/mobotix-scan:0.24.8.16
scienceRules:
  - 'schedule(sdl-mobo-20251204-133930): cronjob("sdl-mobo-20251204-133930", "* * * * *")'
successCriteria: []
```

## Troubleshooting
- If you see YAML errors, check that the generated YAML matches the above format.
- If sesctl returns a 400 error, verify your job file and credentials.
- Make sure the job ID exists and is editable.
- Use the `--dry-run` flag to test without actual submission.

## Additional Notes
- The script is designed for integration with automated event triggers.
- All credentials should be handled securely and never hard-coded.
- For advanced usage, see the sesctl documentation and Waggle Edge Scheduler docs.

---

For questions or issues, contact your system administrator or the Waggle support team.

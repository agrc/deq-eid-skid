# DEQ Environmental Incidents Salesforce Palletjack Skid

[![Push Events](https://github.com/agrc/deq-eid-skid/actions/workflows/push.yml/badge.svg)](https://github.com/agrc/skid/actions/workflows/push.yml)
[![Pull Events](https://github.com/agrc/deq-eid-skid/actions/workflows/pull_request.yml/badge.svg)](https://github.com/agrc/skid/actions/workflows/pull_request.yml)

This skid pulls data from the DEQ EID Salesforce instance and loads it into DEQ AGOL hosted feature layers [for use in the interactive map](https://github.com/agrc/deq-enviro/issues/665).

## Development Setup

1. Create new environment for the project and install Python
   - `conda create --name deq-eid-skid python=3.11`
   - `conda activate deq-eid-skid`
1. Install the skid in your conda environment as an editable package for development
   - This will install all the normal and development dependencies (palletjack, supervisor, etc)
   - `cd c:\path\to\repo`
   - `pip install -e .[tests]`
1. Set config variables and secrets
   - `secrets.json` holds passwords, secret keys, etc, and will not (and should not) be tracked in git
   - `config.py` holds all the other configuration variables that can be publicly exposed in git
   - Copy `secrets_template.json` to `secrets.json` and change/add whatever values are needed for your skid
   - Change/add variables in `config.py` as needed

## Running it as a Google Cloud Function

### Run Locally with Functions Framework

`functions-framework` allows you to run your code in a local framework that mirrors the Google Cloud Functions environment. This lets you make sure it's configured to run properly when called through the cloud process. If you keep the framework of this template, this should start running just fine.

1. Navigate to the package folder within `src`:
   - `cd c:\path\to\repo\src\deq_eid`
1. Start the local functions framework server. This will attempt to load the function and prepare it to be run, but doesn't actually call it.
   - `functions-framework --target=main --signature-type=event`
1. Open a bash shell (`git-bash` if you installed git for Windows) and run the pubsub.sh script to call the function itself with an HTTP request via curl:
   - `/c/path/to/repo/pubsub.sh`
   - It has to be a bash shell, I can't figure out how to get cmd.exe to send properly-formatted JSON

The bash shell will return an HTTP response. The other terminal you used to run functions-framework should show anything you sent to stdout/stderr (print() statements, logging to console, etc) for debugging purposes

If you make changes to your code, you need to kill (ctrl-c) and restart functions-framework to load them.

### Setup Cloud Dev/Prod Environments in Google Cloud Platform

Skids run as Cloud Functions triggered by Cloud Scheduler sending a notification to a pub/sub topic on a regular schedule.

Work with the GCP maestros to set up a Google project via terraform. They can use the erap configuration as a starting point. Skids use some or all of the following GCP resources:

- Cloud Functions (executes the python)
- Cloud Storage (writing the data files and log files for mid-term retention)
  - Set a data retention policy on the storage bucket for file rotation (90 days is good for a weekly process)
- Cloud Scheduler (sends a notification to a pub/sub topic)
- Cloud Pub/Sub (creates a topic that links Scheduler and the cloud function)
- Secret Manager
  - A `secrets.json` with the requisite login info
  - A `known_hosts` file (for loading from sftp) or a service account private key file (for loading from Google Sheets)

### Setup GitHub CI Pipeline

Skids use a GitHub action to deploy the function, pub/sub topic, and scheduler action to the GCP project. They use the following GitHub secrets to do this:

- Identity provider
- GCP service account email
- Project ID
- Storage Bucket ID

The cloud functions may need 512 MB or 1 GB of RAM to run successfully. The source dir should point to `src/deq_eid`. A cloud function just runs the specified function in the `main.py` file in the source dir; it doesn't pip install the function itself. It will pip install any dependencies listed in `setup.py`, however.

### Handling Secrets and Configuration Files

Skids use GCP Secrets Manager to make secrets available to the function. They are mounted as local files with a specified mounting directory (`/secrets`). In this mounting scheme, a folder can only hold a single secret, so multiple secrets are handled via nesting folders (ie, `/secrets/app` and `secrets/ftp`). These mount points are specified in the GitHub CI action workflow.

The `secrets.json` folder holds all the login info, etc. A template is available in the repo's root directory. This is read into a dictionary with the `json` package via the `_get_secrets()` function. Other files (`known_hosts`, service account keys) can be handled in a similar manner or just have their path available for direct access.

A separate `config.py` module holds non-secret configuration values. These are accessed by importing the module and accessing them directly.

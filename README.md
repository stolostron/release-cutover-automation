# Release Cutover Automation

A working repository develop automation to generate and initialize a new versioned release of MCE and ACM

## Prerequisites

- Python 3:
  - You can use the install it for your respective operating system [here](https://realpython.com/installing-python/)

- Docker CLI:
  - Install Docker Desktop following for your respective machine from [this link](https://docs.docker.com/engine/install/#desktop)
  - Verify your docker is installed & running with the following commands:
    ```bash
    docker run hello-world
    ```

### Variables
```
source_version=<Previous Y-version of deliverable>
dest_version=<New Y-version of deliverable>
product_prefix=<product release repo prefix> (backplane/release)
osci_release_repo=<github repo of osci> (usually your fork of openshift/release)
pipeline_repo=<github repo of product manifest> eg (stolostron/backplane-pipeline)
source_pipeline_branch=<branch to receive manifest from> (2.X-integration)
GITUB_TOKEN=<github API Token>
```

## Run

```
python3 ./scripts/osci-config-generator.py
```

Then in your fork of the OSCI Release Repo on the created branch run:

```
make jobs
```

The branch should now be ready to be PR'd into the primary branch of the fork
  

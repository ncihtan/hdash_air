# AWS Pipeline for creating the HTAN Dashboard.

## Overview

An AWS pipeline for creating the HTAN Dashboard.  The pipeline connects to Synapse to retrieve HTAN data and metadata, and summarizes this data in a series of static HTML web pages.  These static pages are then deployed to an S3 cloud bucket.

Previous versions of this code used Apache Airflow, but this new code is designed to run natively within AWS and designed to be more cost-effective.

Specifically:

* the code is packaged into a Docker image, and registered via AWS Elastic Container Registry (ECR).
* database is run via AWS RDS.
* the Docker container is run via AWS Elastic Compute / Fargate.
* Fargate is triggered via AWS EventBridge on a specific cron schedule.
* static HTML pages are stored in an S3 bucket.

With this architecture, our cloud bill should be substantially lower than Airflow, as we will only be paying for on-demand Fargate computing.

## Development

To develop ```hdash```, make sure you are running Python 3.6 or above.

Next, it is recommended that you create a virtual environment:

```
cd hdash_air
python -m venv .venv
```

To activate the virtual environment, run:

```
source .venv/bin/activate
```

Then, install all dependencies:

```
pip install -r requirements.txt
```

## Set Environment Variables

The following environment variables are required, whether run locally or within AWS.

```
SYNAPSE_USER          Synapse User Name, must use a Personal Access Token (PAT)
SYNAPSE_PASSWORD      Synapse Password, must use a Personal Access Token (PAT)
HDASH_DB_HOST         Database Host Name 
HDASH_DB_USER         Database User Name
HDASH_DB_PASSWORD     Database Password
HDASH_DB_NAME         Database name, e.g. htan
S3_ACCESS_KEY_ID      S3 Access Key ID
S3_SECRET_ACCESS_KEY  S3 Access key
S3_ENDPOINT_URL       S3 Endpoint URL, e.g. https://us-east-1.linodeobjects.com
S3_BUCKET_NAME        S3 Bucket Name, e.g. htan
S3_WEB_SITE_URL       S3 Static Site, e.g. http://htan-hdash.s3-website-us-east-1.amazonaws.com
SLACK_WEBHOOK_URL     Slack Web Hook URL for Posting to Slack
```

## Developer Tools



## Command Line Tool

The ```hdash.py``` command line tool does not run the full pipelines.  Rather, it
is designed to initialize a project and test certain external dependencies.
It currently supports the following commands:

```
  deploy  Deploy website from database to S3 bucket.
  init    Initialize the database with atlases.
  reset   Reset the database (use with caution).
  slack   Send a mock message to Slack.
  web     Download website from the database to deploy directory.
```

You can run the CLI like so:

```commandline
python3 hdash.py slack
```

## Developer Notes

The Makefile includes a number of useful targets for developing code.

```
make test       run Pytests
make smoke      run "smoke" tests agains external dependencies, e.g. database, synapse, etc.
make format     run black
make flake8     run flake8
make pyright    run pyright --> used to check type annotations
make deploy     copy files to local Airflow Dev Server
make gcp        copy files to Google Cloud Composer for production deployment
```

## Developer Notes:  Python Type Annotations

I am currently using [Pyright](https://github.com/microsoft/pyright) to check for Python type annotations.  The current code base is a mix of code with and without Python type annotations. Ideally, I would like to get increased type coverage in the code.  I am therefore following this [PyRight Getting Started Guide](https://microsoft.github.io/pyright/#/getting-started?id=_4-strict-typing).  It provides a step-by-step plan for incrementally adding types to an existing code base.

## AWS Notes

AWS Elastic Container Registry (ECR) is used to register the hdash Docker image.

AWS Elastic Compute FarGate is used to run the hdash Docker container.

AWS EventBridge is used to schedule hdash runs on a cron-based schedule.

For this to work, you must specify a schedule with:

* subnet:  copy from a manual run of ECS
* security group:  copy from a manual run of ECS
* auto-assign Public IP:  must be set to enabled;  otherwise the task cannot pull images from ECR.

## MIT License

Copyright (c) ncihtan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# hdash_air

Airflow pipeline for creating the HTAN Dashboard.

## Overview

```hdash_air``` is an Apache Airflow pipeline for creating the HTAN Dashboard.  The
pipeline connects to Synapse to retrieve HTAN data and metadata, and summarizes this
data in a series of static HTML web pages.  These static pages are then deployed to
an S3 compatible cloud bucket.

```hdash_air``` requires the following components:

* A working installation of Apache Airflow, e.g. via
[Astro CLI](https://docs.astronomer.io/astro/cli/overview).
* A MySQL database for storing intermediate files.
* An S3 compatible cloud bucket for hosting static web pages.

```hdash_air``` is currently running on [Google Cloud Composer](https://cloud.google.com/composer),
with a managed MySQL database, and a Linode cloud bucket.

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

To run the ```hdash.py``` command line tool, and/or to run the pipeline within Airflow,
you must set the following variables.

```
SYNAPSE_USER          Synapse User Name
SYNAPSE_PASSWORD      Synapse Password
HDASH_DB_HOST         Database Host Name 
HDASH_DB_USER         Database User Name
HDASH_DB_PASSWORD     Database Password
HDASH_DB_NAME         Database name, e.g. htan
S3_ACCESS_KEY_ID      S3 Access Key ID
S3_SECRET_ACCESS_KEY  S3 Access key
S3_ENDPOINT_URL       S3 Endpoint URL, e.g. https://us-east-1.linodeobjects.com
S3_BUCKET_NAME        S3 Bucket Name, e.g. htan
S3_WEB_SITE_URL       S3 Static Site, e.g. http://hdash.website-us-east-1.linodeobjects.com/
SLACK_WEBHOOK_URL     Slack Web Hook URL for Posting to Slack
```

For local development, you will also need:
```
AIRFLOW_DEV_HOME            Directory of local/dev Airflow installation.
HDASH_CLOUD_COMPOSER_DAG    DAG Bucket location for Google Cloud Composer.
                            Must be of the form:  gs://xxxx/dags 
```

Note:  For the command line tool, all variables must be prefixed with:  ```AIRFLOW_VAR_```.
For example:  ```AIRFLOW_VAR_SYNAPSE_USER```.

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
make lint       run pylint
make deploy     copy files to local Airflow Dev Server.
make gcp        copy files to Google Cloud Composer for production deployment.
```

## Local Development

For local development, I have used the Astro CLI.  See:  https://docs.astronomer.io/astro/cli/overview.

Commands to get started:

```
mkdir astro
cd astro
astro init
astro dev start
```

NOTE:  For the installation to work, you must also copy most of the dependencies from
```requirements.txt``` to ```astro/requirements.txt```.

## Production Deployment

For production deployment, I am using [Google Cloud Composer](https://cloud.google.com/composer).

Google provides complete documentation on installing Python dependencies at:  
https://cloud.google.com/composer/docs/composer-2/install-python-dependencies.
This includes a console interface where you can install dependencies one by one;
but it also includes documentation on installing an entire requirements.txt file via the
gcloud command line utility.

I used the following command to install dependencies in the requirements.txt file:

```
gcloud composer environments update [project-name] --location [location] --update-pypi-packages-from-file requirements.txt
```

Note that when you update dependencies, it can take several minutes for Google to
update the environment.  Google also already has a (large) number of Python dependencies
installed (see:  https://cloud.google.com/composer/docs/concepts/versioning/composer-versions),
and the current requirements.txt may conflict with Google's.  If this happens, you will receive an
error and none of your dependencies will be installed.  You will then need to potentially relax
specific version numbers in the requirements.txt file.

Other important notes:

Use ```make gcp``` to transfer code to Google Cloud Composer.

By default, Google Cloud Composer is set to use fairly minimal VMs with minimal memory.
To adjust, go to Environment Details, and click Workflow Configuration: Edit.  
You can then adjust the CPUs, RAM and storage for the scheduler and the workers.
You can also adjust the maximum number of workers.

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

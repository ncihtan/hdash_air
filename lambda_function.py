import sys
import json
import urllib.parse
import boto3
from jinja2 import Environment, PackageLoader, select_autoescape
from h5ad_validate.validator import Validator
import anndata as ad

from hdash.db.db_util import DbConnection
from hdash.db.h5ad_validation import H5adValidation


def store_h5ad_validation(bucket: str, key: str, valid: bool, error_list: list[str]):
    db_connection = DbConnection()
    session = db_connection.session
    h5ad_validation = H5adValidation()
    h5ad_validation.bucket = bucket
    h5ad_validation.key = key
    h5ad_validation.valid = valid
    error_str = ""
    if len(error_list) > 0:
        error_str = "#".join(error_list)
    h5ad_validation.error_list = error_str
    session.add(h5ad_validation)
    session.commit()

def create_web_page(s3):
    db_connection = DbConnection()
    session = db_connection.session
    h5ad_list = session.query(H5adValidation).all()
    print("Got %d h5ad_list.", len(h5ad_list))

    env = get_template_env()
    template = env.get_template("h5ad.html")
    html = template.render(
        h5ad_list=h5ad_list
    )
    print("Uploading results to S3 Bucket")
    s3.put_object(
        Bucket='htan-hdash',
        Key='h5ad.html',
        Body=html.encode('utf-8'),
        ContentType='text/html'
    )
    return html

def get_template_env():
    return Environment(
        loader=PackageLoader("hdash", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    s3 = boto3.client("s3")

    try:
        # Extract bucket and key
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(
            event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
        )
        print(f"Bucket:  {bucket}")
        print(f"Key:  {key}")

        if key.endswith("h5ad"):
            # Download local copy of h5ad file
            local_path = '/tmp/temp.h5ad'
            out_path = '/tmp/out.txt'
            print("Downloading from s3 bucket")
            s3.download_file(bucket, key, local_path)
        
            # Load into anndata
            adata = ad.read_h5ad(local_path)
            
            # Inspect
            print(f"Shape: {adata.shape}")

            # Create HTAN h5ad validator
            validator = Validator(adata, local_path, out_path)
            error_list = validator.error_list
            pass_codes = validator.pass_code
            valid_flag = True
            if 1 in pass_codes:
                valid_flag = False
            print(error_list)
            print(f"Pass codes:  {pass_codes}")
            print(f"Valid:  {valid_flag}")
            store_h5ad_validation(bucket, key, valid_flag, error_list)
            create_web_page(s3)
            return 'Success Python' + sys.version + '!'
    except Exception as e:
        print(e)
        raise e

# Test Event to try things out
# event = {
#     "Records": [
#         {"s3": {"bucket": {"name": "htan-h5ad"}, "object": {"key": "HTAN_h5ad_error_exemplar.h5ad"}}}
#     ]
# }
# print("Executing")
# handler(event, None)
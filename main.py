import os
import boto3
from botocore.exceptions import ClientError

# --- Configuration ---
# Replace with your desired S3 bucket name and region.
# Ensure your AWS credentials are configured (e.g., via environment variables
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, or ~/.aws/credentials).

BUCKET_NAME = os.environ.get("S3_DEMO_BUCKET_NAME", "s3-folder-demo-bucket-123456789")
REGION_NAME = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

def create_s3_client():
    """Creates and returns an S3 client."""
    return boto3.client("s3", region_name=REGION_NAME)

def create_bucket_if_not_exists(s3_client, bucket_name):
    """Creates an S3 bucket if it doesn't already exist."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Bucket '{bucket_name}' does not exist. Creating...")
            if REGION_NAME == 'us-east-1': # us-east-1 doesn't require LocationConstraint
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': REGION_NAME})
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Error checking/creating bucket: {e}")
            raise

def upload_demo_objects(s3_client, bucket_name):
    """Uploads objects with keys designed to simulate folders."""
    print("\n--- Uploading Demo Objects ---")
    objects_to_upload = [
        ("my_folder/document.txt", "This is a document in 'my_folder'."),
        ("my_folder/another_subfolder/image.jpg", "Binary content for an image."),
        ("my_folder/report.pdf", "Content for a PDF report."),
        ("root_level_file.txt", "This file is at the root level."),
        ("another_folder/data.csv", "CSV data.")
    ]

    for key, content in objects_to_upload:
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=content.encode('utf-8'))
        print(f"Uploaded object with key: '{key}'")

def list_objects_flat(s3_client, bucket_name):
    """Lists all objects in the bucket, showing their true flat key structure."""
    print("\n--- Listing All Objects (Flat View) ---")
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            # S3 stores objects with full, flat keys. There are no actual 'folder' objects.
            print(f"  - Object Key: '{obj['Key']}'")
    else:
        print("  No objects found.")

def list_objects_simulated_folders(s3_client, bucket_name, prefix='', delimiter='/'):
    """Lists objects, simulating folder structure using prefix and delimiter."""
    print(f"\n--- Listing Objects (Simulated Folder View - Prefix: '{prefix}', Delimiter: '{delimiter}') ---")
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter=delimiter)

    if 'CommonPrefixes' in response:
        print("  Simulated 'Folders' (Common Prefixes):")
        for common_prefix in response['CommonPrefixes']:
            # CommonPrefixes represent what look like folders. S3 returns key prefixes
            # that end with the delimiter, indicating a 'directory'.
            print(f"    - '{common_prefix['Prefix']}'")

    if 'Contents' in response:
        print("  Objects at this 'level':")
        for obj in response['Contents']:
            # These are the actual objects whose keys do not contain the delimiter
            # after the given prefix.
            print(f"    - '{obj['Key']}'")
    else:
        print("  No objects or common prefixes found at this level.")

def cleanup_bucket(s3_client, bucket_name):
    """Deletes all objects in the bucket and then the bucket itself."""
    print(f"\n--- Cleaning up bucket '{bucket_name}' ---")
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
            s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
            print(f"Deleted {len(objects_to_delete)} objects.")
        else:
            print("No objects to delete.")

        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' deleted successfully.")
    except ClientError as e:
        print(f"Error during cleanup: {e}")

def main():
    s3_client = create_s3_client()

    # 1. Create a bucket for demonstration
    create_bucket_if_not_exists(s3_client, BUCKET_NAME)

    # 2. Upload objects with keys that resemble a folder structure
    upload_demo_objects(s3_client, BUCKET_NAME)

    # 3. Demonstrate the flat nature of S3 keys
    list_objects_flat(s3_client, BUCKET_NAME)

    # 4. Demonstrate how S3 simulates folders using Delimiter and Prefix
    list_objects_simulated_folders(s3_client, BUCKET_NAME, prefix='', delimiter='/')
    list_objects_simulated_folders(s3_client, BUCKET_NAME, prefix='my_folder/', delimiter='/')
    list_objects_simulated_folders(s3_client, BUCKET_NAME, prefix='my_folder/another_subfolder/', delimiter='/')

    # 5. Clean up
    # Uncomment the line below to enable automatic cleanup after the demo.
    # cleanup_bucket(s3_client, BUCKET_NAME)
    print(f"\nDemo complete. If you did not uncomment cleanup, please manually delete bucket '{BUCKET_NAME}'.")

if __name__ == "__main__":
    main()

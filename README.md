# S3 Object Keys Simulate Folders

This example demonstrates how Amazon S3, an object storage service, handles "folders." It shows that S3 stores objects with flat keys, and what appears as a hierarchical folder structure is merely a convention based on key prefixes and delimiters. The script uploads objects with nested-looking keys and then lists them to illustrate both the flat key storage and S3's ability to simulate folders.

## Language

`python`

## How to Run

1. Install boto3: `pip install boto3`
2. Configure AWS credentials (e.g., `export AWS_ACCESS_KEY_ID=YOUR_KEY`, `export AWS_SECRET_ACCESS_KEY=YOUR_SECRET`, `export AWS_DEFAULT_REGION=us-east-1`).
3. Run the script: `python main.py`

## Original Article

This example accompanies the Turkish article: [Amazon S3, Nesne Depolama ve Var Olmayan Klasörler: Derinlemesine Bir Bakış](https://fatihsoysal.com/blog/amazon-s3-nesne-depolama-ve-var-olmayan-klasorler-derinlemesine-bir-bakis/).

## License

MIT — see [LICENSE](LICENSE).

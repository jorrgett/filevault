import os
import boto3
import logging
import time
from datetime import datetime
from botocore.exceptions import ClientError


class S3Helper:

    def __init__(self, app):
        self.app = app
        self.client = self._initialize_s3_client()
        self.base_url = self.app.cloudfront_url
        self.now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _initialize_s3_client(self):
        return boto3.resource(
            's3',
            region_name=self.app.bucket_region,
            aws_access_key_id=self.app.bucket_key_id,
            aws_secret_access_key=self.app.bucket_secret_key
        )

    def list_resources(self):
        try:
            bucket = self.client.Bucket(self.app.bucket_name)
            return [item.key for item in bucket.objects.all()]
        except ClientError as e:
            logging.error(f"Error listing resources: {e}")
            return []

    def upload(self, file, file_path):
        """Upload a file to an S3 bucket"""
        try:
            bucket = self.client.Bucket(self.app.bucket_name)
            bucket.upload_fileobj(file, file_path)

            return f"{self.base_url}{file_path}"
        except ClientError as e:
            logging.error(f"Failed to upload file: {e}")
            return False

    def remove(self, file_path):
        if self._item_exists(file_path):
            try:
                self._delete_object(file_path)
                self._invalidate_cloudfront(self.app.bucket_invalidation_code)
                return True
            except ClientError as e:
                logging.error(f"Failed to remove file: {e}")
                return False
        else:
            logging.info("File does not exist.")
            return False

    def log_file(self, **args):
        log_name = self._generate_log_name(args)
        log_content = self._generate_log_content(args)

        self._upload_log(log_name, log_content)

    def _generate_log_name(self, args):
        if args['operation'] == 'removed':
            filename, _ = os.path.splitext(args['folder'])
            return f"{filename}-{args['operation']}.log"
        else:
            return f"{args['folder']}/{args['key']}-user-{args['user_id']}-app-{self.app.id}-{args['operation']}.log"

    def _generate_log_content(self, args):
        return f"""
        ------------------------------------------------------
        This image has been {args['operation']} by user_id: {args['user_id']}
        from application: {self.app.name} ({self.app.id}) on date: {self.now}
        under IP {args['ip']} in folder {args['folder']}.
        ------------------------------------------------------
        """

    def _upload_log(self, log_name, log_content):
        try:
            obj = self.client.Object(self.app.bucket_name, log_name)
            obj.put(Body=log_content)
        except ClientError as e:
            logging.error(f"Failed to upload log: {e}")

    def _invalidate_cloudfront(self, distribution_id: str):
        cf = boto3.client(
            service_name='cloudfront',
            region_name=self.app.bucket_region,
            aws_access_key_id=self.app.bucket_key_id,
            aws_secret_access_key=self.app.bucket_secret_key
        )
        try:
            cf.create_invalidation(
                DistributionId=distribution_id,
                InvalidationBatch={
                    'Paths': {'Quantity': 1, 'Items': ["/*"]},
                    'CallerReference': str(time.time()).replace(".", "")
                }
            )
        except ClientError as e:
            logging.error(f"Failed to invalidate CloudFront: {e}")

    def _delete_object(self, file_path):
        try:
            self.client.Object(self.app.bucket_name, file_path).delete()
        except ClientError as e:
            raise

    def _item_exists(self, key):
        try:
            self.client.Object(self.app.bucket_name, key).load()
            return True
        except ClientError:
            return False

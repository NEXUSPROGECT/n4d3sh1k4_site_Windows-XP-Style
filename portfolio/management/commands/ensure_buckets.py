import json
import time

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ensure the MinIO/S3 bucket exists and is publicly readable for uploads.'

    def handle(self, *args, **options):
        opts = settings.STORAGES['default']['OPTIONS']
        bucket = opts['bucket_name']

        client = boto3.client(
            's3',
            endpoint_url=opts['endpoint_url'],
            aws_access_key_id=opts['access_key'],
            aws_secret_access_key=opts['secret_key'],
            config=Config(
                s3={'addressing_style': 'path'},
                connect_timeout=10,
                read_timeout=30,
                retries={'max_attempts': 2, 'mode': 'standard'},
            ),
        )

        self._wait_for_server(client, bucket)
        self._create_bucket(client, bucket)
        self._make_public(client, bucket)

        self.stdout.write(self.style.SUCCESS(f'Bucket "{bucket}" is ready (public read).'))

    def _wait_for_server(self, client, bucket):
        self.stdout.write('Waiting for MinIO to accept connections...')
        for attempt in range(30):
            try:
                client.head_bucket(Bucket=bucket)
                return
            except ClientError as exc:
                code = exc.response.get('Error', {}).get('Code', '')
                if code in ('404', 'NoSuchBucket'):
                    return
                time.sleep(2)
            except Exception:
                time.sleep(2)
        raise SystemExit('MinIO did not become reachable in time.')

    def _create_bucket(self, client, bucket):
        try:
            client.create_bucket(Bucket=bucket)
            self.stdout.write(f'Created bucket "{bucket}".')
        except ClientError as exc:
            code = exc.response.get('Error', {}).get('Code', '')
            if code not in ('BucketAlreadyOwnedByYou', 'BucketAlreadyExists'):
                raise

    def _make_public(self, client, bucket):
        policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': [f'arn:aws:s3:::{bucket}/*'],
                }
            ],
        }
        client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))

import io
import os
import boto3
from botocore.config import Config
from django.core.files.storage import Storage


class MinIOStorage(Storage):
    """
    Direct boto3 storage for MinIO.
    Bypasses django-storages internals to guarantee path-style addressing.
    Automatically converts uploaded images to WebP.
    """

    _IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp'}

    def __init__(
        self,
        access_key='minioadmin',
        secret_key='minioadmin',
        bucket_name='portfolio',
        endpoint_url='http://minio:9000',
        custom_domain='',
        secure_urls=False,
        default_acl='public-read',
        file_overwrite=False,
        querystring_auth=False,
        **kwargs,
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.custom_domain = custom_domain
        self.secure_urls = secure_urls
        self.default_acl = default_acl
        self.file_overwrite = file_overwrite
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=Config(
                    s3={'addressing_style': 'path'},
                    connect_timeout=10,
                    read_timeout=30,
                    retries={'max_attempts': 2, 'mode': 'standard'},
                ),
            )
        return self._client

    def _convert_to_webp(self, name, content):
        ext = os.path.splitext(name)[1].lower()
        if ext not in self._IMAGE_EXTS:
            return name, content
        try:
            from PIL import Image
            data = content.read()
            img = Image.open(io.BytesIO(data))
            output = io.BytesIO()
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            img.save(output, 'WEBP', quality=85, method=4)
            output.seek(0)
            name = os.path.splitext(name)[0] + '.webp'
            output.name = os.path.basename(name)
            return name, output
        except Exception:
            try:
                content.seek(0)
            except Exception:
                pass
            return name, content

    def _save(self, name, content):
        name, content = self._convert_to_webp(name, content)
        if not self.file_overwrite:
            name = self.get_available_name(name)
            content_type = 'image/webp' if name.endswith('.webp') else 'application/octet-stream'
        self.client.upload_fileobj(
            content,
            self.bucket_name,
            name,
            ExtraArgs={
                'ACL': self.default_acl,
                'ContentType': content_type
            },
        )
        return name

    def url(self, name):
        if self.custom_domain:
            protocol = 'https' if self.secure_urls else 'http'
            return f'{protocol}://{self.custom_domain}/{name}'
        return f'{self.endpoint_url}/{self.bucket_name}/{name}'

    def exists(self, name):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except Exception:
            return False

    def delete(self, name):
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=name)
        except Exception:
            pass

    def _open(self, name, mode='rb'):
        obj = self.client.get_object(Bucket=self.bucket_name, Key=name)
        return io.BytesIO(obj['Body'].read())

    def size(self, name):
        obj = self.client.head_object(Bucket=self.bucket_name, Key=name)
        return obj['ContentLength']

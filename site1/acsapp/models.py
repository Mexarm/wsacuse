import botocore
import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse


class DocInfo(models.Model):
    """ Represents document information (informacion de acuse)"""
    doc_id = models.CharField(
        max_length=512, unique=True, db_index=True)  # numero de acuse
    doc_info = JSONField()  # document attributes
    creation_date = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=20)


class DocImage(models.Model):
    """ Represents a document image """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    doc_info = models.ForeignKey(
        'DocInfo', on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=20, editable=False)
    uploaded_key = models.CharField(max_length=4096, editable=False)
    creation_date = models.DateTimeField(editable=False)
    source_ip_address = models.GenericIPAddressField(editable=False)
    barcode_data = models.CharField(
        max_length=512, db_index=True, editable=False)  # acuse
    barcode_type = models.CharField(max_length=128, editable=False)
    barcode_rect = JSONField(editable=False)
    barcode_polygon = JSONField(editable=False)

    def __str__(self):
        return f'{self.uuid}:{self.uploaded_key}:{self.barcode_data}'

    def download(self):
        if self.state != 'VALID':
            raise ValueError("can not dawnload because state is not VALID")
        import boto3

        BUCKET_NAME = 'hzd-docs-001'
        dfile = f"/tmp/acuse_{self.barcode_data}.jpg"
        KEY = f'decoded/{self.uuid}.jpg'  # replace with your object key

        s3 = boto3.resource('s3')

        try:
            s3.Bucket(BUCKET_NAME).download_file(KEY, dfile)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        return dfile

    @property
    def download_url(self):
        return reverse('download', args=[self.uuid])

    class Meta:
        verbose_name = 'Acuse'
        verbose_name_plural = 'Acuses'
        ordering = ('-creation_date',)

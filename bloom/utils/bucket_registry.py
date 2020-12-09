from typing import Dict

from django.conf import settings
from google.cloud.storage import Client
from google.cloud.storage import Bucket

_bucket_registry: Dict[str, Bucket] = dict()


def register_gcs_bucket(bucket):
    id = "gs://" + bucket.name
    _bucket_registry[id] = bucket
    return id


client = Client()
gcs_bucket = client.get_bucket(settings.GS_BUCKET_NAME)
ddcu_bucket_identifier = register_gcs_bucket(gcs_bucket)

from google.cloud.storage import Blob
from google.cloud import storage
from typing import List
import uuid
import os

def upload_source_list(paths: List) -> str:
    client = storage.Client()
    bucket = client.get_bucket(os.getenv('CONF_BUCKET'))
    key = f'config_{uuid.uuid4()}.jsonl'
    blob = Blob(key, bucket)
    entries = [f'{{"content": "{path}", "mimeType": "image/jpg"}}' for path in paths]

    blob.upload_from_string('\n'.join(entries))
    return f'gs://{bucket.name}/{key}'

## Example
# source_uri = upload_source_list([
#    'gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/aaa.jpg',
#    'gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/test.png']
# )
#
# print(source_uri)
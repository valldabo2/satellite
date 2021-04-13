from google.cloud.storage import Blob
from google.cloud import storage

client = storage.Client()
bucket = client.get_bucket("cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d")
blob = Blob("config.jsonl", bucket)
cfg = '''{"content": "gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/test.png", "mimeType": "image/png"}
{"content": "gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/aaa.jpg", "mimeType": "image/jpeg"}
'''
blob.upload_from_string(cfg)
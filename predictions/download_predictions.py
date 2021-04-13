from google.cloud import storage
from urllib.parse import urlparse


def download_predictions(results_path: str):
  client = storage.Client()

  parsed_path = urlparse(results_path)

  for blob in client.list_blobs(parsed_path.netloc, prefix=parsed_path.path.lstrip("/")):
    print(blob.download_as_text())

# Example
# download_predictions('gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/batchprediction-untitled_1618298013322_202141372930-2021-04-13T09:19:12.163334Z')
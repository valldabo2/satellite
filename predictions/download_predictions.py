from google.cloud import storage

client = storage.Client()

prefix='batchprediction-untitled_1618298013322_202141372930-2021-04-13T09:19:12.163334Z/'

for blob in client.list_blobs('cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d', prefix=prefix):
  print(blob.download_as_text())
import requests

data = {
    "displayName": "bbb",
    "model": "projects/317101099846/locations/europe-west4/models/1678646392358174720",
    "modelParameters": {
      "confidenceThreshold": 0.0,
      "maxPredictions": 10
    },
    "inputConfig": {
        "instancesFormat": "jsonl",
        "gcsSource": {
            "uris": ["gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/jsonll.jsonl"]
        }
    },
    "outputConfig": {
        "predictionsFormat": "jsonl",
        "gcsDestination": {
            "outputUriPrefix": "gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d"
        }
    }
}

r = requests.post('https://europe-west4-aiplatform.googleapis.com/v1alpha1/projects/317101099846/locations/europe-west4/batchPredictionJobs',
  json=data, headers={
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer <token_here>"
    }
)
print(r.status_code)
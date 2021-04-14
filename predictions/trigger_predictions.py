import requests
import uuid
import os


def build_request(model: str, source_uri: str, output_uri: str):
    return {
        "displayName": f"run_{uuid.uuid4()}",
        "model": model,
        "modelParameters": {
        "confidenceThreshold": 0.0,
        "maxPredictions": 10
        },
        "inputConfig": {
            "instancesFormat": "jsonl",
            "gcsSource": {
                "uris": [source_uri]
            }
        },
        "outputConfig": {
            "predictionsFormat": "jsonl",
            "gcsDestination": {
                "outputUriPrefix": output_uri
            }
        }
    }

def trigger_predictions(source_uri: str) -> str:
    r = requests.post(os.getenv("PREDICTION_ENDPOINT"),
        json=build_request(os.getenv("MODEL"), source_uri, os.getenv("OUTPUT_URI")),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {os.getenv('TOKEN')}"
        }
    )
    return r.json()['name'].rsplit('/', 1)[-1]

## Example
# job_name = trigger_predictions("gs://cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/config_03401a43-925f-4568-8bf0-9b1d25f3c5ef.jsonl")
# print(job_name)

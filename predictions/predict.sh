# trigger batch prediction

curl -X POST \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
-H "Content-Type: application/json; charset=utf-8" \
-d @request.json \
https://europe-west4-aiplatform.googleapis.com/v1alpha1/projects/317101099846/locations/europe-west4/batchPredictionJobs

# polling for JOB_STATE_SUCCEEDED
curl -X GET \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
https://europe-west4-aiplatform.googleapis.com/v1alpha1/projects/317101099846/locations/europe-west4/batchPredictionJobs/7861332216737955840

# get results from GS
curl -X GET \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -o predictions.jsonl \
  "https://storage.googleapis.com/storage/v1/b/cloud-ai-platform-1b863bec-7bcc-4f10-87ca-405bebd38d4d/o/prediction-untitled_1618298013322_202141372930-2021-04-13T08:12:05.134936Z%2Fpredictions_00001.jsonl?alt=media"

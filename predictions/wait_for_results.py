import requests
import polling

def check_if_completed():
    print(f'Check if completed')
    r = requests.get('https://europe-west4-aiplatform.googleapis.com/v1alpha1/projects/317101099846/locations/europe-west4/batchPredictionJobs/691601609964126208', headers={
        "Authorization": "Bearer <token_here>"
        }
    )
    resp = r.json()
    if resp['state'] == 'JOB_STATE_SUCCEEDED':
        return resp
    
    return False
    
try:
    resp = polling.poll(check_if_completed, timeout=1200, step=10)
    results_dir = resp["outputInfo"]["gcsOutputDirectory"]
    print(results_dir)
except polling.TimeoutException as ex: 
    print(ex)
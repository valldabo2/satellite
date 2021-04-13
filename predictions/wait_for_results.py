import requests
import polling
import os 


def check_if_completed(job_name:str):
    def _check():
        print(f'Check if completed {job_name}')
        r = requests.get(f'{os.getenv("PREDICTION_ENDPOINT")}/{job_name}', 
            headers={
                "Authorization": f"Bearer {os.getenv('TOKEN')}"
            }
        )
        resp = r.json()
        if resp['state'] == 'JOB_STATE_SUCCEEDED':
            return resp
        
        return False
    
    return _check

def wait_for_results(job_name:str) -> str:
    try:
        resp = polling.poll(check_if_completed(job_name), timeout=1200, step=10)
        results_dir = resp["outputInfo"]["gcsOutputDirectory"]
        return results_dir
    except polling.TimeoutException as ex: 
        print(ex)
        return None

## Example
# results_dir = wait_for_results('4150366123784667136')
# print(results_dir)

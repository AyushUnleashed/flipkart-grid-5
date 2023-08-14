import requests
import time
def fetch_gpt_response(prompt: str):
    # make post request with gpt api & get output
    message = {'message': prompt}
    url = 'http://localhost:5001/chat'
    try:
        start_time = time.time()
        print('\n Waiting for gpt response')
        response = requests.post(url, json=message)
        end_time = time.time()
        response_time = end_time - start_time
        print("\nresponse time: ",round(response_time,2) ," seconds\n ")
        if (response.status_code != 200):
            print(f"Response failed with status code: {response.status_code}")
            return None
        else:
            result = response.text
            return result
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None
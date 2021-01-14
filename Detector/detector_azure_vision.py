import json
import os


def detect(photo: bytes) -> str:
    result = azure_vision(photo)
    return json.loads(result)['result']     # get text from JSON results


def azure_vision(photo: bytes) -> str:
    """detecting objects on the photo with Azure Computer Vision API"""
    from dotenv import load_dotenv
    import requests

    load_dotenv()   # get Azure credentials
    api_key = os.getenv('COMPUTER_VISION_API_KEY')
    endpoint = os.getenv('COMPUTER_VISION_ENDPOINT')
    try:
        request_url = endpoint + "vision/v3.1/analyze"
        headers = {'Ocp-Apim-Subscription-Key': api_key,
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Description'}
        response = requests.post(request_url, headers=headers, params=params, data=photo)
        response.raise_for_status()
        results = response.json()
        description = results['description']['captions'][0]['text']
        result = 'There is probably ' + description + ' in front of you.'
        return json.dumps({'result': result})   # send results in JSON
    except:
        return json.dumps({'result':  'I could not perform an image analysis.'})


# to test the function uncomment the line below and change 'capture.png' to some image path OR run test_detector.py
# print(detect(open('capture.png', 'rb').read()))

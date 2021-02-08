import json
import os

from dotenv import load_dotenv

# azure credentials should be sent from
# mobile app in the request headers

# ?basic image processing with openCV (too light/dark/blurred)?

load_dotenv()  # get Azure credentials
user_api_key = os.getenv('COMPUTER_VISION_API_KEY')
user_endpoint = os.getenv('COMPUTER_VISION_ENDPOINT')


def detect(photo: bytes) -> str:
    """function like this will be in Flutter app"""
    result = azure_vision(photo, user_endpoint, user_api_key)
    return json.loads(result)['result']     # get text from JSON results


def azure_vision(photo: bytes, endpoint: str, api_key: str) -> str:
    """detecting objects on the photo with Azure Computer Vision API"""
    import requests

    try:
        request_url = endpoint + "vision/v3.1/analyze"
        headers = {'Ocp-Apim-Subscription-Key': api_key,
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Description,Brands,Objects,Faces,Color'}
        response = requests.post(request_url, headers=headers, params=params, data=photo)
        response.raise_for_status()
        results = response.json()
        # print(results)
        description = results['description']['captions'][0]['text']
        result = 'There is probably ' + description + ' in front of you.'
        if results['brands']:
            brand = results['brands'][0]['name']
            result += ' The brand is ' + brand
        return json.dumps({'result': result})   # send results in JSON
    except:
        return json.dumps({'result': 'I could not perform an image analysis.'})


# to test the function uncomment the code below and change image path OR run detector.py

# if __name__ == '__main__':
    # print(detect(open('capture.png', 'rb').read()))

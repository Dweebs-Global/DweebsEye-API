import os
import logging

import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    ObjectDetector Function or dweebs-eye function app;
    gets an image from the request body and
    makes an API call to Azure Computer Vision API,
    namely to Analyze endpoint to get an image description.
    """    
    if req.method == 'POST':
        logging.info('Python HTTP trigger function processed a request.')
        api_key = os.environ['CV_API_KEY1']
        endpoint = os.environ['CV_ENDPOINT']

        if req.headers.get('Content-Type') not in ['image/jpeg', 'image/png']:
            return func.HttpResponse('Not valid or not specified content type in the headers.', status_code=400)
        else:
            img = req.get_body()
            if not img or not isinstance(img, bytes):
                return func.HttpResponse('No valid image provided.', status_code=400)

        req_url = endpoint + "vision/v3.1/analyze"
        headers = {'Ocp-Apim-Subscription-Key': api_key,
                    'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Description,Brands'}

        try:
            response = requests.post(req_url, headers=headers, params=params, data=img)
            response.raise_for_status()
            results = response.json()
            description = results['description']['captions'][0]['text']
            result = 'There is probably ' + description + ' in front of you.'
            if results['brands']:
                brand = results['brands'][0]['name']
                result += ' The brand is ' + brand
            return func.HttpResponse(f'{result}')
        except:
            return func.HttpResponse('Could not perform image analysis.', status_code=400)

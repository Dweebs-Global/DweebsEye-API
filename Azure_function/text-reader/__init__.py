import os
import logging

import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    TextReader Function or dweebs-eye function app;
    gets an image from the request body and
    makes an API call to Azure Computer Vision API,
    namely to OCR endpoint to get text from the image.
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
        
        req_url = endpoint + "vision/v3.1/ocr"
        headers = {'Ocp-Apim-Subscription-Key': api_key,
                    'Content-Type': 'application/octet-stream'}
        params = {'detectOrientation': 'true'}

        try:
            response = requests.post(req_url, headers=headers, params=params, data=img)
            response.raise_for_status()
            results = response.json()
            result = ''
            for region in results['regions']:
                for line in region['lines']:
                    for word in line['words']:
                        result += word['text'] + ' '
            if result:
                if len(result) <= 150:
                    result = 'The extracted text is: ' + result
                else:
                    result = 'The extracted text is too long.'
            else:
                result = 'No readable text found.'
            return func.HttpResponse(f'{result}')
        except:
            return func.HttpResponse('Could not perform image analysis.', status_code=400)

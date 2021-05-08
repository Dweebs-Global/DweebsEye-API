import logging
import os
import time

import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    text_reader function of dweebs-eye function app;
    gets an image from the request body and
    makes an API call to Azure Computer Vision API,
    namely to Read endpoint first and Get Read Result 
    afterwards to get text from the image.
    """
    if req.method == 'POST':
        logging.info('Python HTTP trigger function processed a request.')
        try:
            api_key = os.environ['CV_API_KEY1']
            endpoint = os.environ['CV_ENDPOINT'] 
        except KeyError:
            api_key = ''
            endpoint = ''

        if req.headers.get('Content-Type') not in ['image/jpeg', 'image/png']:
            return func.HttpResponse('Not valid or not specified content type in the headers.', status_code=400)
        else:
            img = req.get_body()
            if not img or not isinstance(img, bytes):
                return func.HttpResponse('No valid image provided.', status_code=400)
        
        # first (POST) request
        post_req_url = endpoint + 'vision/v3.2/read/analyze'
        post_headers = {'Ocp-Apim-Subscription-Key': api_key,
                    'Content-Type': 'application/octet-stream'}
        # post_params = {'readingOrder': 'natural'}

        # second (GET) request
        get_req_url = endpoint + 'vision/v3.2/read/analyzeResults'
        get_headers = {'Ocp-Apim-Subscription-Key': api_key}

        try:
            # send first (POST) request
            post_response = requests.post(post_req_url, headers=post_headers, data=img)
            post_response.raise_for_status()
            post_results = post_response.headers['Operation-Location']
            # extract operation ID with / from the end of returned Operation-Location URL
            operation_id = post_results[post_results.rfind('/'):]
            
            print(post_results, '\n')

            # wait 0.5 second for read operation to complete
            time.sleep(0.7)

            # send second (GET) request
            get_response = requests.get(get_req_url+operation_id, headers=get_headers)
            get_response.raise_for_status()
            get_results = get_response.json()
            # if the operation not complete, try to make a request again
            if get_results['status'] != 'succeeded':
                # wait 0.5 second for read operation to complete
                time.sleep(0.7)
                get_results = get_response.json()
                # if still not complete, return error response
                if get_results['status'] != 'succeeded':
                    result = 'No readable text found.'
                    return func.HttpResponse(result)

            print(get_results, '\n') 

            lines = get_results['analyzeResult']['readResults'][0]['lines']            
            if lines != []:     # check if there is any text
                # calculate first letter height for all lines
                # and create a dict like, <text> : <line height>
                lines_and_heights = dict()
                text_list = list()
                for line in lines:
                    # delete punctuation signs from the text
                    text = line['text'].translate(str.maketrans('', '', '!#()*+/:;<>[\\]^_{|}~®'))
                    box = line['boundingBox']
                    x1 = box[0]
                    x2 = box[6]
                    y1 = box[1]
                    y2 = box[7]
                    line_height = ((((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5)
                    lines_and_heights[text] = line_height
                    # save recognized text in list to keep the order (no duplicates)
                    if text not in text_list:
                        text_list.append(text)
                print(lines_and_heights)
                
                # ignore small text: find the biggest line 
                # if more than 10 lines, only keep text >= 1/3 its size
                # if fewer than 10 lines, keep text >= 1/4 size of the biggest
                max_line_height = max(lines_and_heights.values())
                if len(lines) > 10:
                    for line, height in lines_and_heights.items():
                        if height <= max_line_height / 3:
                            text_list.remove(line)
                else:
                    for line, height in lines_and_heights.items():
                        if height <= max_line_height / 4:
                            text_list.remove(line)
                
                result = 'The extracted text is: '
                # check if the text from the list was not deleted from dict in the previous step
                for text in text_list:
                    result += text + ' '
                # extract only first 160 characters if captured a lot of text
                if len(result) > 150:
                    result = result[0:150]
                return func.HttpResponse(result)
            else:
                result = 'No readable text found.'
                return func.HttpResponse(result) 
        except Exception as e:
            print('Exception occurred:', e)
            return func.HttpResponse('Could not perform image analysis.', status_code=400)

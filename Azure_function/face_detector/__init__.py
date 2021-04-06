import logging
import os

import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    face_detector function of dweebs-eye function app;
    gets an image from the request body and
    makes an API call to Azure Face API,
    namely to Detect endpoint to get facial attributes of people on the photo.
    """
    if req.method == 'POST':    
        logging.info('Python HTTP trigger function processed a request.')
        try:
            api_key = os.environ['FACE_API_KEY1']
            endpoint = os.environ['FACE_ENDPOINT']
        except KeyError:
            api_key = ''
            endpoint = ''
        
        if req.headers.get('Content-Type') not in ['image/jpeg', 'image/png']:
            return func.HttpResponse('Not valid or not specified content type in the headers.', status_code=400)
        else:
            img = req.get_body()
            if not img or not isinstance(img, bytes):
                return func.HttpResponse('No valid image provided.', status_code=400)
        
        req_url = endpoint + "face/v1.0/detect"
        headers = {'Ocp-Apim-Subscription-Key': api_key,
                    'Content-Type': 'application/octet-stream'}
        params = {
            'returnFaceId': 'false',
            'returnFaceAttributes': 'age,gender,glasses,emotion',
            'faceIdTimeToLive': '100'
            }
        
        emotion_dict = {
            'neutral': 'neutral', 
            'anger': 'angry', 
            'contempt': 'contemptuous', 
            'disgust': 'with disgust', 
            'fear': 'scared', 
            'happiness': 'happy', 
            'sadness': 'sad', 
            'surprise': 'surprised'
            }

        try:
            response = requests.post(req_url, headers=headers, params=params, data=img)
            response.raise_for_status()
            results = response.json()
            if not results:
                return func.HttpResponse('No faces detected')
            result = 'There is a '
            for num, face in enumerate(results, start=1):
                gender = face['faceAttributes']['gender']
                age = int(face['faceAttributes']['age'])
                glasses = face['faceAttributes']['glasses']
                emotion = face['faceAttributes']['emotion']
                # adding age info 
                result += str(age) + ' year old'
                # adding gender info
                if gender == 'male':
                    if age > 18:
                        result += ' man'
                    else:
                        result += ' boy'
                else:
                    if age > 18:
                        result += ' woman'
                    else:
                        result += ' girl'
                # adding glasses info if detected any
                if glasses == 'ReadingGlasses':
                    result += ' in glasses'
                elif glasses == 'Sunglasses':
                    result += ' in sunglasses'
                # adding emotion info
                for key, value in emotion.items():
                    if value > 0.5 and key != 'neutral':
                        result += ' looking ' + emotion_dict[key]
                        break
                # checking if there are more people to add
                if len(results) > num:
                    # stop after 3d face (first faces are the biggest(closest)):
                    if num == 3:
                        break
                    result += ' and a '
            # result += ' in front of you.'
            return func.HttpResponse(result)
        except:
            return func.HttpResponse('Could not perform image analysis.', status_code=400)

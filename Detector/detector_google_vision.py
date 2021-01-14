import os


def google_vision(photo: bytes) -> str:
    """detecting objects on the photo with Google Vision API"""
    from google.cloud import vision

    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "detector_vision.json"
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=photo)
        objects = client.object_localization(image=image).localized_object_annotations
        result = ''
        if objects:
            for num, object_ in enumerate(objects):
                if object_.name in ['Glasses', 'Top', 'Outerwear', 'Pants', 'Clothing']:
                    # BUT what if it is necessary to detect (in the shop etc.)?
                    continue
                result += object_.name+' and '
            result = result[:-5]
            return f"There is probably {result} in front of you"
        else:
            return "I could not find anything."
    except Exception:
        return "I could not perform an image analysis."

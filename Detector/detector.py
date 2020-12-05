from bs4 import BeautifulSoup
import cv2
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import numpy
import requests


def listen():
    """getting user's input with the microphone"""
    recognize = sr.Recognizer()
    # using Google Web Speech API because SpeechRecognition
    # has its API key by default; BUT Google may revoke it;
    # there is (apparently) limit of 50 requests per day
    mic = sr.Microphone()
    with mic as source:
        # audio is analyzed for ambient noises,talk after half second
        recognize.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognize.listen(source, phrase_time_limit=2)
        try:
            user_input = recognize.recognize_google(audio)
        except sr.RequestError:
            user_input = None
            speaker("I could not connect to Internet to convert your speech to text.")
        except sr.UnknownValueError:
            user_input = None
            speaker("I could not understand what you said.")

        return user_input


def speaker(text):
    """returning results with the speaker"""
    try:
        gTTS(text=text).save("speaker.mp3")
        playsound("speaker.mp3")
    except Exception:
        print("Could not activate the speaker")


def capture_img():
    """capturing an image with the camera"""
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # make sure back camera is accessed, not front
    check, frame = cap.read()
    cap.release()
    if check:
        return frame
    else:
        speaker("I didn't manage to take a picture")


def save_img(frame):
    """saving the image in the file 'capture.png'"""
    frame.dtype = numpy.uint8
    cv2.imwrite('capture.png', frame)


def search(photo):
    """performing Google reverse image search and returning the name of the captured object"""
    url = "https://images.google.com/searchbyimage/upload"
    file = {'encoded_image': (photo, open(photo, 'rb'))}
    headers = {'User-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 '
                             'Safari/537.17'}
    try:
        # post request with a binary image file
        response = requests.post(url=url, files=file, allow_redirects=False)
        response.raise_for_status()  # raise Exception if request is unsuccessful
        # get the search results page
        photo_url = response.headers["Location"]
        response1 = requests.get(photo_url, headers=headers)
        response1.raise_for_status()  # raise Exception if request is unsuccessful
        all_results = BeautifulSoup(response1.text, "html.parser")
        # fetch the result word(s) from the search line (next to image)
        result = all_results.find("input", {"class": "gLFyf gsfi"})["value"]
        speaker(f"There is probably {result} in front of you.")
    except Exception:
        speaker("I could not perform an image search.")


def main():
    """
    This Object Detector gets user's voice input (code word "object")
    and takes a photo with the device's default camera,
    sends the photo to Google reverse image search
    and returns audio output stating which object is in front of the user.
    """
    speech = listen()   # do we need other languages?
    if speech == "object":
        photo = capture_img()
        if photo is not None:
            save_img(photo)
            search("capture.png")


if __name__ == '__main__':
    main()

import os
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
        audio = recognize.listen(source, phrase_time_limit=3)
        try:
            user_input = recognize.recognize_google(audio)
        except sr.RequestError:
            user_input = None
            speaker("I could not connect to Internet to convert your speech to text.")
        except sr.UnknownValueError:
            user_input = None
            speaker("I could not understand what you said. Let's try again?")
        except Exception:
            user_input = None
            speaker("I could not activate speech recognizer.")
        return user_input


def speaker(text):
    """returning results with the speaker"""
    try:
        gTTS(text=text, lang="en").save(f"{text.split()[0]}.mp3")
        playsound(f"{text.split()[0]}.mp3")
        os.remove(f"{text.split()[0]}.mp3")
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
    cv2.imwrite("capture.png", frame)


def search(photo):
    """performing Google reverse image search and returning the name of the captured object"""
    url = "https://www.google.com/searchbyimage/upload"
    file = {'encoded_image': (photo, open(photo, 'rb'), "multipart/form-data")}
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.88 Safari/537.36'}
    try:
        # post request with a binary image file
        response = requests.post(url=url, files=file, allow_redirects=False)
        response.raise_for_status()  # raise Exception if request is unsuccessful
        # get the search results page
        photo_url = response.headers["Location"]
        response1 = requests.get(photo_url, headers=headers, params={"hl": "EN"})
        response1.raise_for_status()  # raise Exception if request is unsuccessful
        all_results = BeautifulSoup(response1.text, "html.parser")
        # fetch the result word(s) from the search line (next to image)
        result = all_results.find("a", {"class": "fKDtNb"}).text
        if result:
            speaker(f"There is probably {result} in front of you.")
        else:
            speaker("I could not find anything.")
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
    while speech not in ["object", "origin", "audit", "Orchard", "dodgy", "aubergine", "rbg"]:
        speech = listen()
    photo = capture_img()
    if photo is not None:   # making sure it's a new photo, not previous one:
        save_img(photo)
        search("capture.png")


if __name__ == '__main__':
    main()

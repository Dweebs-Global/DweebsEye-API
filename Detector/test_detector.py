import os

import cv2
from gtts import gTTS
import numpy
from playsound import playsound
import speech_recognition as sr

from detector_azure_vision import azure_vision
from detector_google_vision import google_vision
from detector_reverse_search import image_search


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


def main():
    """
    This Object Detector gets user's voice input (code word "object")
    and takes a photo with the device's default camera,
    then detects objects on it with one of the three detection functions
    (using Google Reverse Image Search, Google Vision API or Azure Computer Vision API -
    you should specify it in the last line of this function)
    and returns audio output stating which object is in front of the user.
    """
    speech = listen()
    while speech not in ["object", "origin", "audit", "Orchard", "dodgy", "aubergine", "rbg"]:
        speech = listen()
    photo = capture_img()
    if photo is not None:
        save_img(photo)
        with open('capture.png', 'rb') as file:  # get bytes representation of the image
            photo = file.read()
        print(image_search(photo))


if __name__ == '__main__':
    main()

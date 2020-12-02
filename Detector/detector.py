import cv2
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# check internet connection, access to camera, microphone?


def listen():
    """getting user's input with the microphone"""
    recognize = sr.Recognizer()
    # using Google Web Speech API because SpeechRecognition
    # ships with a default API key for it so it's free
    # BUT Google may revoke API, and
    # there is a limit of 50 requests per day
    mic = sr.Microphone()
    with mic as source:
        # the user should wait 1 second while the audio
        # is analyzed for ambient noises before talking
        recognize.adjust_for_ambient_noise(source)
        audio = recognize.listen(source, phrase_time_limit=2)
        try:
            user_input = recognize.recognize_google(audio)
        except sr.RequestError:
            user_input = None
            # send to the speaker later
            speaker("I could not connect to Internet to convert your speech to text.")
        except sr.UnknownValueError:
            user_input = None
            # send to the speaker later
            speaker("I did not understand what you just said. Could you repeat it please?")

        return user_input


def speaker(text):
    """returning results with the speaker"""
    # for mobile would be best with Kivy?
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


def show_img(frame):
    """displaying the image"""
    cv2.imshow('capture', frame)
    cv2.waitKey(0)
    cv2.destroyWindow('capture')


def save_img(frame):
    """saving the image in the file 'capture.png'"""
    cv2.imwrite('capture.png', frame)


def main():
    """
    This Object Detector gets user's voice input (code word "sense")
    and takes a photo with the device's back camera,
    sends the photo to Google back image search
    and returns audio output stating which object is in front of the user.
    """
    speech = listen()   # do we need other languages?
    if speech is not None:
        print(speech)
        # speaker(speech)
    # word "sense" is not easily recognised; added similar words
    # another option: other word, like "object" or "photo"/"take photo"
    if speech in ["sense", "since", "send"]:
        photo = capture_img()
        if photo is not None:
            show_img(photo)
        else:
            speaker("I didn't manage to take a picture")


if __name__ == '__main__':
    main()

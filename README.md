# DweebsEye API

---
Public REST API for DweebsEye app.

Hosted on Microsoft Azure as a Function App consisting of several functions, some of them relying on Azure Cognitive 
Services to process image data for the app end user.
---
#### Object detection 
Function `object-detector` makes use of [Azure Computer Vision API](https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-1-ga/operations/56f91f2e778daf14a499f21b), 
particularly *Analyze Image* operation. 

Takes an image as an input and returns objects (and brands, if any) detected in the image in a descriptive manner.

**How to use:**

- endpoint: TBA
- request: `POST`
- headers: `{'Content-Type: image/jpeg'}` or `{'Content-Type: image/png'}`
- body: `binary data` (image)
- response: `text/plain; charset=UTF-8`
---
#### Text extraction 
Function `text-reader` makes use of [Azure Computer Vision API](https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-1-ga/operations/56f91f2e778daf14a499f20d), 
particularly *Optical Character Recognition* operation.

Takes an image (binary data) as an input and returns the short text (if any) detected in the image.

**How to use:**

- endpoint: TBA
- request: `POST`
- headers: `{'Content-Type: image/jpeg'}` or `{'Content-Type: image/png'}`
- body: `binary data` (image)
- response: `text/plain; charset=UTF-8`
---
#### Face recognition 
Function `face-recognizer` returns the names of the people familiar to the end user, whose photos were given to the model.

**How to use:**

- endpoint: TBA
- request: `POST`
- headers: `{'Content-Type: image/jpeg'}` or `{'Content-Type: image/png'}`
- body: `binary data` (image)
- response: `text/plain; charset=UTF-8`
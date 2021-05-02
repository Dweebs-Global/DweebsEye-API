# DweebsEye API

***Before working on the code check [Contributing guidelines](https://github.com/Dweebs-Global/DweebsEye-API/blob/main/CONTRIBUTING.md)***


Public REST API for DweebsEye app.

Hosted on Microsoft Azure as a Function App consisting of several functions, some of them relying on Azure Cognitive Services to process image data for the app end user.


### Object detection 
Function `object_detector` makes use of [Azure Computer Vision API](https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-1-ga/operations/56f91f2e778daf14a499f21b), 
particularly *Analyze Image* operation. 

Takes an image as an input and returns objects (and brands, if any) detected in the image in a descriptive manner.

**How to use:**

- request: `POST`
- headers: `{'Content-Type: image/jpeg'}` or `{'Content-Type: image/png'}`
- body: `binary data` (image)
- response: `text/plain; charset=UTF-8`

### Text extraction 
Function `text_reader` makes use of [Azure Computer Vision API](https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-1-ga/operations/56f91f2e778daf14a499f20d), 
particularly of asynchronous Read operation. First, POST request is sent to Read endpoint, then GET request is sent to Get Read Result endpoint.

Takes an image (binary data) as an input and returns the short text (if any) detected in the image.

**How to use:**

- request: `POST`
- headers: `{'Content-Type: image/jpeg'}` or `{'Content-Type: image/png'}`
- body: `binary data` (image)
- response: `text/plain; charset=UTF-8`

### Face detection 
Function `face_detector` makes use of [Azure Face API](https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236), 
particularly *Detect* operation.

Takes an image (binary data) as an input and returns features (age, gender, glasses, emotion) detected in the faces of people on the photo.

**How to use:**

- request: `POST`
- headers: `{'Content-Type: image/jpeg'}` or `{'Content-Type: image/png'}`
- body: `binary data` (image)
- response: `text/plain; charset=UTF-8`
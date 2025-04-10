# -*- coding: UTF-8 -*-
# Import the httplib module for Python 2.x.
# import httplib
# Import the http.client module for Python 3.x.
import http.client
import os
import json

from dotenv import load_dotenv

load_dotenv()


appKey = os.getenv("TRANSCRIBE_APP_KEY")
token = os.getenv("TRANSCRIBE_TOKEN")


def process(audioFile):

    # Specify the service request address.
    url = "http://nls-gateway-ap-southeast-1.aliyuncs.com/stream/v1/asr"

    format = "pcm"

    sampleRate = 16000
    enablePunctuationPrediction = True
    enableInverseTextNormalization = True
    enableVoiceDetection = False

    # Configure the RESTful request parameters.
    request = url + "?appkey=" + appKey
    request = request + "&format=" + format
    request = request + "&sample_rate=" + str(sampleRate)

    if enablePunctuationPrediction:
        request = request + "&enable_punctuation_prediction=" + "true"

    if enableInverseTextNormalization:
        request = request + "&enable_inverse_text_normalization=" + "true"

    if enableVoiceDetection:
        request = request + "&enable_voice_detection=" + "true"

    print("Request: " + request)

    # Read the audio file.
    with open(audioFile, mode="rb") as f:
        audioContent = f.read()

    host = "nls-gateway-ap-southeast-1.aliyuncs.com"

    # Configure the HTTP request header.
    httpHeaders = {
        "X-NLS-Token": token,
        "Content-type": "application/octet-stream",
        "Content-Length": len(audioContent),
    }

    # Use the httplib module for Python 2.x.
    # conn = httplib.HTTPConnection(host)

    # Use the http.client module for Python 3.x.
    conn = http.client.HTTPConnection(host)

    conn.request(method="POST", url=request, body=audioContent, headers=httpHeaders)

    response = conn.getresponse()
    print("Response status and response reason:")
    print(response.status, response.reason)

    body = response.read()
    try:
        print("Recognize response is:")
        body = json.loads(body)
        print(body)

        status = body["status"]
        if status == 20000000:
            result = body["result"]
            print("Recognize result: " + result)
            return result
        else:
            print("Recognizer failed!")

    except ValueError:
        print("The response is not json format string")

    conn.close()

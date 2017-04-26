from __future__ import print_function
import time
from datetime import datetime
import requests
import operator
import numpy as np
import json
import urllib2
from bingtts import Translator


def processRequest( json, data, headers, params ):
    numRetries = 0
    detected = None

    while True:
        response = requests.request( 'post', _url, json = jsonObj, data = data, headers = headers, params = params )
        if response.status_code == 429:
            print("response")
            if numRetries <= _maxNumRetries:
                time.sleep(1)
                numRetries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 200 or response.status_code == 201:
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                detected = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    detected = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    detected = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['message'] ) )
        break
    return detected

def renderResult (detected) :
    objectDetected = detected['description']['captions'][0]['text']
    print(objectDetected)
    translator = Translator('[tts key]')
    output = translator.speak(objectDetected, "en-US", "Female", "riff-16khz-16bit-mono-pcm")
    with open("file.wav", "w") as f:
        f.write(output)
    i = 15
    time.sleep(0.3)


# API parameters
_url = 'https://api.projectoxford.ai/vision/v1.0/analyze'
_key = '[compvision api key]'
_maxNumRetries = 10
params = {'visualFeatures' : 'Color, Categories, Description'}
headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'
jsonObj = None

imageName = 'droneimage.jpg'
with open(imageName, 'rb') as f:
    data = f.read()
detected = processRequest(json, data, headers, params)
if detected is not None:
    renderResult(detected)

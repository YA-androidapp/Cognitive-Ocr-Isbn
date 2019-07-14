#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
#
# $ pip install requests matplotlib pillow

from io import BytesIO
from matplotlib.patches import Polygon
from PIL import Image, ImageDraw
import configparser
import matplotlib.pyplot as plt
import os
import requests
import time


currentdirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentdirectory)
print(os.getcwd())

# 設定ファイル読み込み
inifile = configparser.ConfigParser()
inifile.read(os.path.join(currentdirectory, './setting.ini'), 'UTF-8')

subscription_key = inifile.get('Cognitive', 'key')
vision_base_url = inifile.get('Cognitive', 'endpoint')
text_recognition_url = vision_base_url + '/read/core/asyncBatchAnalyze'


assert subscription_key
assert vision_base_url


###


# image_url = 'https://upload.wikimedia.org/wikipedia/commons/d/dd/Cursive_Writing_on_Notebook_paper.jpg'
# headers = {'Ocp-Apim-Subscription-Key': subscription_key}
# data = {'url': image_url}

# response = requests.post(text_recognition_url, headers=headers, json=data)


headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
image_path = 'DSC_0005.JPG'
data = open(image_path, 'rb').read()

response = requests.post(text_recognition_url, headers=headers, data=data)

response.raise_for_status()

# OCR処理と結果の読み出しの2種類のAPIを呼び出す必要がある

# 読み出し用にURLを保持しておく
operation_url = response.headers['Operation-Location']

analysis = {}
poll = True
while (poll):
    response_final = requests.get(
        response.headers['Operation-Location'], headers=headers)
    analysis = response_final.json()
    # print(analysis)
    time.sleep(1)
    if ('recognitionResults' in analysis):
        poll = False
    if ('status' in analysis and analysis['status'] == 'Failed'):
        poll = False

polygons = []
if ('recognitionResults' in analysis):
    polygons = [(line['boundingBox'], line['text'])
                for line in analysis['recognitionResults'][0]['lines']]

# print(polygons)

image = Image.open(BytesIO(open(image_path, 'rb').read()))
draw = ImageDraw.Draw(image)


isbns = []

for polygon in polygons:
    vertices = [(polygon[0][i], polygon[0][i+1])
                for i in range(0, len(polygon[0]), 2)]
    text = polygon[1]
    text = str(text)
    if text.startswith('978') and len(text) == 13:
        isbns.append(text)
        draw.text((vertices[0][0], vertices[0][1]),text)

image.save('result_'+str(os.path.basename(image_path)))
print(isbns)

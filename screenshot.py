# -*- encoding: utf-8 -*-
from selenium import webdriver
from PIL import Image

def get_element(element,name):
    location = element.location
    size = element.size
    im = Image.open(name)
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom))
    im.save(name)  
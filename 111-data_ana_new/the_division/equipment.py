import pandas as pd
import cv2
import pytesseract as pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open('test_img/未标题-1.png'), lang='chi_sim')
print(text)

# 不行, 要做这个识别很困难

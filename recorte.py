from shared import resize_image, substitute_with_index
import numpy as np
import cv2
from PIL import Image
import pytesseract
import pandas as pd


def ocr(image, tesseract_path):
    
    image = resize_image(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if gray.mean() < 255 // 2:
        gray = cv2.bitwise_not(gray)

    thresholded = cv2.threshold(gray, 50, 200, cv2.THRESH_OTSU)[1]

    thresholded = cv2.copyMakeBorder(thresholded,top =  int(0.05 * thresholded.shape[0]) ,bottom = int(0.05 * thresholded.shape[0]), left = int(0.05 * thresholded.shape[0]), right = int(0.05 * thresholded.shape[0]), borderType = cv2.BORDER_CONSTANT, value = int(thresholded[0][0]))

    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    config = ('-l eng --oem 3 --psm 6')
    data = pd.DataFrame(pytesseract.image_to_data(thresholded, config=config, output_type=pytesseract.Output.DICT))

    lines = data[data['text'] != ''].line_num.unique()
    tabs = data[data['text'] != ''].groupby('line_num').first().reset_index()['left'].values

    min_tab = np.argmin(tabs)
    tabs = (tabs / tabs[min_tab]).round(3).round(2).round(1).round(0).astype(int)
    tabs -= tabs[min_tab]
    tabs = substitute_with_index(tabs)

    txt = ''
    for line, tab in zip(lines, tabs):
        txt += '\t' * tab + ' ' + ' '.join(data[data['line_num'] == line].text.values) + '\n'
    
    return txt




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
    config = ('-l eng --oem 3 --psm 3')
    data = pd.DataFrame(pytesseract.image_to_data(thresholded, config=config, output_type=pytesseract.Output.DICT))
    
    data = data[data.text != '']
    
    final_list = []
    for block in data.block_num.unique():
        block_data = data[data.block_num == block]
        for par in block_data.par_num.unique():
            par_data = block_data[block_data.par_num == par]
            for line in par_data.line_num.unique():
                line_data = par_data[par_data.line_num == line]
                ident = min(line_data.left)
                text = ' '.join(line_data.text) + '\n'
                final_list.append([text, ident])

    lefts = np.array([i[1] for i in final_list])
    min_left = min(lefts)
    tabs = (lefts / min_left).round(3).round(2).round(1).round(0).astype(int)
    tabs -= 1
    tabs = substitute_with_index(tabs)

    txt = ''
    for i in range(len(final_list)):
        txt += tabs[i]*'\t' + final_list[i][0]
    
    return txt




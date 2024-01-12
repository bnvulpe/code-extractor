from shared import resize_image, substitute_with_index
import numpy as np
import cv2
from PIL import Image
import pytesseract
import pandas as pd
import scipy.ndimage as ndimage

def correct_skew(image, delta=1, limit=10):
    def determine_score(arr, angle):
        data = ndimage.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(image, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
            borderMode=cv2.BORDER_REPLICATE)
    return corrected

def ocr(image, tesseract_path):
    image = resize_image(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if gray.mean() < 255 // 2:
        gray = cv2.bitwise_not(gray)

    blur = cv2.GaussianBlur(gray,(5,5),0)
    dst = cv2.threshold(blur,50,200,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    kernel = np.ones((2,2),np.uint8)
    erosion = cv2.erode(dst,kernel,iterations = 2)

    dst = cv2.copyMakeBorder(dst,top =  int(0.1 * dst.shape[0]) ,bottom = int(0.1 * dst.shape[0]), left = int(0.1 * dst.shape[1]), right = int(0.1 * dst.shape[1]), borderType = cv2.BORDER_CONSTANT, value = int(dst[0][0]))

    final = correct_skew(dst)

    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    config = ('-l eng --oem 3 --psm 3')
    data = pd.DataFrame(pytesseract.image_to_data(final, config= config, output_type=pytesseract.Output.DICT))

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
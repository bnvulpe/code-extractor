import numpy as np
import cv2
from PIL import Image

def resize_image(img, target_size = 2000):
    if img.shape[0] < img.shape[1]:
        return cv2.resize(img, (int(target_size * img.shape[1] / img.shape[0]), target_size))
    else:
        return cv2.resize(img, (target_size, int(target_size * img.shape[1] / img.shape[0])))

def substitute_with_index(nums):
    unique_sorted_nums = sorted(set(nums))
    index_mapping = {num: index for index, num in enumerate(unique_sorted_nums)}
    result = [index_mapping[num] for num in nums]
    return result

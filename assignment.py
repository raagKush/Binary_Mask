# -*- coding: utf-8 -*-
"""
@author: kushw
"""
import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

def create_mask(file_path):
    img = cv2.imread(file_path)
    if img is None:
        return None,0
    
    mask = np.all(img>200,axis=2).astype(np.uint8)*255
    mask_path = os.path.splitext(file_path)[0]+"_mask.png"
    
    cv2.imwrite(mask_path,mask)
    
    count_max_pix = np.sum(mask==255)
    
    return mask_path,count_max_pix


folder_path = r"D:\Downloads\Online-test"
count_max_pix_list = []
total_count = 0
futures = []

img_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]

with ThreadPoolExecutor() as executor:
    for img_file in img_files:
        futures.append(executor.submit(create_mask, img_file))
 
    for future in futures:
        result = future.result()
        if result:
            mask_path,count_max_pix = result
            count_max_pix_list.append(count_max_pix)
            print("Mask saved at: ",mask_path)

csv_path = os.path.join(folder_path,'count_max_pix_list.txt' )
with open(csv_path,'w') as file:
    for item in count_max_pix_list:
        file.write(f"{item}\n")
    print("Max pix counts saved at: ",csv_path)
    
    
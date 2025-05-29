import cv2
import os
import numpy as np

dataset_path = "dataset/leapGestRecog"
output_path = "dataset/processed"
if not os.path.exists(output_path):
    os.makedirs(output_path)

gesture_labels = {
    "00": 0, "01": 1, "02": 2, "03": 3, "04": 4,
    "05": 5, "06": 6, "07": 7, "08": 8, "09": 9
}

IMG_SIZE = (64, 64)

data = []
labels = []

for gesture_folder in os.listdir(dataset_path):
    gesture_path = os.path.join(dataset_path, gesture_folder)
    if not os.path.isdir(gesture_path):
        continue
    
    label = gesture_labels[gesture_folder]
    
    for subfolder in os.listdir(gesture_path):
        subfolder_path = os.path.join(gesture_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue
        
        for img_name in os.listdir(subfolder_path):
            img_path = os.path.join(subfolder_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            
            img = cv2.resize(img, IMG_SIZE)
            img = img / 255.0
            
            data.append(img)
            labels.append(label)

data = np.array(data)
labels = np.array(labels)

data = data.reshape(-1, IMG_SIZE[0], IMG_SIZE[1], 1)

np.save(os.path.join(output_path, "data.npy"), data)
np.save(os.path.join(output_path, "labels.npy"), labels)

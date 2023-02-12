import os
import cv2
import json
import numpy as np
import shutil

source_folder = os.path.join(os.getcwd(), "./via-2.0.12/images")
json_path = "D:/Depot/2022_PAPER/via-2.0.12/via_project_17Oct2022_17h33m_json (1).json"  # Relative to root directory
count = 0  # Count of total images saved
file_bbs = {}  # Dictionary containing polygon coordinates for mask
MASK_WIDTH = 870  # Dimensions should match those of ground truth image
MASK_HEIGHT = 1348
data = {}
# Read JSON file
with open(json_path) as f:
    data = json.load(f)


# Extract X and Y coordinates if available and update dictionary
def add_to_dict(data, itr, key, count):
    try:
        x_points = data[itr]["regions"][count]["shape_attributes"]["all_points_x"]
        y_points = data[itr]["regions"][count]["shape_attributes"]["all_points_y"]
    except:
        print("No BB. Skipping", key)
        return

    all_points = []
    for i, x in enumerate(x_points):
        all_points.append([x, y_points[i]])
    file_bbs[key] = all_points


for itr in data:
    file_name_json = data[itr]["filename"]
    sub_count = 0  # Contains count of masks for a single ground truth image
    index = 0

    if len(data[itr]["regions"]) > 1:
        for _ in range(len(data[itr]["regions"])):
            try:

                if data[itr]["regions"][_]['region_attributes']['label'] == 'building':
                    index = 1
                elif data[itr]["regions"][_]['region_attributes']['label'] == 'sky':
                    index = 2
                elif data[itr]["regions"][_]['region_attributes']['label'] == 'mount':
                    index = 3

                key = file_name_json[:-4] + "*" + str(index)
                add_to_dict(data, itr, key, sub_count)
                sub_count += 1
            except:
                print("No BB. Skipping", key)
                continue

print("\nDict size: ", len(file_bbs))

for file_name in os.listdir(source_folder):
    to_save_folder = os.path.join(source_folder, file_name[:-4])
    image_folder = os.path.join(to_save_folder, "images")
    mask_folder = os.path.join(to_save_folder, "masks")
    curr_img = os.path.join(source_folder, file_name)

    # make folders and copy image to new location
    os.mkdir(to_save_folder)
    os.mkdir(image_folder)
    os.mkdir(mask_folder)
    os.rename(curr_img, os.path.join(image_folder, file_name))

# For each entry in dictionary, generate mask and save in correponding
# folder
for itr in file_bbs:
    num_masks = itr.split("*")
    to_save_folder = os.path.join(source_folder, num_masks[0])
    mask_folder = os.path.join(to_save_folder, "masks")
    image_folder = os.path.join(to_save_folder, "images")

    if len(num_masks) > 1:
        originName = itr.replace("*", "_").split("_")[0]
        originPath = os.path.join(image_folder, originName + ".png")
        img = cv2.imread(originPath, cv2.IMREAD_COLOR)
        print('img.shape ', img.shape)
        h, w, c = img.shape
        mask = np.ones((h, w)) * 255

    try:
        arr = np.array(file_bbs[itr])
    except:
        print("Not found:", itr)
        continue
    count += 1
    cv2.fillPoly(mask, [arr], color=(0))

    if len(num_masks) > 1:
        cv2.imwrite(os.path.join(mask_folder, itr.replace("*", "_") + ".png"), mask)
        originName = itr.replace("*", "_").split("_")[0]
        path = os.path.join(image_folder, itr.replace("*", "_") + ".png")
        originPath = os.path.join(image_folder, originName + ".png")
        shutil.copyfile(originPath, path)

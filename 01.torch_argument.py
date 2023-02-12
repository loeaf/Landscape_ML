import torchvision.transforms.functional as TF
import random
import os
import numpy as np
from PIL import Image
import cv2
from matplotlib import pyplot as plt

root_image = "D:/Depot/2022_PAPER/via-2.0.12/images"
#fileNames = ['map-00b1dbdd-ea15-4d46-bcb0-7dc3abae0cb5.png']
file_names = []


class UNetDataArgumentation:
    def __init__(self, rootImage, fileNames):
        self.rootImage = rootImage
        self.fileNames = fileNames
        self.imageRoot = '/images/'
        self.labelRoot = '/masks/'

    '''
    파일종류 : image / masks
    기본 경로 : D:\Depot\2022_PAPER\via-2.0.12\images\파일명\파일종류\파일명_label_[j]_rot_[angle].png 를 따름
    기본 경로 : D:\Depot\2022_PAPER\via-2.0.12\images\파일명\파일종류\파일명_label_shift_[j]_rot_[angle].png 를 따름
    '''
    def argumentFlip(self):
        print("argumentFlip")
        for i in range(0, len(file_names)):
            originFileName = file_names[i].split('.')[0]
            print(f"originFileName : {originFileName}")
            # self.rotation(i, originFileName)
            self.hflip(i, originFileName)
        print("argumentFlip end")
    def argumentRot(self):
        print("argumentRot")
        for i in range(0, len(file_names)):
            originFileName = file_names[i].split('.')[0]
            self.rotation(i, originFileName)
        print("argumentRot end")
    def argumentFlipRot(self):
        print("argumentShiftRot")
        for i in range(0, len(file_names)):
            originFileName = file_names[i].split('.')[0]
            self.flip_rotation(i, originFileName)
        print("argumentShiftRot end")


    def hflip(self, i, originFileName):
        size = os.listdir(f"{self.rootImage}/{originFileName}/{self.imageRoot}")
        # 라벨 파일 회전
        for j in range(1, len(size) + 1):
            try:
                image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}",
                                               f"{originFileName}_{j}.png")
                image = Image.open(image_path).convert("RGB")
                image = TF.hflip(image)
                save_image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}",
                                               f"{originFileName}_{j}_flip.png")
                image.save(save_image_path)

                label_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.labelRoot}",
                                          f"{originFileName}_{j}.png")
                segmentation = Image.open(label_path)
                segmentation = TF.hflip(segmentation)
                full_path = f"{self.rootImage}/{originFileName}/{self.labelRoot}/{originFileName}_{j}_flip.png"
                print(f"full_path : {full_path}")
                segmentation.save(full_path)
            except:
                print("No segmentation")

    def rotation(self, i, originFileName):
        size = os.listdir(f"{self.rootImage}/{originFileName}/{self.imageRoot}")
        # 라벨 파일 회전
        for j in range(1, len(size) + 1):
            for angle in range(-30, 30):
                # 원본 파일 회전
                image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}", f"{originFileName}_{j}.png")
                image = Image.open(image_path).convert("RGB")
                image = TF.rotate(image, angle)
                print(f"{self.rootImage}/{originFileName}/{self.imageRoot}",
                      f"{originFileName}_rot_{angle}.png")
                save_image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}",
                                               f"{originFileName}_{j}_rot_{angle}.png")
                image.save(save_image_path)

                label_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.labelRoot}", f"{originFileName}_{j}.png")
                segmentation = Image.open(label_path)
                segmentation = TF.rotate(segmentation, angle)
                print(f"{self.rootImage}/{originFileName}/{self.labelRoot}",
                      f"{originFileName}_{j}_rot_{angle}.png")
                segmentation.save(f"{self.rootImage}/{originFileName}/{self.labelRoot}/{originFileName}_{j}_rot_{angle}.png")

    def flip_rotation(self, i, originFileName):
        size = os.listdir(f"{self.rootImage}/{originFileName}/{self.imageRoot}")
        notsize = size.filter(lambda x: not x.contains('flip') or not x.contains('rot'))
        print(f"notsize : {size + 1 - notsize}")
        for j in range(1, size + 1 - notsize):
            for angle in range(-30, 30):
                # 원본 파일 회전
                image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}", originFileName + f"_{j}_flip.png")
                image = Image.open(image_path).convert("RGB")
                image = TF.rotate(image, angle)
                print(f"{self.rootImage}/{originFileName}/{self.imageRoot}",
                                               f"{originFileName}_{j}_flip_rot_{angle}.png")
                save_image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}",
                                               f"{originFileName}_{j}_flip_rot_{angle}.png")
                image.save(save_image_path)
                # 라벨 파일 회전
                label_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.labelRoot}",
                                          f"{originFileName}_{j}.png")
                segmentation = Image.open(label_path)
                segmentation = TF.rotate(segmentation, angle)
                print(f"{self.rootImage}/{originFileName}/{self.labelRoot}",
                                  f"{originFileName}_{j}_flip_rot_{angle}.png")
                segmentation.save(f"{self.rootImage}/{originFileName}/{self.labelRoot}/{originFileName}_{j}_flip_rot_{angle}.png")

    def deleteOriginFile(self):
        for i in range(0, len(file_names)):
            originFileName = file_names[i].split('.')[0]
            image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}", file_names[i])
            os.remove(image_path)
    def resizeImageByPath(self):
        for i in range(0, len(file_names)):
            originFileName = file_names[i].split('.')[0]
            size = os.listdir(f"{self.rootImage}/{originFileName}/{self.imageRoot}")
            # 라벨 파일 회전
            for j in range(1, 4):
                try :
                    print(f"j : {j}")
                    print(f"size : {size}")
                    image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.imageRoot}",
                                                   f"{originFileName}_{j}.png")
                    image = Image.open(image_path).convert("RGB")
                    image = TF.resize(image, (128, 128))
                    image.save(image_path)
                    image_path = os.path.join(f"{self.rootImage}/{originFileName}/{self.labelRoot}",
                                                   f"{originFileName}_{j}.png")
                    image = Image.open(image_path).convert("RGB")
                    image = TF.resize(image, (128, 128))
                    image.save(image_path)
                except:
                    print("No segmentation")
    def imageHisto(self, path):
        img = cv2.imread(path, 0)
        plt.hist(img.ravel(), 256, [0, 256])
        plt.xlabel('Intensity Value')
        plt.ylabel('value')
        plt.savefig("./histogram3.png", dpi=300)
        # plt.show()


# 해당 폴더에서 폴더 목록을 가져옴
def getFolderList(root):
    folderList = []
    for folder in os.listdir(root):
        folderList.append(folder+'.png')
    return folderList

file_names = getFolderList(root_image)

dataArguments = UNetDataArgumentation(root_image, file_names)
# 원본 파일 제거
dataArguments.deleteOriginFile()
# 이미지 파일 리사이즈
dataArguments.resizeImageByPath()
# 플립
dataArguments.argumentFlip()
# 회전
# dataArguments.argumentRot()
# 플립회전
# dataArguments.argumentFlipRot()

# dataArguments.imageHisto("D:/Depot/2022_PAPER/via-2.0.12/histo/image01.png")
# dataArguments.imageHisto("D:/Depot/2022_PAPER/via-2.0.12/histo/image02.png")
# dataArguments.imageHisto("D:/Depot/2022_PAPER/via-2.0.12/histo/image03.png")
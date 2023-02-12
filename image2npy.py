import os
import cv2
import json
import numpy as np
import shutil

root_image = "D:/Depot/2022_PAPER/via-2.0.12/images"
class Image2Npy:
    def __init__(self, rootImage, fileNames):
        self.rootImage = rootImage
        self.fileNames = fileNames
        self.imageRoot = '/images/'
        self.labelRoot = '/masks/'
        self.imageLen = 0
        self.labelLen = 0
    def getImageRootPathImage(self):
        folderList = []
        for i in range(0, len(self.fileNames)):
            fileName = self.fileNames[i].split('.')[0]
            imagePath = f"{root_image}/{fileName}/{self.imageRoot}/"
            for folder in os.listdir(imagePath):
                folderList.append(f"{imagePath}/{folder}")
        self.imageLen = len(folderList)
        return folderList
    def getLabelRootPathImage(self):
        folderList = []
        for i in range(0, len(self.fileNames)):
            fileName = self.fileNames[i].split('.')[0]
            imagePath = f"{root_image}/{fileName}/{self.labelRoot}/"
            for folder in os.listdir(imagePath):
                folderList.append(f"{imagePath}/{folder}")
        self.labelLen = len(folderList)
        return folderList
    def createNpy(self):
        data = []
        imageArr = sorted(self.getImageRootPathImage())
        labelArr = sorted(self.getLabelRootPathImage())
        print(f"imageLen : {self.imageLen}")
        print(f"labelLen : {self.labelLen}")
        print(f"sum : {self.imageLen + self.labelLen}")
        for i in range(0, len(imageArr)):
            if imageArr[i].find('_3') != -1:
                data = np.array(cv2.imread(imageArr[i]))
                np.save(f"D://Depot/2022_PAPER/datasets/image/input_{i}.npy", data)
                print(f"imageArr : {imageArr[i]}")
        for i in range(0, len(labelArr)):
            if imageArr[i].find('_3') != -1:
                data = np.array(cv2.imread(labelArr[i]))
                np.save(f"D://Depot/2022_PAPER/datasets/label/label_{i}.npy", data)
                print(f"labelArr : {labelArr[i]}")
        print("createNpy Done")

def getFolderList(root):
    folderList = []
    for folder in os.listdir(root):
        folderList.append(folder+'.png')
    return folderList

imageNp = Image2Npy(root_image, getFolderList(root_image))
imageNp.createNpy()

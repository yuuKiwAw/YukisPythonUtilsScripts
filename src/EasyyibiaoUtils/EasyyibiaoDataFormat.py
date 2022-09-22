# coding:utf-8
# author:yuki
#!/usr/bin/python3.8.5

"""
用于处理百度第三方标注工具数据格式转换
https://github.com/Baidu-AIP/Easyyibiao

# 支持的数据转换
- EasyData(json通用格式)
- YOLO
"""

import os
import json
import shutil


class EasyyiBiaoFormat():
    def __init__(self, sourcePath: str, savePath: str) -> None:
        self.sourcePath = sourcePath
        self.savePath = savePath

    def __getFiles(self):
        file_list = os.listdir(self.sourcePath)
        return file_list

    def __getFiles(self, fileType: str):
        outFile_list = []
        file_list = os.listdir(self.sourcePath)
        for item in file_list:
            fileName = item.split(".")
            if len(fileName) >= 1:
                if fileName[1] == fileType:
                    outFile_list.append(item)
        return outFile_list

    def __formatDataGeneral(self, filePath: str):
        formatedList = []
        outPutData = {}

        with open(filePath, 'r', encoding='utf-8') as f:
            sourceData = f.read()
            shapeList = json.loads(sourceData)["shapes"]

            for item in shapeList:
                label = item["label"]
                points = item["points"]

                formatedItem = {}
                formatedItem["name"] = label
                formatedItem["y1"] = int(points[0][1])
                formatedItem["x1"] = int(points[0][0])
                formatedItem["y2"] = int(points[1][1])
                formatedItem["x2"] = int(points[1][0])

                formatedList.append(formatedItem)

            outPutData["labels"] = formatedList

            return outPutData

    def __formatData_yolo(self, filePath: str, labelList: list, imgSize: list):
        formatedText = ''
        outPutData = []

        dw = 1./(imgSize[0])
        dh = 1./(imgSize[1])

        with open(filePath, 'r', encoding='utf-8') as f:
            sourceData = f.read()
            shapeList = json.loads(sourceData)["shapes"]

            for item in shapeList:
                label = item["label"]
                points = item["points"]

                label_index = labelList.index(label)
                y1 = int(points[0][1])
                x1 = int(points[0][0])
                y2 = int(points[1][1])
                x2 = int(points[1][0])

                x = (points[0][0] + points[1][0]) / 2.0
                y = (points[0][1] + points[1][1]) / 2.0
                w = points[1][0] - points[0][0]
                h = points[1][1] - points[0][1]

                x = x*dw
                w = w*dw
                y = y*dh
                h = h*dh

                formatedText = str(label_index) + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n"
                outPutData.append(formatedText)
        return outPutData

    def __collectYOLO_labels(self, filePath: str, labelList: list):
        with open(filePath, 'r', encoding='utf-8') as f:
            sourceData = f.read()
            shapeList = json.loads(sourceData)["shapes"]
            for item in shapeList:
                label = item["label"]

                if label not in labelList:
                    labelList.append(label)
        return labelList


    def ChangeDataFormat(self):
        """百度EasyData - json(平台通用)
        """
        fileLists = self.__getFiles("json")

        count = 0
        allCounts = len(fileLists)
        for fileName in fileLists:
            imgFile = fileName.split(".")[0] + ".jpg"
            shutil.copyfile(self.sourcePath + "\\" + imgFile,
                            self.savePath + "\\" + imgFile)

            filePath = self.sourcePath + "\\" + fileName
            annotatedData = self.__formatDataGeneral(filePath)
            with open(self.savePath + "\\" + fileName, 'w', encoding='utf-8') as f:
                f.write(json.dumps(annotatedData, ensure_ascii=False))
            count += 1
            print(str(count) + "/" + str(allCounts))
        return "All Done!!!"

    def ChangeDataFormatYolo(self, img_size: list):
        """YOLO 数据格式

        Args:
            img_size (list): _description_
        """
        label_List = []
        fileLists = self.__getFiles("json")
        for fileName in fileLists:
            filePath = self.sourcePath + "\\" + fileName
            self.__collectYOLO_labels(filePath, label_List)
        print(label_List)

        # 写入YOLO标签名
        with open(self.savePath+ "\\classes.txt", 'wb') as f:
            for labels in label_List:
                f.write(bytes(labels+'\n', encoding='utf-8'))

        # 写入YOLO标注坐标
        count = 0
        allCounts = len(fileLists)
        for fileName in fileLists:
            filePath = self.sourcePath + "\\" + fileName
            yolodata_list = self.__formatData_yolo(filePath, label_List, img_size)

            with open(self.savePath + "\\" + fileName.split(".")[0] + ".txt", 'wb') as f:
                for yolodata in yolodata_list:
                    f.write(bytes(yolodata, encoding='utf-8'))
            count += 1
            print(str(count) + "/" + str(allCounts))
        return "All Done!!!"


def main():
    sourcePath = r"E:\AI\PN-AI\sliced\苯酚2#灌島\mark"
    savePath = r"E:\AI\PN-AI\sliced\苯酚2#灌島\mark2"

    easyyibiaoFormat = EasyyiBiaoFormat(sourcePath, savePath)
    # easyyibiaoFormat.ChangeDataFormat()
    easyyibiaoFormat.ChangeDataFormatYolo([1920, 1080])


if __name__ == '__main__':
    main()

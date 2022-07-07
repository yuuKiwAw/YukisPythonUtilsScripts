import os
import json
import shutil


def getFiles(folderPath: str):
    """_summary_
    Gets files in the folder

    Args:
        folderPath (str): folder path
    Returns:
        _type_: list[str] (file name)
    """
    file_list=os.listdir(folderPath)
    return file_list


def getFiles(folderPath: str, fileType: str):
    """_summary_
    Gets files of the specified type in the folder

    Args:
        folderPath (str): folder path
        fileType (str): file type

    Returns:
        _type_: list[str] (file name)
    """
    outFile_list = []
    file_list=os.listdir(folderPath)
    for item in file_list:
        fileName = item.split(".")
        if len(fileName) >= 1:
            if fileName[1] == fileType:
                outFile_list.append(item)
    return outFile_list


def formatData(sourcePath: str):
    """_summary_
    Format json data

    Args:
        sourcePath (str): source path

    Returns:
        _type_: dict
    """
    formatedList = []
    outPutData = {}

    with open (sourcePath, 'r', encoding='utf-8') as f:
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


def ChangeDataFormat(sourceFolder, saveFolder):
    """_summary_
    Change JSON Data Format
    Easyyibiao To Common Json Annotated (EasyData)

    Args:
        sourceFolder (_type_): source folder
        saveFolder (_type_): save folder
    """
    fileLists = getFiles(sourceFolder, "json")

    count = 0;
    allCounts = len(fileLists)
    for fileName in fileLists:
        imgFile = fileName.split(".")[0] + ".jpg"
        shutil.copyfile(sourceFolder + "\\" + imgFile, saveFolder + "\\" + imgFile)

        filePath = sourceFolder + "\\" + fileName
        annotatedData = formatData(filePath)
        with open(saveFolder + "\\" + fileName, 'w', encoding='utf-8') as f:
            f.write(json.dumps(annotatedData, ensure_ascii=False))
        count += 1
        print(str(count) + "/" + str(allCounts))

    print("All Done!!!")


def main():
    sourceFolder = r"E:\AI\PN-AI\sliced\苯酚2#灌島\mark"
    saveFolder = r"E:\AI\PN-AI\sliced\苯酚2#灌島\mark2"

    ChangeDataFormat(sourceFolder, saveFolder)


if __name__ == '__main__':
    main()

import docx
import uuid
import os, re

fileList = []

def scanDir(filePath):
    files = os.listdir(filePath)

    # 遍历所有文件
    for file in files:
        # 把文件路径和文件名结合起来
        file_d = os.path.join(filePath, file)
        # 判断该文件是单个文件还是文件夹
        if os.path.isdir(file_d):  # 如果是文件夹则递归调用 scanDir() 函数
            scanDir(file_d)
        else:
            if (file_d.endswith(".pdf") == False):
                fileList.append(file_d)

def copyImgFromWord(word_path, result_path):
    count = 0
    try:
        doc = docx.Document(word_path)
        dict_rel = doc.part._rels
        for rel in dict_rel:
            rel = dict_rel[rel]
            if "image" in rel.target_ref:
                if not os.path.exists(result_path):
                    os.makedirs(result_path)
                img_name = re.findall("/(.*)", rel.target_ref)[0]
                word_name = os.path.splitext(word_path)[0]
                if os.sep in word_name:
                    new_name = word_name.split('\\')[-1]
                else:
                    new_name = word_name.split('/')[-1]
                img_name = f'{new_name}-'+'.'+f'{img_name}'
                count += 1
                with open(f'{result_path}/{uuid.uuid1()}{img_name}', "wb") as f:
                    f.write(rel.target_part.blob)
    except:
        pass


if __name__ == "__main__":
    scanDir("E:\\img\\20220324")

    for word_path in fileList:
        copyImgFromWord(word_path, "E:\\img\\20220324Img")




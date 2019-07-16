# --*-- coding=utf-8 --*--

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

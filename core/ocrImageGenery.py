# --*-- coding=utf-8 --*--

import os
import time
import traceback
from PIL import Image
from conf.config import TMP
from lib.fileRead import get_file_content
from lib.orcExcepts import NotImageError
from base import Basic

if not TMP:
    TMP = "/tmp/"
if not TMP.endswith("/"):
    TMP = TMP + "/"


class BasicImageGenery(Basic):
    def __init__(self):
        self.options = {}
        self.options["detect_direction"] = "true"

    def __read_image(self, file_path):
        '''
        open image
        :param file_path:
        :return: obj
        '''

        try:
            return Image.open(file_path)
        except:
            raise NotImageError

    def _zip_image(self, file_path, betstart=2):
        '''
        zip image, when the size less than about 512K return
        :param file_path:
        :param betstart:
        :return:
        '''

        bet = betstart
        im = self.__read_image(file_path)

        while True:
            w, h = im.size
            im.thumbnail((w / bet, h / bet))
            t_file = os.path.basename(file_path)
            save_path = TMP + t_file.split(".")[0] + "_" + str(bet) + ".jpg"
            im.save(save_path, 'jpeg')
            time.sleep(0.1)
            if os.path.getsize(save_path) > 539528:
                bet += 1
                os.remove(save_path)
            else:
                return save_path

    def _ensure_image_size(self, file_path, betstart=2):
        '''
        make sure the file size less than 512K, orz, zip it
        :param file_path:
        :param betstart:
        :return:
        '''

        size = os.path.getsize(file_path)
        if size > 539528:
            return self._zip_image(file_path, betstart)
        else:
            return file_path

    def __list_files(self, path):
        '''
        show all the iamge file path
        :param path:
        :return:
        '''

        allfile = []
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                filepath = os.path.join(root, name)
                filepath = filepath.replace("\\", "/", 1)
                if "\\" in filepath:
                    raise ValueError("%s 不能有子目录" % path)
                allfile.append(filepath)

        return allfile

    def _ocr_image(self, file_path, is_show=False):
        '''
        get the image word info, and save
        :param file_path:
        :param is_show:  print the result default false
        :return:
        '''

        image = get_file_content(file_path)
        reslut = self.client.basicGeneral(image, self.options)

        self.save("=-" * 20 + "   " + file_path + "   " + "=-" * 20)
        reslut_words = self._format_result(result=reslut)
        self.save(reslut_words)

        if is_show:
            self._show(reslut_words)

    def general_one(self, file_path='exm.jpg', is_show=False):
        '''
        collect an image word
        :param file_path:
        :param is_show:
        :return:
        '''

        try:
            file_path = self._ensure_image_size(file_path)
        except NotImageError, e:
            print "%s 不是图片" % file_path
            return
        except Exception, e:
            print traceback.format_exc()
            print "%s 分析失败" % file_path
            return

        self._ocr_image(file_path, is_show)

    def general_path(self, path, is_show=False):
        '''
        collect the path
        :param path:
        :param is_show:
        :return:
        '''

        try:
            allfile = self.__list_files(path)
        except ValueError, e:
            print e.message
            return
        except Exception, e:
            print traceback.format_exc()
            print "%s 获取图片失败" % path
            return

        for file in allfile:
            self.general_one(file, is_show)

    def __str__(self):
        return "<BasicImageGenery> Class WordOcr"


if __name__ == '__main__':
    s = BasicImageGenery()
    # s.general_one(file_path='exm.jpg', is_show=True)
    s.general_one(file_path='test.jpg', is_show=True)

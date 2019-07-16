# --*-- coding=utf-8 --*--

import io

from conf.config import SAVEFILE
from lib.sdkClient import client

savefile = io.open(SAVEFILE, mode='a+', encoding='utf-8')


class Basic(object):
    client = client
    savefile = savefile

    def save(self, res):
        if isinstance(res, basestring):
            self.savefile.write(res.encode('utf-8') + u"\n")
            self.savefile.flush()
        elif isinstance(res, list):
            self.savefile.writelines(res)
            self.savefile.write(u"\n")
            self.savefile.flush()
        else:
            self.savefile.write(bytes(res.encode('utf-8')))
            self.savefile.flush()

    def _format_result(self, result):
        words_list = []
        res = result.get("words_result")
        for wordsline in res:
            words_list.append(wordsline.get("words") + "\n")
        return words_list

    def _show(self, result):
        if isinstance(result, basestring):
            print result
        else:
            for words in result:
                print words

    def __str__(self):
        return "<Basic> ocr class"


if __name__ == '__main__':
    Basic().save(['1', '2', '3'])
    Basic().save(["seiee"])

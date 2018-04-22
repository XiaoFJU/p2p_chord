# -*- coding:utf-8 -*-
import sys
import time


class ProgressBar:
    def __init__(self, count=0, total=0, width=50, show=False):
        self.count = count
        self.total = total
        self.width = width
        self.show = show

    def log(self, s='', print_end=''):

        # move to next
        self.count += 1

        sys.stdout.write(' '*(self.width + 13) + '\r')
        sys.stdout.flush()
        print(s, end=print_end)
        progress = (int)(self.width * self.count / self.total)
        sys.stdout.write('{0:5}/{1:5}: '.format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')

        if progress == self.width and not self.show:
            sys.stdout.write(' '*(self.width + 13) + '\r')
        sys.stdout.flush()


if __name__ == "__main__":
    bar = ProgressBar(total=1000)
    for i in range(1000):
        # bar.log('We have arrived at: ' + str(i + 1))
        bar.log()
        time.sleep(.001)


'''
首先 import sys
print 等於 sys.stdout.write() + 輸出換行
他不會真的輸出出去
要這樣  sys.stdout.flush()
他會印在畫面上可是他沒有真的輸出
sys.stdout.write( '-'*50 )  #放50個 '-' 到buffer
print ("hello") #印出hello+ 45個'-'
'''

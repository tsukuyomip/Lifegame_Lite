#coding: utf-8

import numpy as np
import pylab as pl
import subprocess

class My_Lifegame(object):
    def __init__(self, size = (10, 10), map = None, rng = None):
        if rng is None:
            rng = np.random.RandomState(29432)

        if map is None:
            map = []
            for y in xrange(size[1]):
                l = []
                for x in xrange(size[0]):
                    l.append(rng.binomial(p = 0.5, n = 1))
                map.append(l)

        self.size = size
        self.map = map
        self.rng = rng
        self.p = subprocess.Popen(['gnuplot','-p'], 
                                  shell=True,
                                  stdin=subprocess.PIPE,
                              )


    def run(self):
        next_l = []
        for y in xrange(self.size[1]):
            l = []
            for x in xrange(self.size[0]):
                #l.append(self.next_life(x, y))
                l.append(self.next_life(y, x))
            next_l.append(l)

        self.map = next_l


    def next_life(self, x, y):
        n = self.calc_neighber(x, y)
        if n < 2:
            return 0
        elif n == 2:
            return self.map[x][y]
        elif n == 3:
            return 1
        else:
            return 0


    def calc_neighber(self, x, y):
        n = 0
        for offset_y in xrange(-1, 2):  # offset_y = {-1, 0, 1}
            for offset_x in xrange(-1, 2):  # offset_x = {-1, 0, 1}
                if (offset_x == 0 and offset_y == 0):
                    continue

                xx = x + offset_x
                if (xx < 0):
                    xx += self.size[0]
                elif (xx >= self.size[0]):
                    xx -= self.size[0]

                yy = y + offset_y
                if (yy < 0):
                    yy += self.size[1]
                elif (yy >= self.size[1]):
                    yy -= self.size[1]

                #print xx, yy
                n += self.map[xx][yy]
        return n


    def show_img(self, p, img):
        p.stdin.write("plot '-' matrix with image\n")
        for l in self.map:
            for dat in l:
                p.stdin.write(str(dat) + ' ')
            p.stdin.write('\n')
        p.stdin.write('e\ne\n')


def demo():
    lg = My_Lifegame(size = (32, 32))
    lg.show_img(lg.p, lg.map)
    while(True):
        lg.run()
        lg.show_img(lg.p, lg.map)

if __name__ == "__main__":
    demo()

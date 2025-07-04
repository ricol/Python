#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''Conway's Game Of Life, Author Anurag Kumar(mailto:anuragkumarak95@gmail.com) 

Requirements:
  - numpy
  - random
  - time
  - matplotlib

Python:
  - 3.5

Usage:
  - $python3 game_o_life <canvas_size:int>

Game-Of-Life Rules:

 1.
 Any live cell with fewer than two live neighbours
 dies, as if caused by under-population.
 2.
 Any live cell with two or three live neighbours lives
 on to the next generation.
 3.
 Any live cell with more than three live neighbours
 dies, as if by over-population.
 4.
 Any dead cell with exactly three live neighbours be-
 comes a live cell, as if by reproduction.
 '''
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random
import sys
import time

usage_doc = 'Usage of script: script_nama <size_of_canvas:int>'

choice = [0] * 100 + [1] * 10
random.shuffle(choice)

def create_canvas(size):
    canvas = [[False for i in range(size)] for j in range(size)]
    return canvas

def seed(canvas):
    for i, row in enumerate(canvas):
        for j, _ in enumerate(row):
            canvas[i][j] = bool(random.getrandbits(1))

def run(canvas):
    ''' This  function runs the rules of game through all points, and changes their status accordingly.(in the same canvas)
    @Args:
    --
    canvas : canvas of population to run the rules on.

    @returns:
    --
    None
    '''
    canvas = np.array(canvas)
    next_gen_canvas = np.array(create_canvas(canvas.shape[0]))
    for r, row in enumerate(canvas):
        for c, pt in enumerate(row):
            # print(r-1,r+2,c-1,c+2)
            next_gen_canvas[r][c] = __judge_point(pt, canvas[r-1:r + 2, c-1:c + 2])

    canvas = next_gen_canvas
    del next_gen_canvas # cleaning memory as we move on.
    return canvas.tolist()   

def __judge_point(pt, neighbours):
    dead  = 0
    alive = 0
    # finding dead or alive neighbours count.
    for i in neighbours:
        for status in i:
            if status: alive += 1
            else: dead += 1

    # handling duplicate entry for focus pt.
    if pt: alive -= 1
    else: dead -= 1

    # running the rules of game here.
    state = pt
    if pt:
        if alive < 2:
            state = False
        elif alive == 2 or alive == 3:
            state = True
        elif alive > 3:
            state = False
    else:
        if alive == 3:
            state = True

    return state

if __name__ == '__main__':
    if len(sys.argv) != 2: raise Exception(usage_doc)

    canvas_size = int(sys.argv[1])
    # main working structure of this module.
    c = create_canvas(canvas_size)
    seed(c)
    fig, ax = plt.subplots()
    fig.show() 
    cmap = ListedColormap(['w', 'k'])
    try:
        while True:
            print("continue")
            c = run(c)            
            ax.matshow(c, cmap=cmap)
            fig.canvas.draw()
            ax.cla() 
            input("press any key to continue...")
    except KeyboardInterrupt:
        # do nothing.
        pass
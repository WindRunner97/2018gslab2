# -*- coding: utf-8  -*-
"""
Created on Thu Sep 24 16:37:21 2015
use anaconda2 5.1.0 //使用anaconda2
python version 2.7.0
@author: Eddy_zheng
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import struct 

def readfile( filename , list): 
    fr = open(filename, 'rb' )
    fsize = os.path.getsize(filename)
    fsize  = fsize / 4  #点的个数有3057个，与esp中反汇编得到的个数一模一样
    alist = []
    i = 0
    while i < fsize :
        fnum = struct.unpack('<f', fr.read(4))[0]
        i = i + 1
        alist.append(fnum)
        if i % 3 == 0 :
            list.append(alist)
            alist = []
    fr.close()
    return 


def draw():

    
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    list = []
    readfile("point.txt", list )
    #  将数据点分成三部分画，在颜色上有区分度
    for elist in list:
        ax.scatter(elist[0],elist[1],elist[2],c='r', marker='.')

    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()




    list = []
    readfile("point.txt", list )
    fig = plt.figure()  
    ax1 = fig.add_subplot(111)  
    #设置标题  
    ax1.set_title('ANSWER')  
    #设置X轴标签  
    plt.xlabel('X')  
    #设置Y轴标签  
    plt.ylabel('Y')  
    #画散点图  
    for elist in list:
        ax1.scatter(elist[0],elist[1],c='r', marker='.')
    #设置图标  
    plt.legend('x1')  
    #显示所画的图  
    plt.show()


draw()
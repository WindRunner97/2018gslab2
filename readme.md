2018GSLAB腾讯游戏安全竞赛决赛一
=======
# 一.初步分析： 
把几年前写的writeup翻了出来，希望能对后人有所帮助。这个题还是蛮有意思的。  
打开esp.exe  拖动鼠标，发现有个箭头指向一些东西，但是显示不出来。那么我们第一步就要找到那个显示不出来的图片。esp是透视的意思，所以我猜后续是不是跟FPS游戏有关。  
# 二.寻找看到图片的方法：  

WINMAIN函数中先读取了两段数据：  
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/1.png)   

把这两段数据拖到WinHex上一看，发现是两个JPG文件,把两张照片组合一下，就组成了我们看到的这个  
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/2.png)   
但其实没啥用,思路偏了,继续找。  
在sub_407270处 发现了:  
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/3.png)   
很明显就是我们要找的地方，可以nop掉，也可以改数值。
在OD里Nop掉后 发现这个图是这样的:
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/4.png)  
但是很乱，基本看不出来这是什么。  
# 3.	重新绘制图  
思路是把这些图在内存中的位置找到，将找到的点的坐标得到，再用我们更清晰的方法显示出来。
发现在OD里，这一段是存储点位置的地方，存的都是浮点数：  
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/5.png)  
从B29000开始 到B2BFC4  一共2FC4大小。

每一个点的形式是（x,y,z）
所以一共有1019个点，也与IDA中的分析吻合：  
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/6.png)  
  
使用python3（anaconda）完成图片的重新绘制。首先从olldbg中读出1019个点，将其保存在Txt中，使用python将文件还原为1019 * 3 个浮点数，代码在findflag.py中的readfile函数内。

    def readfile( filename , list): 
    fr = open(filename, 'rb' )
    fsize = os.path.getsize(filename)
    fsize = fsize / 4 #点的个数有3057个，与esp中反汇编得到的个数一模一样
    alist = []
    i = 0
    while i < fsize :
    #<f表示小端序，浮点数
    fnum = struct.unpack('<f', fr.read(4))[0]#以浮点数的形式将数据打包
    i = i + 1
    alist.append(fnum)
    if i % 3 == 0 :
    list.append(alist)#将数保存在alist内，每满三个将其存入list
    alist = []
    fr.close()
    return   
之前我们对这个文件直接进行过重定位，将输出结果保存在txt中，部分信息如下：  
3057.0  
[37.0, 9.0, -6.5]  
[38.0, 9.0, -4.099999904632568]  
[39.0, 9.0, -5.900000095367432]  
[40.0, 9.0, -4.599999904632568]  
[41.0, 9.0, -7.0]  
[73.0, 9.0, -5.599999904632568]  
[74.0, 9.0, -4.199999809265137]  
[75.0, 9.0, -6.400000095367432]  
[76.0, 9.0, -5.599999904632568]  
…… 
再将点重新绘制为二维，三维图。
Readfile函数将点数据保存在list中，draw函数将list的数据读出，并且将其化为一张三维图。  

    ax = plt.subplot(111, projection='3d') # 创建一个三维的绘图工程
    list = []
    readfile("point.txt", list )
    # 将数据画出
    for elist in list:#子列表三个元素为xyz轴
    ax.scatter(elist[0],elist[1],elist[2],c='r', marker='.')
    ax.set_zlabel('Z') # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()  


![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/7.png)  

如图可看见一个箭头，即图片中箭头，而上面不容易看清，拖动视角进行二次分析：  
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/8.png)    
由图可见 flag已经出现 为 flag：dogod字符串。
有点不清晰，不太满意
再进行二维视角分析，代码如下：

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

得出结果如下：  
![](https://github.com/WindRunner97/2018gslab2/blob/master/IMG/9.png) 
自此可以确定answer为：flag:dogod
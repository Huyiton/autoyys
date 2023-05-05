'''
群号：650774545快来一起摸鱼
'''

import random
import time
import cv2

from numpy import frombuffer, uint8, array, random
import numpy as np
from win32con import SRCCOPY, DESKTOPHORZRES, DESKTOPVERTRES, WM_LBUTTONUP, WM_LBUTTONDOWN, WM_ACTIVATE, WA_ACTIVE, MK_LBUTTON, WM_NCHITTEST, WM_SETCURSOR, HTCLIENT, WM_MOUSEMOVE
from win32gui import IsWindow, GetWindowText, FindWindow, FindWindowEx, IsWindow, GetWindowRect, GetWindowDC, DeleteObject, SetForegroundWindow, IsWindowVisible, GetDC, GetParent
from win32ui import CreateDCFromHandle, CreateBitmap
from win32api import GetSystemMetrics, SendMessage, MAKELONG, PostMessage
from PIL import Image
from win32gui import FindWindow

from ctypes import windll
from ctypes.wintypes import RECT
from ctypes import Structure, c_long
from ctypes import windll
from ctypes.wintypes import RECT
from math import dist

from cBezier import BezierTrajectory


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


#用于截图操作
def getScreen(handleNum :int):
    """
    windows api 截图
    可以后台，可被遮挡，但是不能点击最小化 图片不包括标题栏边框等1280x720
    :param handleNum:句柄
    :return:截取的这张图
    """
    winRect = GetWindowRect(handleNum)
    width = winRect[2] - winRect[0]  # 右x-左x
    height = winRect[3] - winRect[1]  # 下y - 上y 计算高度
    winSize = [width, height]
    scaleRate = 1
    
    widthScreen = int(winSize[0] / scaleRate)
    heightScreen = int(winSize[1] / scaleRate)

    # 获取窗口的客户区域
    rect = RECT()
    windll.user32.GetClientRect(handleNum, rect)
    # 将客户区域的坐标转换为屏幕坐标
    topLeft = POINT(rect.left, rect.top)
    windll.user32.ClientToScreen(handleNum, topLeft)
    bottomRight = POINT(rect.right, rect.bottom)
    windll.user32.ClientToScreen(handleNum, bottomRight)

    # 返回句柄窗口的设备环境
    hwndDc = GetWindowDC(handleNum)
    # 创建设备描述表
    mfcDc = CreateDCFromHandle(hwndDc)
    # 创建内存设备描述表
    saveDc = mfcDc.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDc, widthScreen, heightScreen)
    # 将截图保存到saveBitMap中
    saveDc.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDc.BitBlt((0, 0), (widthScreen, heightScreen), mfcDc, (topLeft.x, topLeft.y), SRCCOPY)

    # 保存图像
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    imgSrceen = frombuffer(signedIntsArray, dtype='uint8')
    imgSrceen.shape = (heightScreen, widthScreen, 4)
    #imgSrceen = cv2.cvtColor(imgSrceen, cv2.COLOR_BGRA2GRAY)
    imgSrceen = cv2.resize(imgSrceen, (winSize[0], winSize[1]))

    # 边框的宽度和高度
    #边框修正，去除上边框和又边框
    border_width_right = 42
    border_height_top = 34

    # 裁剪图片，去掉右边和上面的边框
    imgSrceen = imgSrceen[border_height_top:, :widthScreen - border_width_right]


    # 测试显示截图图片
    #cv2.namedWindow('imgSrceen')  # 命名窗口
    #cv2.imshow("imgSrceen", imgSrceen)  # 显示
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    DeleteObject(saveBitMap.GetHandle())
    saveDc.DeleteDC()
    mfcDc.DeleteDC()
    return imgSrceen

#用于点击操作
def click(handleNum: int, pos: list):
    '''
    :param handleNum:句柄
    '''
    pos[1] += 34#边框修正，去除上边框
    PostMessage(handleNum, WM_ACTIVATE, WA_ACTIVE, 0)  # 激活窗口
    # 先移动到第一个点
    tmpPos = MAKELONG(pos[0], pos[1])
    SendMessage(handleNum, WM_NCHITTEST, 0, tmpPos)
    SendMessage(handleNum, WM_SETCURSOR, handleNum, MAKELONG(HTCLIENT, WM_LBUTTONDOWN))
    PostMessage(handleNum, WM_LBUTTONDOWN, MK_LBUTTON, tmpPos)
    time.sleep((random.randint(0.3, 5))/1000.0)
    # 最后释放鼠标
    tmpPos = MAKELONG(pos[0], pos[1])
    PostMessage(handleNum, WM_LBUTTONUP, 0, tmpPos)

#用于滑动操作
def swipe(handleNum :int, startPos :list, endPos :list) -> None:
    """
    后台滑动
    :param handleNum:句柄
    :param startPos:起点
    :param endPos:终点
    """
    startPos[1] += 34
    endPos[1] += 34
    interval: int = 2.5  # 每次移动的间隔时间
    numberList :int = int(dist(startPos, endPos)/(1.5*interval))  # 表示每秒移动1.5个像素点， 总的时间除以每个点10ms就得到总的点的个数
    le = random.randint(2, 4)  #
    deviation = random.randint(20, 40)  # 幅度
    type = 3
    obbsType = random.random()   # 0.8的概率是先快中间慢后面快， 0.1概率是先快后慢， 0.1概率先慢后快
    if obbsType>0 and obbsType <=0.8:
        type = 3
    elif obbsType<0.9:
        type = 2
    else: obbsType = 1
    trace :list = BezierTrajectory.trackArray(start=startPos, end=endPos, numberList=numberList, le=4,
                 deviation=30, bias=0.5, type=3, cbb=0, yhh=20)

    PostMessage(handleNum, WM_ACTIVATE, WA_ACTIVE, 0)  # 激活窗口
    # 先移动到第一个点
    tmpPos = MAKELONG(trace[0][0], trace[0][1])
    SendMessage(handleNum, WM_NCHITTEST, 0, tmpPos)
    SendMessage(handleNum, WM_SETCURSOR, handleNum, MAKELONG(HTCLIENT, WM_LBUTTONDOWN))
    PostMessage(handleNum, WM_LBUTTONDOWN, MK_LBUTTON, tmpPos)
    # 一点一点移动鼠标WM_LBUTTONUP
    for pos in trace:
        tmpPos = MAKELONG(pos[0], pos[1])
        PostMessage(handleNum, WM_MOUSEMOVE, MK_LBUTTON, tmpPos)
        time.sleep((interval+random.randint(-2, 2))/1000.0)
    # 最后释放鼠标
    tmpPos = MAKELONG(trace[-1][0], trace[-1][1])
    PostMessage(handleNum, WM_LBUTTONUP, 0, tmpPos)


#用于判断图片的相似性。返回目标图片的坐标
def find_target_image(screenshot, target_image_path):
    """
    后台滑动
    :param screenshot:截图函数获得的图片变量
    :param target_image_path:需要点击的图片的地址
    """

    
    # 读取目标图片
    target = cv2.imread(target_image_path, 0)
    # 获取目标图片的宽度和高度
    target_height, target_width = target.shape
    # 将PIL图片转为OpenCV格式，并转换为灰度图像
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    # 使用matchTemplate函数进行模板匹配
    result = cv2.matchTemplate(screenshot_cv, target, cv2.TM_CCOEFF_NORMED)  
    # 设定阈值
    threshold = 0.8
    # 找到匹配程度最高的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        # 在目标图片的区域内生成随机坐标
        random_x = random.randint(0, target_width - 1)
        random_y = random.randint(0, target_height - 1)
        random_point = [max_loc[0] + random_x, max_loc[1] + random_y]
        return random_point
    else:
        return None


#用于从区域内一点滑动到另外一点
def random_point(x1, y1, x2, y2):
    """
    在给定的区域内随机生成一个点的坐标。

    :param x1: 区域左侧的 x 坐标
    :param y1: 区域顶部的 y 坐标
    :param x2: 区域右侧的 x 坐标
    :param y2: 区域底部的 y 坐标
    :return: 返回一个数组，包含随机生成的点的 (x, y) 坐标
    """
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    pos=[x, y]
    return pos


#用于测试是否能够捕获到窗口句柄
#hwnd = FindWindow(None, '夜神模拟器1')
#print(hwnd)

#用于测试是否能够正确获得1280*780的截图
#img=getScreen(hwnd)
#print("Image size: ", img.shape)


#配合模拟器开发者模式显示指针位置，用于测试click函数是否准确识别坐标
#a=click(hwnd,[300,500])
#print(a)

#配合模拟器开发者模式显示指针位置，用于测试swipe函数是否准确识别坐标
#b=swipe(hwnd,[350,500],[300,600])
#print(b)

#用于测试是否能够生成目标区域随机一点的坐标用来滑动和点击
#print(random_point(300,500,600,800))

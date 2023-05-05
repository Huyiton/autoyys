from win32gui import FindWindow
from brick import getScreen,click,swipe,find_target_image，random_point #导入砖头开始砌墙

#建房子用的砖头已经建立好。大家想建什么房子，自己动手，因为每个人的需求不一样，自己的需求自己满足，出新活动了自己更新。

#getScreen(handleNum :int)                              截一张图1280*720，返回这张图
#click(handleNum: int, pos: list)                       点击，随机延时已经设定好
#swipe(handleNum :int, startPos :list, endPos :list)    滑动，逻辑基于cbb写的贝塞尔曲线，随机延时已经设定好
#find_target_image(screenshot, target_image_path)       判断是否相似，返回目标图片的随机坐标，自己去截图
#random_point(x1, y1, x2, y2)                           返回区域内随机一点，用于滑动


#例1：
'''
hwnd = FindWindow(None, '夜神模拟器1')
#可以实现多开，或者队长队员相互配合，比如 '夜神模拟器1'登录队长号，'夜神模拟器2'登录队员号
#目前截图的函数只支持夜神模拟器，因为每种模拟器，截取的窗口的边框大小都不一样，如果想使用别的模拟器需要修改brick的边框修正，否则坐标会不准确
screenshot=getScreen(hwnd)
zhunbei=("zhandou.png")
pos=find_target_image(screenshot, zhunbei)
click(hwnd,pos)
print(pos)
'''

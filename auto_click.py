import time
import pyautogui
import pyperclip
from tools import print_text
from pynput.keyboard import Controller,Key

class AUTO_CLICK(object):
    def __init__(self,tk_Text,tk_root):
        self.tk_Text=tk_Text
        self.tk_root=tk_root
        self.keyboard=Controller()

    def start(self,data,repetition,set_time):
        try:
            if repetition:
                while True:
                    self.__begin_work(data,set_time)
            else:
                self.__begin_work(data,set_time)
            print_text(self.tk_Text, "-----完成-----")
        except ValueError:
            print_text(self.tk_Text, "命令出错!!!")
        finally:
            self.tk_root.deiconify()
            time.sleep(1)
            self.keyboard.press(Key.esc)  # 模拟按键esc结束监听线程

    def __begin_work(self,commands,set_time):
        total_num=len(commands)
        # 执行每一行
        for i,command in enumerate(commands):
            opt_command,opt_object,reTry = command
            reTry=int(reTry)
            # 1单击左键
            if opt_command == "单击":
                if reTry:
                    for re in range(reTry):
                        print_text(self.tk_Text,"[{}/{}] 单击：{}".format(i+1,total_num,opt_object))
                        self.__mouseclick(1, "left", opt_object, set_time)
                else:
                    while True:
                        print_text(self.tk_Text,"[{}/{}] 单击：{}".format(i+1, total_num, opt_object))
                        self.__mouseclick(1, "left", opt_object, set_time)
            # 2双击左键
            elif opt_command == "双击":
                if reTry:
                    for re in range(reTry):
                        print_text(self.tk_Text,"[{}/{}] 双击：{}".format(i+1,total_num,opt_object))
                        self.__mouseclick(2, "left", opt_object, set_time)
                else:
                    while True:
                        print_text(self.tk_Text,"[{}/{}] 双击：{}".format(i+1,total_num,opt_object))
                        self.__mouseclick(2, "left", opt_object, set_time)
            # 3右键
            elif opt_command == "右键":
                if reTry:
                    for re in range(reTry):
                        print_text(self.tk_Text,"[{}/{}] 右键：{}".format(i+1,total_num,opt_object))
                        self.__mouseclick(1, "right", opt_object, set_time)
                else:
                    while True:
                        print_text(self.tk_Text,"[{}/{}] 右键：{}".format(i+1,total_num,opt_object))
                        self.__mouseclick(1, "right", opt_object, set_time)
            # 4拖拽
            elif opt_command == "拖拽":
                if reTry:
                    for re in range(reTry):
                        print_text(self.tk_Text,"[{}/{}] 拖拽：{}".format(i+1,total_num,opt_object))
                        self.__drag(opt_object,set_time)
                else:
                    while True:
                        print_text(self.tk_Text,"[{}/{}] 拖拽：{}".format(i+1,total_num,opt_object))
                        self.__drag(opt_object,set_time)
            # 5输入
            elif opt_command == "输入":
                print_text(self.tk_Text,"[{}/{}] 输入：{}".format(i+1,total_num,opt_object))
                pyperclip.copy(opt_object)
                pyautogui.hotkey('ctrl', 'v')
            # 6等待
            elif opt_command == "等待":
                print_text(self.tk_Text,"[{}/{}] 等待{}秒".format(i+1,total_num,opt_object))
                time.sleep(int(opt_object))
            # 7滚轮
            elif opt_command == "滚轮":
                print_text(self.tk_Text,"[{}/{}] 滚轮：{}像素".format(i+1,total_num,int(opt_object)))
                pyautogui.scroll(int(opt_object))
                
    def __mouseclick(self,clickTimes,l_or_r,obj,set_time):
        # 处理坐标位置
        if ".png" not in obj:
            obj=obj[1:-1].split(",")
        # 操作图片
        if type(obj) is str:
            while True:
                # 根据图片找到位置
                location = pyautogui.locateCenterOnScreen(obj, confidence=0.8)
                if location is not None:
                    pyautogui.click(location.x, location.y, clicks=clickTimes, interval=set_time, duration=set_time, button=l_or_r)
                    break
                print_text(self.tk_Text,"等待匹配,0.5秒后重试")
                time.sleep(0.5)
        # 操作位置
        else:
            pyautogui.click(int(obj[0]), int(obj[1]), clicks=clickTimes, interval=set_time, duration=set_time, button=l_or_r)

    def __drag(self,obj,set_time):
        # 处理目标位置
        ori,dist=obj.split(" -> ")
        ori_x,ori_y=ori[1:-1].split(",")
        dist_x,dist_y=dist[1:-1].split(",")
        # 开始拖拽
        pyautogui.moveTo(int(ori_x),int(ori_y),duration=set_time)
        pyautogui.dragTo(int(dist_x),int(dist_y),duration=set_time)
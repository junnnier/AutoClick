from tkinter import Tk,Canvas
from datetime import datetime
from pynput import keyboard
import ctypes

class PrScreen(object):
    def xFunc1(self, event):
        # 鼠标左键按下
        if event.state == 8:
            self.position=(event.x,event.y)
            self.__win.quit()
            self.__win.destroy()

    def start(self):
        self.__win = Tk()
        self.__win.attributes("-alpha", 0.4)
        self.__win.attributes("-fullscreen", True)
        self.__win.attributes("-topmost", True)
        # 获取屏幕宽高
        self.__width, self.__height = self.__win.winfo_screenwidth(), self.__win.winfo_screenheight()
        # 创建画布
        self.__canvas = Canvas(self.__win, width=self.__width, height=self.__height)
        # 绑定事件
        self.__win.bind('<Button-1>', self.xFunc1)
        self.__win.mainloop()

prscreen = PrScreen()

def print_text(tk_Text,string):
    tk_Text["state"] = "normal"
    tk_Text.insert("end", "{}\n{}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],string))
    tk_Text.see("end")
    tk_Text["state"] = "disable"

# 用于强制停止线程弹出错误
class Define_error(Warning):
    def __init__(self):
        pass

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("无效的线程id ",tid)
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("线程{}退出失败".format(tid))

def stop_thread(thread):
    thread._is_stopped = True
    _async_raise(thread.ident, Define_error)

def key_release(key,click_thread,tk_Text):
    if key==keyboard.Key.esc:
        stop_thread(click_thread)
        print_text(tk_Text, "-----手动中断-----")
        return False


if __name__ == '__main__':
    prscreen.start()
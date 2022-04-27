from tkinter import Tk,Canvas
from datetime import datetime
from pynput.keyboard import Key,Listener,Controller
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
    current_time=datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.%f")
    tk_Text.insert("end", "{}\n{}\n".format(current_time[:-3],string))
    tk_Text.update()
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

def key_press(key):
    return True

def key_release(key):
    if key==Key.esc:
        return False

# 监控线程执行
def monitor_thread_execution(tk_root,tk_Text,click_thread):
    listener=Listener(on_press=key_press,on_release=key_release)
    listener.start()
    keyboard=Controller()
    tk_root.iconify()  # 最小化窗口
    while True:
        if not click_thread.is_alive():
            keyboard.release(Key.esc)  # 模拟按下esc结束监听线程
            break
        if not listener.is_alive():
            stop_thread(click_thread)
            print_text(tk_Text, "-----手动中断-----")
            break
    tk_root.deiconify()


if __name__ == '__main__':
    prscreen.start()
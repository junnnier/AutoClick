# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import messagebox,filedialog
from tkinter import ttk
from data import db
from tools import prscreen,print_text,key_release
from auto_click import AUTO_CLICK
from threading import Thread
import webbrowser
from pynput.keyboard import Listener

class Mainwindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("自动点击")
        self.root.geometry("713x395+{}+{}".format((self.root.winfo_screenwidth()-713)//2,(self.root.winfo_screenheight()-395-47)//2))
        self.root.resizable(0,0)
        self.create_page()
        self.root.iconbitmap(os.path.join(self.resource_path(),'logo.ico'))
        self.auto_click = AUTO_CLICK(self.info_text,self.root)
        self.root.mainloop()

    def create_page(self):
        # 菜单栏
        meunbar = tk.Menu(self.root)
        filemenu = tk.Menu(meunbar,tearoff=0)
        filemenu.add_command(label="保存到...",command=self.save_to_csv)
        filemenu.add_command(label="导入",command=self.load_csv_file)
        filemenu.add_command(label="清空指令",command=self.delete_table_all_data)
        filemenu.add_separator()
        self.keep_root_value=tk.IntVar()
        filemenu.add_checkbutton(label="保持显示",variable=self.keep_root_value)
        self.loop_execution_value=tk.IntVar()
        filemenu.add_checkbutton(label="循环执行",variable=self.loop_execution_value)
        filemenu.add_separator()
        filemenu.add_command(label="退出",command=self.root.quit)
        aboutmenu = tk.Menu(meunbar,tearoff=0)
        aboutmenu.add_command(label="关于",command=self.show_about)
        meunbar.add_cascade(label="文件", menu=filemenu)
        meunbar.add_cascade(label="帮助", menu=aboutmenu)
        self.root.config(menu=meunbar)
        # 显示表
        table_frame=tk.Frame(self.root)
        table_frame.grid(row=0,column=0,padx=10,pady=10)
        table_scrollbar=tk.Scrollbar(table_frame)
        table_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        column_values={"num":["步骤",50],"command_type":["指令类型",80],"operate_obj":["操作对象",250],"loop_times":["循环次数",80]}
        self.table=ttk.Treeview(table_frame, show="headings",columns=tuple(column_values.keys()),yscrollcommand=table_scrollbar.set)
        for k,v in column_values.items():
            self.table.column(k,width=v[1],anchor="center",stretch=0)
            self.table.heading(k,text=v[0])
        self.table.bind('<Button-1>', self.handle_move_column)
        self.table.pack()
        table_scrollbar.config(command=self.table.yview)
        # 操作界面
        label_frame=tk.LabelFrame(self.root,text="设置点击过程",labelanchor="n",width=478,height=135)
        label_frame.grid_propagate(0)
        label_frame.grid(row=1,column=0,padx=10,pady=(0,10))
        # -----
        command_frame=tk.Frame(label_frame)
        command_frame.grid(row=0,column=0,padx=10,pady=10,sticky="W")
        command_label=tk.Label(command_frame,text="指令类型：")
        command_label.grid(row=0,column=0)
        self.command_combobox=ttk.Combobox(command_frame,width=4,state="readonly",value=["单击","双击","右键","输入","等待","滚轮"])
        self.command_combobox.current(0)
        self.command_combobox.grid(row=0,column=1)
        self.command_combobox.bind("<<ComboboxSelected>>",self.combobox_choice)
        # -----
        loop_frame=tk.Frame(label_frame)
        loop_frame.grid(row=0,column=1,pady=10,sticky="W")
        loop_lable=tk.Label(loop_frame,text="循环次数：")
        loop_lable.grid(row=0,column=0)
        self.loop_entry=tk.Entry(loop_frame,width=6)
        self.loop_entry.insert(0,"1")
        self.loop_entry.grid(row=0,column=1)
        # -----
        operate_frame=tk.Frame(label_frame)
        operate_frame.grid(row=1,column=0,columnspan=4,padx=10,sticky="W")
        operate_label=tk.Label(operate_frame,text="操作对象：")
        operate_label.grid(row=0,column=0)
        self.operate_entry=tk.Entry(operate_frame,width=54)
        self.operate_entry.grid(row=0,column=1)
        # -----
        button_frame=tk.Frame(label_frame)
        button_frame.grid(row=2,column=0,columnspan=2,padx=(75,0),pady=10,sticky="NSWE")
        add_button=tk.Button(button_frame,text="点击位置",command=self.get_pixel_position)
        add_button.grid(row=0,column=0)
        add_button=tk.Button(button_frame,text="图片路径",command=self.get_image_path)
        add_button.grid(row=0,column=1,padx=(10,0))
        # -----
        button_frame_2=tk.Frame(label_frame)
        button_frame_2.grid(row=2,column=2,columnspan=2,padx=(20,10),pady=10,sticky="NSWE")
        add_button=tk.Button(button_frame_2,text="插入",width=6,command=self.insert_table_data)
        add_button.grid(row=0,column=0)
        add_button=tk.Button(button_frame_2,text="删除",width=6,command=self.delete_table_data)
        add_button.grid(row=0,column=1,padx=(10,0))
        add_button=tk.Button(button_frame_2,text="添加",width=6,command=self.add_table_data)
        add_button.grid(row=0,column=2,padx=(10,0))
        # 显示信息
        right_frame=tk.Frame(self.root)
        right_frame.grid(row=0,column=1,rowspan=2,padx=(0,10),pady=10)
        # -----
        text_frame=tk.Frame(right_frame)
        text_frame.grid(row=0,column=0)
        text_scrollbar=tk.Scrollbar(text_frame)
        text_scrollbar.grid(row=0,column=1,sticky="NS")
        self.info_text=tk.Text(text_frame,width=26,state="disable",yscrollcommand=text_scrollbar.set)
        self.info_text.grid(row=0, column=0, sticky="NS")
        text_scrollbar.config(command=self.info_text.yview)
        # -----
        start_button=tk.Button(right_frame,text="开始",height=2,command=self.start_button)
        start_button.grid(row=1,column=0,pady=(10,2),sticky="WE")

    # 资源访问路径
    def resource_path(self):
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return base_path

    # 获取设置的命令数据
    def get_set_command(self):
        command_combobox_value=self.command_combobox.get()
        loop_entry_value=self.loop_entry.get()
        operate_entry_value=self.operate_entry.get()
        # 检查参数
        if not loop_entry_value.isdigit():
            messagebox.showinfo("警告",message="循环次数：必须填入整数！")
            return None
        elif operate_entry_value=="":
            messagebox.showinfo("警告",message="操作对象：不能为空！")
            return None
        else:
            return [command_combobox_value,operate_entry_value,loop_entry_value]

    # 显示表格数据
    def show_table_data(self):
        # 清空原数据
        item=self.table.get_children()
        for i in item:
            self.table.delete(i)
        # 显示
        for i,item in enumerate(db.data):
            self.table.insert("","end",value=[i+1]+item)
        self.table.yview_moveto(1.0)

    # 增加操作命令
    def add_table_data(self):
        single_data=self.get_set_command()
        if single_data:
            db.add_data(single_data)  # 加入数据
            self.show_table_data() # 显示

    # 插入表格某个数据
    def insert_table_data(self):
        index_num=self.table.selection()
        if index_num:
            single_data=self.get_set_command()
            if single_data:
                value=self.table.item(index_num[0],"values")
                db.insert_data(int(value[0])-1,single_data)
                self.show_table_data()

    # 删除表格某个数据
    def delete_table_data(self):
        index_num=self.table.selection()
        if index_num:
            for i in range(len(index_num),0,-1):
                value=self.table.item(index_num[i-1],"values")
                db.remove_data(int(value[0])-1)
            self.show_table_data()

    # 删除表格所有数据
    def delete_table_all_data(self):
        db.remove_all_data()
        self.show_table_data()

    # 获取点击像素位置
    def get_pixel_position(self):
        self.root.iconify()
        prscreen.start()
        self.operate_entry.delete(0,"end")  # 清空
        self.operate_entry.insert(0,str(prscreen.position))
        self.root.deiconify()

    # 获取图片路径
    def get_image_path(self):
        image_path=filedialog.askopenfilename()
        self.operate_entry.delete(0, "end")  # 清空
        self.operate_entry.insert(0, image_path)

    # 命令数据保存到csv文件
    def save_to_csv(self):
        save_path=filedialog.asksaveasfilename(initialfile="auto_click.csv",filetypes=[("csv文件",".csv")])
        if save_path:
            db.save_data(save_path)
            print_text(self.info_text,"保存到 {}".format(save_path))

    # 加载csv文件数据
    def load_csv_file(self):
        file_path=filedialog.askopenfilename(filetypes=[("csv文件",".csv")])
        if file_path:
            db.load_data(file_path)
            self.show_table_data()
            print_text(self.info_text,"导入成功！")

    # 开始按钮
    def start_button(self):
        print_text(self.info_text,"开始运行...")
        if not self.keep_root_value.get():
            self.root.iconify()  # 最小化窗口
        click_thread=Thread(target=self.auto_click.start,args=(db.data,self.loop_execution_value.get()))
        click_thread.setDaemon(True)
        listener = Listener(on_release=lambda key:key_release(key,click_thread,self.info_text))
        listener.start()
        click_thread.start()

    # 禁止移动列宽
    def handle_move_column(self,event):
        if self.table.identify_region(event.x, event.y) == "separator":
            return "break"

    # 列表盒改变选择时触发
    def combobox_choice(self,event):
        temp=self.command_combobox.get()
        if temp in ["输入","等待","滚轮"]:
            self.loop_entry.delete(0,"end")
            self.loop_entry.insert(0,"1")
            self.loop_entry["state"]="disable"
        else:
            self.loop_entry["state"] = "normal"

    def show_about(self):
        webbrowser.open("https://github.com/junnnier/auto_click")


if __name__=="__main__":
    Mainwindow()
## 介绍
这是一个可视化的自动点击的程序。

![gui界面](https://github.com/junnnier/auto_click/blob/main/gui.png)
## 使用说明
- 指令和对应的操作对象：
    - 单击、双击、右键（操作对象可以是下面其中一个）
        - 位置坐标：点击按钮**点击位置**获取。
        - 图片路径：当不确定点击目标出现的位置时，首先将要点击的目标截取保存为.png格式的图片（路径和图片名必须是全英文），通过按钮**图片路径**选中要操作的图片，软件会在桌面上自动寻找并点击该图片出现的地方。
    - 拖拽
        - 拖拽坐标：点击按钮**拖拽位置**获取。按下鼠标左键然后移动到需要的位置释放左键，完成拖拽位置获取。
    - 输入
        - 文本：填入所需要输入的文本内容。
    - 等待
        - 大于0的整数：单位为秒。
    - 滚轮
        - 带+/-的整数：滚动的像素距离，如+300表示鼠标滚轮向上滚动，-300表示鼠标滚轮向下滚动。

- 循环次数：该条指令执行的次数（大于等于0的整数，默认1次），如果填0，表示无限次。当指令为输入、等待、滚轮时无法修改。

- 添加/插入/删除：设置好指令后，点击**添加**按钮将该条指令记录到执行列表中；点击**插入**按钮将该条指令插入到执行列表中选中的前一条；也可在执行列表中选中某一条指令，点击**删除**按钮去除。

- 导出到.../加载：将执行列表中的指令导出到csv文件进行保存，以便以后使用，下次使用时加载该文件即可。

- 清空指令：快速清除执行列表中的所有指令。

- 保持显示：选中后，程序运行时界面不会最小化隐藏。如果是单个屏幕，可能会影响到点击位置。如果有多个屏幕，可放在副屏观察打印的运行状况。默认不选中。

- 循环执行：选中后，程序运行时一直重复执行列表中的指令，直到用户手动中断。默认不选中。

- 点击模式：模拟/快速 两种模式，模拟模式下仿照人类移动鼠标和点击速度，快速模式则以最大速度运行。默认模拟。

- ESC键：自动点击过程中的任意时刻，可按键盘上的ESC键强制中断。
## 注意事项
文件auto_click.py中函数的参数confidence是匹配图片过程中筛选的置信度，降低误点击率，如使用则环境中需要安装opencv库。如不需要可以删除该参数。
~~~ python
locateCenterOnScreen(obj, confidence=0.8)
~~~
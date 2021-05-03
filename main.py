import ctypes
import os
import shutil
import time
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
from tkinter import ttk
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab
from scipy.interpolate import interpolate


# to do
# 将界面大小固定

# 删除文件前n行
def delete_first_lines(filename, count):
    fin = open(filename, 'r')
    a = fin.readlines()
    fout = open(filename, 'w')
    b = ''.join(a[count:])
    fout.write(b)


def read_data():
    # 读取数据
    eIAN1 = entry_IAN1.get()
    eIMN1 = entry_IMN1.get()
    eIAN2 = entry_IAN2.get()
    eIMN2 = entry_IMN2.get()
    eCHAEGR = entry_CHAEGR.get()
    if entry_NDEGv.get() == 'Dunhan':
        eNDEGv = 0
    elif entry_NDEGv.get() == 'NDE':
        eNDEGv = 1
    else:
        eNDEGv = 2
    if entry_NDEBv.get() == 'NDE':
        eNDEBv = 0
    elif entry_NDEBv.get() == 'MXR':
        eNDEBv = 1
    else:
        eNDEBv = -1
    eLMAXGv = entry_LMAXGv.get()
    ewe = entry_we.get()
    ewexe = entry_wexe.get()
    eLMAXBv = entry_LMAXBv.get()
    eBe = entry_Be.get()
    if entry_Kasier.get() == '是':
        eKasier = 1
    else:
        eKasier = 0
    eNSV = entry_NSV.get()
    eVEXT = entry_VEXT.get()
    eV1_1 = entry_V1_1.get()
    eDV_1 = entry_DV_1.get()
    eV2_1 = entry_V2_1.get()
    eV1_2 = entry_V1_2.get()
    eDV_2 = entry_DV_2.get()
    eV2_2 = entry_V2_2.get()

    f = open('RKR1_fort.5', 'w', encoding='gbk')
    f.write(
        eIAN1 + ' ' + eIMN1 + ' ' + eIAN2 + ' ' + eIMN2 + ' ' + eCHAEGR + ' ' + str(eNDEGv) + ' ' + str(eNDEBv) + '\n')
    f.write('\'Dunham Caculation		[VEXT = 23]\'' + '\n')
    f.write(eLMAXGv + '\n' + ewe + ' ' + ewexe + '\n' + eLMAXBv + '\n' + eBe + '\n')
    f.write(str(eKasier) + ' ' + eNSV + ' ' + eVEXT + '\n')
    f.write(eV1_1 + ' ' + eDV_1 + ' ' + eV2_1 + '\n')
    f.write(eV1_2 + ' ' + eDV_2 + ' ' + eV2_2)
    f.close()


def callexit():
    if messagebox.askokcancel("退出", "你是否要退出？"):
        if not os.path.exists("data"):
            os.mkdir("data")
        now = time.strftime("%m-%d-%H_%M_%S", time.localtime(time.time()))
        if os.path.exists("fort.10"):
            shutil.move("fort.10", "data/" + now + "-fort.10")
        if os.path.exists("fort.7"):
            shutil.move("fort.7", "data/" + now + "-fort.7")
        if os.path.exists("RKR1_fort.5"):
            shutil.move("RKR1_fort.5", "data/" + now + "-RKR1_fort.5")
        window.destroy()


def callulate():
    try:
        read_data()
    except():
        print("数据错误，请重新输入")

    m = ".\\bin\\RKR1.exe < RKR1_fort.5 > fort.10"
    os.system(m)

    delete_first_lines('fort.7', 3)  # 删除 fort.7 前三行

    x = [float(x.split()[0]) for x in open("fort.7")]
    y = [float(y.split()[1]) for y in open("fort.7")]

    f = interpolate.interp1d(x, y, kind='cubic')

    startNum = x[0]
    endNum = x[len(x) - 1]
    dNum = 10000

    x1 = np.linspace(startNum, endNum, dNum)
    y1 = f(x1)

    fig = pylab.gcf()
    fig.canvas.set_window_title('双原子分子势能函数曲线')
    plt.plot(x, y, '.')
    plt.plot(x1, y1, color='black')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    plt.title('势能函数曲线拟合')
    plt.xlabel('r/ANG')
    plt.ylabel('U(r)/cm^-1')
    plt.show()


if __name__ == '__main__':
    # GUI 界面
    window = tk.Tk()
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    window.tk.call('tk', 'scaling', ScaleFactor / 80)
    window.title('双原子分子势能曲线拟合')
    window.geometry('990x550')
    window.resizable(0, 0)
    window.iconbitmap('./img/rkr1.ico')
    # 字体设置
    ft = tkFont.Font(family='Arial', size=12, weight=tkFont.BOLD)
    ft1 = tkFont.Font(family='微软雅黑', size=13)
    # IAN1
    tk.Label(window, text='原子序数1', font=ft1).place(x=40, y=9)
    IAN1 = tk.StringVar(window, value='6')
    entry_IAN1 = tk.Entry(window, textvariable=IAN1, font=ft)
    entry_IAN1.place(x=150, y=10, width=100, height=30)
    # IMN1
    tk.Label(window, text='原子质量1', font=ft1).place(x=270, y=9)
    IMN1 = tk.StringVar(window, value='12')
    entry_IMN1 = tk.Entry(window, textvariable=IMN1, font=ft)
    entry_IMN1.place(x=380, y=10, width=100, height=30)
    # IAN2
    tk.Label(window, text='原子序数2', font=ft1).place(x=510, y=9)
    IAN2 = tk.StringVar(window, value='16')
    entry_IAN2 = tk.Entry(window, textvariable=IAN2, font=ft)
    entry_IAN2.place(x=620, y=10, width=100, height=30)
    # IMN2
    tk.Label(window, text='原子质量2', font=ft1).place(x=750, y=9)
    IMN2 = tk.StringVar(window, value='32')
    entry_IMN2 = tk.Entry(window, textvariable=IMN2, font=ft)
    entry_IMN2.place(x=860, y=10, width=100, height=30)

    # CHAEGR
    tk.Label(window, text='带电荷数 ', font=ft1).place(x=40, y=59)
    CHAEGR = tk.StringVar(window, value='0')
    entry_CHAEGR = tk.Entry(window, textvariable=CHAEGR, font=ft)
    entry_CHAEGR.place(x=150, y=60, width=100, height=30)
    # NDEGv
    tk.Label(window, text='展开式选择NDEGv', font=ft1).place(x=300, y=59)
    entry_NDEGv = ttk.Combobox(window, values=['Dunhan', 'NDE', 'MXR'], state="readonly", font=ft)
    entry_NDEGv.current(0)
    entry_NDEGv.place(x=480, y=60, width=100, height=30)
    # NDEBv
    tk.Label(window, text='展开式选择NDEBv', font=ft1).place(x=640, y=59)
    entry_NDEBv = ttk.Combobox(window, values=['NONE', 'NDE', 'MXR'], state="readonly", font=ft)
    entry_NDEBv.current(1)
    entry_NDEBv.place(x=820, y=60, width=100, height=30)

    # LMAXGv
    tk.Label(window, text='振动多项式阶数', font=ft1).place(x=40, y=109)
    LMAXGv = tk.StringVar(window, value='2')
    entry_LMAXGv = tk.Entry(window, textvariable=LMAXGv, font=ft)
    entry_LMAXGv.place(x=195, y=110, width=100, height=30)
    # we
    tk.Label(window, text='ωe', font=ft1).place(x=370, y=109)
    we = tk.StringVar(window, value='1.3768D03')
    entry_we = tk.Entry(window, textvariable=we, font=ft)
    entry_we.place(x=435, y=110, width=150, height=30)
    # wexe
    tk.Label(window, text='ωexe', font=ft1).place(x=640, y=109)
    wexe = tk.StringVar(window, value='-1.03D01')
    entry_wexe = tk.Entry(window, textvariable=wexe, font=ft)
    entry_wexe.place(x=735, y=110, width=150, height=30)

    # LMAXBv
    tk.Label(window, text='转动多项式阶数', font=ft1).place(x=40, y=159)
    LMAXBv = tk.StringVar(window, value='0')
    entry_LMAXBv = tk.Entry(window, textvariable=LMAXBv, font=ft)
    entry_LMAXBv.place(x=195, y=160, width=100, height=30)
    # Be
    tk.Label(window, text='Be', font=ft1).place(x=370, y=159)
    Be = tk.StringVar(window, value='8.617D-1')
    entry_Be = tk.Entry(window, textvariable=Be, font=ft)
    entry_Be.place(x=435, y=160, width=150, height=30)

    # Kasier
    tk.Label(window, text='启用 Kasier correction', font=ft1).place(x=40, y=209)
    entry_Kasier = ttk.Combobox(window, values=['是', '否'], state="readonly", font=ft)
    entry_Kasier.current(0)
    entry_Kasier.place(x=255, y=210, width=100, height=30)
    # NSV
    tk.Label(window, text='计算区间段数', font=ft1).place(x=380, y=209)
    # entry_NSV = ttk.Combobox(window, values=[2], state="readonly", font=ft)
    # entry_NSV.current(0)
    NSV = tk.StringVar(window, value='2')
    entry_NSV = tk.Entry(window, textvariable=NSV, font=ft, state="readonly")
    entry_NSV.place(x=515, y=210, width=100, height=30)
    # VEXT
    tk.Label(window, text='VEXT', font=ft1).place(x=660, y=209)
    VEXT = tk.StringVar(window, value='14.9')
    entry_VEXT = tk.Entry(window, textvariable=VEXT, font=ft)
    entry_VEXT.place(x=740, y=210, width=100, height=30)

    # V1_1
    tk.Label(window, text='第一段区间初始值', font=ft1).place(x=40, y=259)
    V1_1 = tk.StringVar(window, value='-0.4d0')
    entry_V1_1 = tk.Entry(window, textvariable=V1_1, font=ft)
    entry_V1_1.place(x=210, y=260, width=100, height=30)
    # DV_1
    tk.Label(window, text='步长', font=ft1).place(x=390, y=259)
    DV_1 = tk.StringVar(window, value='0.02d0')
    entry_DV_1 = tk.Entry(window, textvariable=DV_1, font=ft)
    entry_DV_1.place(x=440, y=260, width=100, height=30)
    # V2_1
    tk.Label(window, text='第一段区间末尾值', font=ft1).place(x=640, y=259)
    V2_1 = tk.StringVar(window, value='1.6d0')
    entry_V2_1 = tk.Entry(window, textvariable=V2_1, font=ft)
    entry_V2_1.place(x=810, y=260, width=100, height=30)

    # V1_2
    tk.Label(window, text='第二段区间初始值', font=ft1).place(x=40, y=309)
    V1_2 = tk.StringVar(window, value='1.6d0')
    entry_V1_2 = tk.Entry(window, textvariable=V1_2, font=ft)
    entry_V1_2.place(x=210, y=310, width=100, height=30)
    # DV_2
    tk.Label(window, text='步长', font=ft1).place(x=390, y=309)
    DV_2 = tk.StringVar(window, value='0.15d0')
    entry_DV_2 = tk.Entry(window, textvariable=DV_2, font=ft)
    entry_DV_2.place(x=440, y=310, width=100, height=30)
    # V2_1
    tk.Label(window, text='第二段区间末尾值', font=ft1).place(x=640, y=309)
    V2_2 = tk.StringVar(window, value='50.0d0')
    entry_V2_2 = tk.Entry(window, textvariable=V2_2, font=ft)
    entry_V2_2.place(x=810, y=310, width=100, height=30)

    ft2 = tkFont.Font(family='微软雅黑', size=10, weight=tkFont.BOLD)

    start = tk.Button(width=20, height=2, bg="#F0F0F0", font=ft2, text='开 始 计 算', command=callulate)
    start.place(x=385, y=390)

    end = tk.Button(width=20, height=2, bg="#FFA7A7", font=ft2, text='退 出 程 序', command=callexit)
    end.place(x=385, y=450)

    window.mainloop()

from pydub import AudioSegment
from os import listdir
from os import path
import os
import threading
import tkinter as tk
import traceback
# import tempfileatexit as tfae
from openpyxl import Workbook
from platform import system
from subprocess import Popen, PIPE
from tkinter import filedialog, dialog, scrolledtext, Canvas, END
from tkinter.messagebox import askyesno
from time import sleep, time

def initgui():
    # global window
    global inpath, outpath
    inpath=''; outpath=''

    def closewindow():
        ans = askyesno(title="退出确认窗口", message="真的要退出程序吗?")
        if ans:
            update_text(text1, "用户退出")
            sleep(1)
            window.destroy()
        else: return

    def readmusicfiles():
        musiclist=[]
        # update_text(text1, '源文件夹内无有效文件\n')

    def open_source():
        try:
            inpath = filedialog.askdirectory(title=u'选择源文件目录')
            if inpath != '':
                update_entry(stext, inpath)
            else:
                update_entry(stext, '源文件夹打开失败')
                update_text(text1, '源文件夹打开失败\n')
                return
            # read files
            readmusicfiles()
            if inpath != '' and outpath != '':
                btconvert.config(state='normal')
        except:
            traceback.print_exc()
            update_entry(stext, inpath)
            update_text(text1, '源文件夹读取失败\n')

    def open_target():
        try:
            outpath = filedialog.askdirectory(title=u'选择目标文件目录')
            if outpath != '':
                update_entry(ttext, outpath)
            else:
                update_entry(ttext, '输出文件夹打开失败')
                update_text(text1, '输出文件夹打开失败\n')
                return

            if outpath != '' and outpath != '':
                btconvert.config(state='normal')
        except:
            traceback.print_exc()
            update_entry(ttext, outpath)
            update_text(text1, '输出文件夹打开失败\n')

    def open_wmk():
        wmkpath = filedialog.askopenfilename(title=u'选择水印文件')
        if wmkpath != '':
            update_entry(wmktext, wmkpath)
        else:
            update_entry(wmktext, '源文件打开失败')
            update_text(text1, '源文件打开失败\n')
            return

    def call_convert():
        pass

    def show_infilter():
        pass
    # ft1 = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
    # 构建图形界面
    window = tk.Tk()
    #设置程序缩放
    # window.tk.call('tk', 'scaling', 2.1)
    window.protocol('WM_DELETE_WINDOW', closewindow)
    window.title('音频DEMO处理工具')  # 标题
    window.geometry(UI_WINDOW_SIZE)  # 窗口尺寸
    window.rowconfigure(1, weight=1)
    window.columnconfigure(0, weight=1)
    window.resizable(True, True)  # 规定窗口可缩放

    # 路径区块
    basicset = tk.LabelFrame(window, text = "基础设置", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    basicset.columnconfigure(4, weight=1)
    basicset.grid(row = 0, sticky=tk.EW)
    bt1 = tk.Button(basicset, text='源文件目录', fg='black', width=13, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=open_source).grid(row=1, column = 1)
    stext = tk.Entry(basicset, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black', state='readonly')
    stext.grid(row=1, column=2, sticky=tk.EW, columnspan=5)
    
    bt2 = tk.Button(basicset, text='输出文件到', fg='black', width=13, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=open_target).grid(row=2, column = 1)
    ttext = tk.Entry(basicset, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black', state='readonly')
    ttext.grid(row=2, column=2, sticky=tk.EW, columnspan=5)

    lbinfilter = tk.Label(basicset, text="筛选文件类型: ", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    lbinfilter.grid(row=3, column = 1)
    infilter_wav = tk.IntVar()
    infilter_mp3 = tk.IntVar()
    cbinwav = tk.Checkbutton(basicset, variable = infilter_wav, onvalue = 1, offvalue = 0, text="WAV", font=('TkDefaultFont',UI_FONT_SIZE_Checkbutton), fg='black', command=show_infilter)
    # tk.Radiobutton(basicset, text='wav', variable = infilter, value='wav', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "处理WAV文件\n"))
    cbinwav.grid(row=3, column = 2)
    cbinmp3 = tk.Checkbutton(basicset, variable = infilter_mp3, onvalue = 1, offvalue = 0, text='MP3', font=('TkDefaultFont',UI_FONT_SIZE_Checkbutton), fg='black', command=show_infilter)
    cbinmp3.grid(row=3, column = 3)
    # cbhd = tk.Radiobutton(basicset, text='HDSource-newtitle', variable = infilter, value='hd', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "设置计算模式为hd\n"))
    # cbhd.grid(row=0, column = 3)
    infilter_wav.set(1)
    infilter_mp3.set(1)
    # update_text(text1, "设置计算模式为普通\n")

    # watermark set
    wmkframe = tk.LabelFrame(window, text = "水印设置", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    wmkframe.columnconfigure(5, weight=1)
    wmkframe.grid(row = 1, sticky=tk.EW)
    btopenwmk = tk.Button(wmkframe, text='打开水印文件', fg='black', width=13, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=open_wmk).grid(row=0, column = 1)
    wmktext = tk.Entry(wmkframe, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black', state='readonly')
    wmktext.grid(row=0, column=2, sticky=tk.EW, columnspan=5)
    # manual set start
    l1 = tk.Label(wmkframe, text="水印起始位置: ", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l1.grid(row=1, column = 1, sticky=tk.W)
    starttime = tk.IntVar()
    starttime.set(0)
    enstarttime = tk.Entry(wmkframe, textvariable = starttime, width=5, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    enstarttime.grid(row=1, column = 2, sticky=tk.EW)
    l2 = tk.Label(wmkframe, text="秒   水印间隔: ", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l2.grid(row=1, column = 3)
    pausetime = tk.IntVar()
    pausetime.set(30)
    enpausetime = tk.Entry(wmkframe, textvariable = pausetime, width=5, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    enpausetime.grid(row=1, column = 4, sticky=tk.EW)
    l3 = tk.Label(wmkframe, text="秒", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l3.grid(row=1, column = 5, sticky=tk.W)
    # set volume
    l3 = tk.Label(wmkframe, text="水印音量调整: -", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l3.grid(row=2, column = 1, sticky=tk.W)
    wmkvol = tk.IntVar()
    wmkvol.set(6)
    enwmkvol = tk.Entry(wmkframe, textvariable = wmkvol, width=5, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    enwmkvol.grid(row=2, column = 2, sticky=tk.EW)
    l4 = tk.Label(wmkframe, text="dB", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l4.grid(row=2, column = 3, sticky=tk.W)

    # output setting
    outputframe = tk.LabelFrame(window, text = "输出设置", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    outputframe.columnconfigure(6, weight=1)
    outputframe.grid(row = 2, sticky=tk.EW)

    l5 = tk.Label(outputframe, text="输出文件格式：", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l5.grid(row=0, column = 1, sticky=tk.W)
    outfilter = tk.StringVar()
    cboutwav = tk.Radiobutton(outputframe, text='WAV', variable = outfilter, value='wav', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "输出为WAV\n"))
    cboutwav.grid(row=0, column = 2)
    cboutmp3 = tk.Radiobutton(outputframe, text='MP3', variable = outfilter, value='mp3', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "输出为MP3\n"))
    cboutmp3.grid(row=0, column = 3)
    outfilter.set('mp3')
    # set quality
    # l6 = tk.Label(outputframe, text="输出文件质量：", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    # l6.grid(row=0, column = 4, sticky=tk.W)
    # wmkqlt = tk.IntVar()
    # wmkqlt.set(128)
    # enwmkqlt = tk.Entry(outputframe, textvariable = wmkqlt, width=5, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    # enwmkqlt.grid(row=0, column = 5, sticky=tk.W)
    # l7 = tk.Label(outputframe, text="kbps", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    # l7.grid(row=0, column = 6, sticky=tk.W)
    # set out filename
    l8 = tk.Label(outputframe, text="文件名前缀：", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l8.grid(row=1, column = 1, sticky=tk.W)
    outfileprefx = tk.StringVar()
    outfileprefx.set('DEMO')
    enoutfileprefx = tk.Entry(outputframe, textvariable = outfileprefx, width=20, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    enoutfileprefx.grid(row=1, column = 2, columnspan=5, sticky=tk.W)
    # set metadata
    

    # Caculate Button
    calcframe = tk.LabelFrame(window, text = "", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    calcframe.columnconfigure(4, weight=1)
    calcframe.grid(row = 3, sticky=tk.EW)
    btconvert = tk.Button(calcframe, text='开始转换', fg='black', width=12, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=lambda :thread_it(call_convert), state='disabled')
    btconvert.grid(row=0, column = 3, rowspan=2)
    btexit = tk.Button(calcframe,  text='退出程序', fg='black', width=12, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=closewindow)
    btexit.grid(row=0, column = 4, rowspan=2)

    # output text
    outframe = tk.LabelFrame(window, text = "运行日志", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    text1 = scrolledtext.ScrolledText(outframe, width=60, height=12, font=('TkDefaultFont',UI_FONT_SIZE_ScrolledText), fg='black', bg='orange', state='disabled')
    text1.pack()
    outframe.grid(row=5, sticky=tk.W)

    window.mainloop()

# 创建线程调用 防止在长时间计算时图形界面卡死导致程序崩溃
def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()

def update_entry(wichentry, input_text):
    print('updating entry: ', input_text)
    wichentry.config(state='normal')
    wichentry.delete(0, END)
    wichentry.insert(0, input_text)
    wichentry.update()
    wichentry.config(state='readonly')

def update_text(wichtext, input_text):
    print('updating text: ', input_text)
    wichtext.config(state='normal')
    wichtext.insert(END, input_text)
    wichtext.update()
    wichtext.config(state='disabled')
    wichtext.see(END)


if __name__ == "__main__":
    # 根据不同平台设置UI参数
    if system().lower() == 'darwin':
        SYSARCH = 'mac'
        UI_WINDOW_SIZE = '600x700'
        UI_FONT_SIZE_LabelFrame = 14
        UI_FONT_SIZE_Label = 16
        UI_FONT_SIZE_Entry = 16
        UI_FONT_SIZE_Radiobutton = 16
        UI_FONT_SIZE_Checkbutton = 16
        UI_FONT_SIZE_Button = 14
        UI_FONT_SIZE_ScrolledText = 20
    elif system().lower() == 'windows':
        SYSARCH = 'win'
        UI_WINDOW_SIZE = '600x750'
        UI_FONT_SIZE_LabelFrame = 10
        UI_FONT_SIZE_Label = 12
        UI_FONT_SIZE_Entry = 12
        UI_FONT_SIZE_Radiobutton = 12
        UI_FONT_SIZE_Checkbutton = 12
        UI_FONT_SIZE_Button = 10
        UI_FONT_SIZE_ScrolledText = 16
    initgui()

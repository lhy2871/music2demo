from pydub import AudioSegment
import os
import threading
import tkinter as tk
import traceback
from platform import system
from tkinter import filedialog, scrolledtext, END
from tkinter.messagebox import askyesno
from time import sleep, strftime, localtime

class Musicdir:
    def __init__(self):
        self.inpath=''
        self.outpath=''
        self.wmkpath=''
        self.music_num=0
        self.music_done=0
        self.musiclist={}
        self.curet_music = None
        self.wmk=None
        self.convrted = 0
    
    def readmusicdir(self, wav=1, mp3=1):
        if wav == 1 and mp3 == 1:
            for files in os.listdir(self.inpath):
                if files.endswith(('.wav','.mp3','.WAV','.MP3')):
                    self.musiclist[files] = 0
                    self.music_num = self.music_num + 1
        elif wav == 1 and mp3 == 0:
            for files in os.listdir(self.inpath):
                if files.endswith(('.wav','.WAV')):
                    self.musiclist[files] = 0
                    self.music_num = self.music_num + 1
        elif mp3 == 1 and wav == 0:
            for files in os.listdir(self.inpath):
                if files.endswith(('.mp3','.MP3')):
                    self.musiclist[files] = 0
                    self.music_num = self.music_num + 1
        else:
            pass

    def readwmk(self):
        if self.wmkpath.endswith(('mp3','MP3')):
            self.wmk = AudioSegment.from_mp3(self.wmkpath)
        elif self.wmkpath.endswith(('wav','WAV')):
            self.wmk = AudioSegment.from_wav(self.wmkpath)

def initgui():

    def closewindow():
        ans = askyesno(title="退出确认窗口", message="真的要退出程序吗?")
        if ans:
            update_text(text1, "\n用户退出")
            if musicdir.convrted == 1:
                with open(os.path.join(musicdir.outpath,os.path.basename(musicdir.inpath)+'_addwmk_log.txt'), 'a') as f:
                    f.write(strftime("%Y-%m-%d %H:%M:%S", localtime())+'\n\n')
                    f.write(text1.get(1.0,END) + '\n')
                    f.close()

            sleep(1)
            window.destroy()
        else: return

    def open_source():
        try:
            musicdir.inpath = filedialog.askdirectory(title=u'选择源文件目录')
            if musicdir.inpath != '':
                update_entry(stext, musicdir.inpath)
                update_text(text1, '已打开源文件夹: '+musicdir.inpath)
            else:
                update_entry(stext, '源文件夹打开失败')
                update_text(text1, '源文件夹打开失败')
                return

            if musicdir.inpath != '' and musicdir.outpath != '' and musicdir.wmkpath != '':
                btconvert.config(state='normal')
        except:
            traceback.print_exc()
            update_entry(stext, musicdir.inpath)
            update_text(text1, '源文件夹读取失败')

    def open_target():
        try:
            musicdir.outpath = filedialog.askdirectory(title=u'选择目标文件目录')
            if musicdir.outpath != '':
                update_entry(ttext, musicdir.outpath)
                update_text(text1, '已设置输出文件夹: '+musicdir.outpath)
            else:
                update_entry(ttext, '输出文件夹打开失败')
                update_text(text1, '输出文件夹打开失败')
                return

            if musicdir.inpath != '' and musicdir.outpath != '' and musicdir.wmkpath != '':
                btconvert.config(state='normal')
        except:
            traceback.print_exc()
            update_entry(ttext, musicdir.outpath)
            update_text(text1, '输出文件夹打开失败')

    def open_wmk():
        musicdir.wmkpath = filedialog.askopenfilename(title=u'选择水印文件')
        if musicdir.wmkpath != '':
            if musicdir.wmkpath.endswith(('.wav','.mp3','.WAV','.MP3')):
                musicdir.readwmk()
                if musicdir.wmk != None:
                    update_entry(wmktext, musicdir.wmkpath)
                    update_text(text1, '成功读取水印文件: '+os.path.basename(musicdir.wmkpath))
                    if musicdir.inpath != '' and musicdir.outpath != '' and musicdir.wmkpath != '':
                            btconvert.config(state='normal')
        else:
            update_entry(wmktext, '源文件打开失败')
            update_text(text1, '源文件打开失败\n')
            return

    def call_convert():
        musicdir.music_done = 0
        wmk = musicdir.wmk+AudioSegment.silent(int(pausetime.get())*1000)
        wmk.apply_gain((0-int(wmkvol.get())))
        num_inc = 1

        # read files
        if infilter_wav.get() == 0 and infilter_mp3.get() == 0:
            update_text(text1, '未选择要处理的文件类型')
            return

        musicdir.readmusicdir(int(infilter_wav.get()),int(infilter_mp3.get()))
        update_text(text1, '共有 '+str(musicdir.music_num)+' 个音频文件')
        # update_text(text1, str(musicdir.musiclist))
        mlist = sorted(musicdir.musiclist)
        for m in mlist:
            update_text(text1, m)

        # Process
        for key in musicdir.musiclist:
            update_text(text1, '正在处理['+str(musicdir.music_done+1)+'/'+str(musicdir.music_num)+']: '+key+' as: '+outfileprefx.get()+'_'+str(num_inc)+'.'+outfilter.get())
            try:
                if key.endswith(('.mp3','.MP3')):
                    musicdir.curet_music = AudioSegment.from_mp3(os.path.join(musicdir.inpath,key))
                elif key.endswith(('.wav','.WAV')):
                    musicdir.curet_music = AudioSegment.from_wav(os.path.join(musicdir.inpath,key))
                demo = musicdir.curet_music.overlay(wmk, position=float(starttime.get())*1000, loop=True)

                if outfilter.get() == 'mp3':
                    outfile = os.path.join(musicdir.outpath, outfileprefx.get()+'_'+str(num_inc)+'.mp3')
                    demo.export(outfile, format='mp3')
                elif outfilter.get() == 'wav':
                    outfile = os.path.join(musicdir.outpath, outfileprefx.get()+'_'+str(num_inc)+'.wav')
                    demo.export(outfile, format='wav')

                musicdir.musiclist[key] = 1
                musicdir.music_done = musicdir.music_done + 1
                num_inc = num_inc+1

            except:
                pass
        
        musicdir.convrted =1

        if musicdir.music_done >= musicdir.music_num:
            update_text(text1, '\n所有文件处理完成')
        else:
            update_text(text1, '\n处理失败的文件:')
            for key in musicdir.musiclist:
                if musicdir.musiclist[key] == 0:
                    update_text(text1, key)


    # ft1 = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
    # 构建图形界面
    window = tk.Tk()
    #设置程序缩放
    window.protocol('WM_DELETE_WINDOW', closewindow)
    window.title('音频DEMO处理工具  v1.0\t\tby Hanyuan6')  # 标题
    window.geometry(UI_WINDOW_SIZE)  # 窗口尺寸
    window.rowconfigure(1, weight=1)
    window.columnconfigure(0, weight=1)
    window.resizable(True, True)  # 规定窗口可缩放

    # 路径区块
    basicset = tk.LabelFrame(window, text = "基础设置", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    basicset.columnconfigure(6, weight=1)
    basicset.grid(row = 0, sticky=tk.EW)
    bt1 = tk.Button(basicset, text='源文件目录', fg='black', width=13, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=open_source).grid(row=1, column = 1)
    stext = tk.Entry(basicset, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black', state='readonly')
    stext.grid(row=1, column=2, sticky=tk.EW, columnspan=5)
    
    bt2 = tk.Button(basicset, text='输出文件到', fg='black', width=13, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=open_target).grid(row=2, column = 1)
    ttext = tk.Entry(basicset, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black', state='readonly')
    ttext.grid(row=2, column=2, sticky=tk.EW, columnspan=5)

    lbinfilter = tk.Label(basicset, text="要处理的文件类型: ", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    lbinfilter.grid(row=3, column = 1, columnspan=2)
    infilter_wav = tk.IntVar()
    infilter_mp3 = tk.IntVar()
    cbinwav = tk.Checkbutton(basicset, variable = infilter_wav, onvalue = 1, offvalue = 0, text="WAV", font=('TkDefaultFont',UI_FONT_SIZE_Checkbutton), fg='black')
    # tk.Radiobutton(basicset, text='wav', variable = infilter, value='wav', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "处理WAV文件\n"))
    cbinwav.grid(row=3, column = 3)
    cbinmp3 = tk.Checkbutton(basicset, variable = infilter_mp3, onvalue = 1, offvalue = 0, text='MP3', font=('TkDefaultFont',UI_FONT_SIZE_Checkbutton), fg='black')
    cbinmp3.grid(row=3, column = 4)
    # cbhd = tk.Radiobutton(basicset, text='HDSource-newtitle', variable = infilter, value='hd', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "设置计算模式为hd\n"))
    # cbhd.grid(row=0, column = 3)
    infilter_wav.set(1)
    infilter_mp3.set(1)

    # watermark set
    wmkframe = tk.LabelFrame(window, text = "水印设置", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    wmkframe.columnconfigure(8, weight=1)
    wmkframe.grid(row = 1, sticky=tk.EW)
    btopenwmk = tk.Button(wmkframe, text='打开水印文件', fg='black', width=13, height=2, font=('TkDefaultFont',UI_FONT_SIZE_Button), command=open_wmk).grid(row=0, column = 1)
    wmktext = tk.Entry(wmkframe, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black', state='readonly')
    wmktext.grid(row=0, column=2, sticky=tk.EW, columnspan=7)
    # manual set start
    l1 = tk.Label(wmkframe, text="水印起始位置: ", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l1.grid(row=1, column = 1, sticky=tk.W, columnspan=2)
    starttime = tk.IntVar()
    starttime.set(7.5)
    enstarttime = tk.Entry(wmkframe, textvariable = starttime, width=5, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    enstarttime.grid(row=1, column = 3, sticky=tk.EW)
    l2 = tk.Label(wmkframe, text="秒   水印间隔: ", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l2.grid(row=1, column = 4)
    pausetime = tk.IntVar()
    pausetime.set(5)
    enpausetime = tk.Entry(wmkframe, textvariable = pausetime, width=5, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    enpausetime.grid(row=1, column = 5, sticky=tk.EW)
    l3 = tk.Label(wmkframe, text="秒", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l3.grid(row=1, column = 6, sticky=tk.W)
    # set volume
    l3 = tk.Label(wmkframe, text="水印音量调整: -", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l3.grid(row=2, column = 1, sticky=tk.W, columnspan=2)
    wmkvol = tk.IntVar()
    wmkvol.set(6)
    enwmkvol = tk.Entry(wmkframe, textvariable = wmkvol, width=5, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black')
    enwmkvol.grid(row=2, column = 3, sticky=tk.EW)
    l4 = tk.Label(wmkframe, text="dB", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l4.grid(row=2, column = 4, sticky=tk.W)

    # output setting
    outputframe = tk.LabelFrame(window, text = "输出设置", fg='black', font=('TkDefaultFont',UI_FONT_SIZE_LabelFrame))
    outputframe.columnconfigure(6, weight=1)
    outputframe.grid(row = 2, sticky=tk.EW)

    l5 = tk.Label(outputframe, text="输出文件格式：", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l5.grid(row=0, column = 1, sticky=tk.W)
    outfilter = tk.StringVar()
    cboutwav = tk.Radiobutton(outputframe, text='WAV', variable = outfilter, value='wav', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "输出为WAV"))
    cboutwav.grid(row=0, column = 2)
    cboutmp3 = tk.Radiobutton(outputframe, text='MP3', variable = outfilter, value='mp3', font=('TkDefaultFont',UI_FONT_SIZE_Radiobutton), fg='black', command=lambda :update_text(text1, "输出为MP3"))
    cboutmp3.grid(row=0, column = 3)
    outfilter.set('mp3')

    l8 = tk.Label(outputframe, text="文件名前缀：", font=('TkDefaultFont',UI_FONT_SIZE_Label), fg='black')
    l8.grid(row=1, column = 1, sticky=tk.W)
    outfileprefx = tk.StringVar()
    outfileprefx.set('DEMO')
    enoutfileprefx = tk.Entry(outputframe, textvariable = outfileprefx, width=20, font=('TkDefaultFont',UI_FONT_SIZE_Entry), fg='black', bg='white')
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
    text1 = scrolledtext.ScrolledText(outframe, width=60, height=16, font=('TkDefaultFont',UI_FONT_SIZE_ScrolledText), fg='black', bg='orange', state='disabled')
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
    wichtext.insert(END, input_text+'\n')
    wichtext.update()
    wichtext.config(state='disabled')
    wichtext.see(END)


if __name__ == "__main__":
    # 根据不同平台设置UI参数
    if system().lower() == 'darwin':
        SYSARCH = 'mac'
        UI_WINDOW_SIZE = '600x800'
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
    
    musicdir = Musicdir()
    initgui()

"""
用tkinter内置标准库制作一个记事本程序
"""
import tkinter as tk#实现菜单栏和工具栏,主要引入tkinter的全局属性，如tk.SEL_FIRST,tk.SEL_LAST等
from tkinter import scrolledtext#实现滚动文本框(自带滚动条)
import fileinput#fileinput模块可以对一个或多个文件中的内容进行迭代、遍历等操作。该模块的input()函数有点类似文件
from tkinter import filedialog#创建标准的打开文件对话框
import os#判断文件路径是否存在
from tkinter import messagebox#实现对话框效果(消息框和用户输入框)
from tkinter import simpledialog#在窗体中创建输入对话框，用于查找字符串
from tkinter import colorchooser#创建颜色选择对话框
from tkinter import Scrollbar#创建滚动条
from tkinter import Listbox#创建列表框,并与滚动条绑定
from tkinter import StringVar
from tkinter import LabelFrame#LabelFrame组件是Frame组件的变体。默认情况下,LabelFrame会在其子组件周围绘制一个边框和一个标题
from tkinter import Label#LabelFrame内的标签
from tkinter import Button
from tkinter import font#设置字体
class editor():#记事本类
    def __init__(self,rt):#构造函数用来实例化窗体对象
        if rt == None:#第一次启动程序时,执行if语句，创建根窗口(其实根窗口主窗口本身就是一个Toplevel)
          self.t = tk.Tk()
        self.t.title("文本编辑器")
        
        self.frm_file=tk.Frame(self.t,bg='gray')#实例化一个Frame，Frame就是屏幕上的一块矩形区域，多是用来作为容器（container）来布局窗体，内容比较少。
        self.frm_file.grid(row =0,column =0,padx =0,sticky = 'w')#设置功能左栏，即菜单栏和文本输入框中间那一栏，以下组件都将设置到工具内
        
        self.btn_open=tk.Button(self.frm_file,text="打开",relief='groove',command=self.openfile)#relief设置按钮边框样式，默认raised
        self.btn_open.pack(side='left',padx=5,fill='both',expand=1)
        
        self.btn_new=tk.Button(self.frm_file,text="新建",relief='groove',command=self.neweditor)
        self.btn_new.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_save=tk.Button(self.frm_file,text='保存',relief='groove',command=self.savefile)
        self.btn_save.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_saveas=tk.Button(self.frm_file,text='另存为',relief='groove',command=self.saveasfile)
        self.btn_saveas.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_exit=tk.Button(self.frm_file,text='退出',relief='groove',command=self.die)
        self.btn_exit.pack(side='left',padx=5,fill='both',expand=1)

        self.frm_edit = tk.Frame(self.t,bg='gray')#实例化一个Frame,设置背景颜色，同上
        self.frm_edit.grid(row =0,column =1,padx =1,sticky = 'w')#设置功能右栏
        
        self.btn_copy = tk.Button(self.frm_edit,text = "复制",command=self.copy)
        self.btn_copy.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_cut = tk.Button(self.frm_edit,text = "剪切",command=self.cut)
        self.btn_cut.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_paste = tk.Button(self.frm_edit,text = "粘贴",command=self.paste)
        self.btn_paste.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_find = tk.Button(self.frm_edit,text = "查询(未实现)",command=self.find_char)
        self.btn_find.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_allselect = tk.Button(self.frm_edit,text = "全选",command=self.select_char_all)
        self.btn_allselect.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_font = tk.Button(self.frm_edit,text = "字体样式",command=self.font_it)
        self.btn_font.pack(side='left',padx=5,fill='both',expand=1)

        self.btn_color = tk.Button(self.frm_edit,text = "字体颜色",command=self.color_it)
        self.btn_color.pack(side='left',padx=5,fill='both',expand=1)
        
        #至此完成工具栏的UI界面,下面完成菜单栏的UI界面
        
        self.bar=tk.Menu(self.t)#实例化菜单栏
        
        self.filem=tk.Menu(self.bar)#实例化名为"文件"的菜单
        
        self.filem.add_separator()#菜单项分割线
        
        self.filem.add_command(label="新建",command=self.neweditor,accelerator="     Ctr+N")#菜单添加菜单项，并绑定按键事件，下同
        self.filem.bind_all("<Control-n>",self.neweditor)#同时绑定快捷键事件,下同

        self.filem.add_command(label="打开",command=self.openfile,accelerator="     Ctr+O")
        self.filem.bind_all("<Control-s>",self.savefile)

        self.filem.add_command(label="保存",command=self.savefile,accelerator="     Ctr+S")
        self.filem.bind_all("<Control-s>",self.savefile)

        self.filem.add_command(label = "另存为",command = self.saveasfile,accelerator = "     Ctr + Shif + S ")
        self.filem.bind_all("<Control-Shift-KeyPress-S>",self.saveasfile)

        self.filem.add_command(label = "关闭",command = self.close,accelerator = "     F4")
        self.filem.bind_all("<F4>",self.close)

        self.filem.add_separator()#菜单项分割线

        self.filem.add_command(label="退出",command=self.die,accelerator="     ESC")
        self.filem.bind_all("<Escape>",self.die)
        
        self.bar.add_cascade(label = "文件",menu = self.filem)#将'文件'菜单self.filem绑定到菜单栏self.bar，下同

        
        self.editm=tk.Menu(self.bar)#实例化名为"编辑"的菜单

        self.editm.add_separator()

        self.editm.add_command(label = "复制",command = self.copy,accelerator = " "*10 + "Ctr + C")
        self.editm.bind_all("<Control-c>",self.copy)
        self.editm.add_separator()

        self.editm.add_command(label = "黏贴",command = self.paste,accelerator = " "*10 + "Ctr + V")
        self.editm.bind_all("<Control-v>",self.paste)
        self.editm.add_separator()

        self.editm.add_command(label = "剪切",command = self.cut,accelerator = " "*10 + "Ctr + X")
        self.editm.bind_all("<Control-x>",self.cut)
        self.editm.add_separator()

        self.editm.add_command(label = "删除",command = self.delete_text,accelerator = " "*10 + "Delete")
        self.editm.bind_all("<Delete>",self.delete_text)
        self.editm.add_separator()

        self.editm.add_command(label = "查找(未实现)",command = self.find_char,accelerator = " "*10 + "Ctr +F")
        self.editm.bind_all("<Control-f>",self.find_char)
        self.editm.add_separator()

        self.editm.add_command(label = "全选",command = self.select_char_all,accelerator = " "*10 + "Ctr + A")
        self.editm.bind_all("<Control-a>",self.select_char_all)
        
        self.bar.add_cascade(label = "编辑",menu = self.editm)#将'编辑'菜单self.editm绑定到菜单栏self.bar


        self.formm = tk.Menu(self.bar)#实例化名为"格式"的菜单

        self.formm.add_command(label = "字体颜色",command = self.color_it,accelerator = " "*10 + "Alt + C")
        self.formm.bind_all("<Alt-f>",self.color_it)
        self.formm.add_separator()

        self.formm.add_command(label = "字体格式",command = self.font_it,accelerator = " "*10 + "Alt + F")
        self.formm.bind_all("<Alt-f>",self.font_it)
    
        self.bar.add_cascade(label = "格式",menu = self.formm)#将'格式'菜单self.formm绑定到菜单栏self.bar


        self.helpm = tk.Menu(self.bar)#实例化名为"帮助"的菜单
        self.helpm.add_command(label = "关于",command = self.about)
        self.bar.add_cascade(label = "帮助",menu = self.helpm)#将'帮助'菜单self.helpm绑定到菜单栏self.bar
        
        self.t.config(menu = self.bar)#在创建菜单控件时,需要使用创建主窗口的方法config()将菜单添加到窗口。

        #至此,工具栏的UI界面和菜单栏的UI界面已完成,接下来完成滚动文本框

        self.st=scrolledtext.ScrolledText(self.t)
        self.st.grid(row=1,column=0,columnspan=3,pady=3)

        #至此，所有GUI完成，下面完成事件处理函数
        
    def openfile(self,event =None):#此处涉及创建打开/保存文件对话框知识
        oname=tk.filedialog.askopenfilename(filetypes=[("打开文件","*.txt")])#返回一个文件路径的字符串对象
        print(oname)#控制台打印
        if oname:
            self.st.delete(1.0, "end") # 使用 delete
            for line in fileinput.input(oname):
                self.st.insert("end",line)
            self.t.title(oname)#主窗体标题改变为打开的文件路径
    def neweditor(self,event=None):
        global root
        win_list.append(editor(root))
    def savefile(self,event=None):
        if os.path.isfile(self.t.title()):#获取打开文件的路径，此处是打开一个文本文件修改后进行保存
            opf=open(self.t.title(),"w")
            opf.write(self.st.get(1.0,"end"))#获取滚动文本框的内容
            opf.flush()#把缓冲区内容写入硬盘
            opf.close()
            messagebox.showinfo("保存消息框","保存成功!")
        else:#此处是在记事本程序中没有打开任何文件，之间在记事本程序中编写文本然后保存，需要指定保存路径,默认文本文件保存在当前程序运行路径，，可自己在文件对话框修改
            sname=tk.filedialog.asksaveasfilename(title = '保存',initialdir=os.getcwd(),initialfile = '新建文本.txt',filetypes=[("打开文件","*.txt")])
            if sname:
                ofp=open(sname,"w")
                ofp.write(self.st.get(1.0,"end"))
                ofp.flush()
                ofp.close()
            self.t.title(sname)
            messagebox.showinfo("保存消息框","保存成功!")
    def saveasfile(self,event=None):
        sname=tk.filedialog.asksaveasfilename(title="另存为",filetypes=[("保存文件","*.txt")],defaultextension = ".txt")
        if sname:
            ofp=open(sname,"w")
            ofp.write(self.st.get(1.0,"end"))
            ofp.flush()
            ofp.close()
            self.t.title(sname)
    def close(self,event=None):
        self.t.destroy()
    def die(self,event=None):
        self.t.destroy()
    def copy(self,event=None):
        text = self.st.get(tk.SEL_FIRST,tk.SEL_LAST)
        self.st.clipboard_clear()#每次复制之前,清空之前复制到Tk剪切板的内容
        self.st.clipboard_append(text)#将字符串追加到Tk剪贴板。
    def paste(self,event=None):
        try:
            text = self.st.selection_get(selection = "CLIPBOARD")#返回当前选择的内容,关键字参数selection指定数据的获取形式，此处为CLIPBOARD(剪切板),默认为STRING
            self.st.insert(tk.INSERT,text)#滚动文本框内容插入的方式为鼠标光标位置
        except tk.TclError:#经测试，发现粘贴操作经常出现TclError异常，此时考虑程序的健壮性,使用异常捕获语句
            pass
    #剪切：将图片或文字选中后，通过Ctrl＋X命令，将图片或文字裁切下来，放到电脑剪切版(一块内存动态空间)上，再通过Ctrl+V粘贴到所要粘贴的位置，剪切操作后原来的地方就没有那个信息了，裁切文字的过程称为剪切。
    def cut(self,event=None):
        text=self.st.get(tk.SEL_FIRST,tk.SEL_LAST)#选中文本
        self.st.delete(tk.SEL_FIRST,tk.SEL_LAST)#删除所选中得文本
        self.st.clipboard_clear()#清空之前存在剪切板的内容
        self.st.clipboard_append(text)#将选择的文本加入剪切板,接下来进行复制操作即可
    def delete_text(self,event=None):
        try:
            self.st.delete(tk.SEL_FIRST,tk.SEL_LAST)
        except tk.TclError:
            pass
    def find_char(self,event=None):
        target=simpledialog.askstring("Search Dialog","寻找字符串",initialvalue="请输入要查询的字符")#输入对话框标题，提示字符，设置初始化文本
        end = self.st.index(tk.END)#返回表单行中的索引,即滚动文本框中有几行文本,返回类似"4.0"字样的str类型对象
        print(type(end))#<class 'str'>
        print(end)
        endindex = end.split(".")#通过指定分隔符对字符串进行切片,返回列表对象,列表的元素类型为字符串
        print(endindex)
        end_line = int(endindex[0])
        end_column = int(endindex[1])
        pos_line =1
        pos_column=0
        length =len(target)#要查询字符串的字符数
        pass
    def select_char_all(self,event=None):
        self.st.tag_add(tk.SEL,1.0,tk.END)
        self.st.see(tk.INSERT)
        self.st.focus()
    def color_it(self,event=None):
        color=colorchooser.askcolor(title = 'Python')
        self.st["foreground"] = color[1]
    def font_it(self,event=None):
        self.t_font=tk.Toplevel()#创建一个顶层窗口
        self.t_font.title("字体选择面板")
        self.label_size=tk.Label(self.t_font,text="字体大小")
        self.label_size.grid(row = 0 ,column =0,padx =30)
        self.label_font=tk.Label(self.t_font,text = "字体类型")
        self.label_font.grid(row = 0,column =2,padx =30)
        self.label_shape=tk.Label(self.t_font,text = "字体形状")
        self.label_shape.grid(row = 0,column =4,padx =30)
        self.label_weight=tk.Label(self.t_font,text = "字体粗细")
        self.label_weight.grid(row =0,column = 6,padx =30)
        #创建以上四列属性的滚动条
        self.scroll_size = Scrollbar(self.t_font)
        self.scroll_size.grid(row=1,column=1,stick="ns")
        self.label_font = Scrollbar(self.t_font)
        self.label_font.grid(row=1,column=3,stick="ns")
        self.label_shape = Scrollbar(self.t_font)
        self.label_shape.grid(row=1,column=5,stick="ns")
        self.label_weight = Scrollbar(self.t_font)
        self.label_weight.grid(row=1,column=7,stick="ns")
        #创建字符串追踪变量
        list_var_font=StringVar()
        list_var_size=StringVar()
        list_var_shape=StringVar()
        list_var_weight=StringVar()
        #创建"字体类型"列表框控件
        self.list_font=Listbox(self.t_font,selectmode="browse",listvariable=list_var_font,exportselection=0)
        #selectmode=BROWSE表示单选，但可拖动鼠标或方向键直接修改
        #exportselection=0(False)表示选中的项目文本是否可以被复制到剪切板,此时表示不允许复制项目文本
        #listvariable指向一个StringVar类型的变量，该变量存放Listbox中所有的项目文本
        self.list_font.grid(row=1,column=2,padx=4)
        list_font_item=["\"Arial\"","\"Arial Baltic\"","\"Arial Black\"","\"Arial CE\"","\"Arial CYR\"","\"Arial Greek\"","\"Arial Narrow\"",
             "\"Arial TUR\"","\"Baiduan Number\"","\"Batang,BatangChe\""]
        for item in list_font_item:
            self.list_font.insert(0,item)
        
        self.list_font.bind("<ButtonRelease-1>",self.change_font)#ButtonRelease-1表示鼠标左键释放,调用change_font()事件处理函数
        #创建"字体大小"列表框控件
        self.list_size=Listbox(self.t_font,selectmode="browse",listvariable=list_var_size,exportselection=0)
        self.list_size.grid(row=1,column=0,padx=4)
        list_size_item=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        for item in list_size_item:
            self.list_size.insert(0,item)
        self.list_size.bind("<ButtonRelease-1>",self.change_size)
        #创建"字体形状"列表框
        self.list_shape=Listbox(self.t_font,selectmode="browse",listvariable=list_var_shape,exportselection=0)
        self.list_shape.grid(row=1,column=4,padx=4)
        list_shape_item=["italic","roman"]#斜体字，罗马字
        for item in list_shape_item:
            self.list_shape.insert(0,item)
        self.list_shape.bind("<ButtonRelease-1>",self.change_shape)
        #创建"字体粗细"列表框
        self.list_weight=Listbox(self.t_font,selectmode="browse",listvariable=list_var_weight,exportselection=0)
        self.list_weight.grid(row=1,column=6,padx=4)
        list_weight_item=["bold","normal"]
        for item in list_weight_item:
            self.list_weight.insert(0,item)
        self.list_weight.bind("<ButtonRelease-1>",self.change_weight)
        #创建字体样式演示标签
        self.font_display=LabelFrame(self.t_font,text="字体样式演示区域")
        self.font_display.grid(row=2,column=0,pady=4)
        self.lab_display=Label(self.font_display,text = "我在这里")
        self.lab_display.pack()
        #创建"字体选择面板窗口"的确定和取消按钮
        self.btn_ok=Button(self.t_font,text="确定",width=8,height=2,command=self.change)
        self.btn_ok.grid(row=2,column=2,pady=4)
        self.btn_cancel=Button(self.t_font,text="取消",width=8,height=2,command=self.exit_subwindow)
        self.btn_cancel.grid(row=2,column=4,pady=4)
    def change_font(self,event):
        tk.customFont = font.Font(family = "Helvetica",size = 12,weight = "normal",slant = "roman",underline =0)
        family = tk.customFont["family"]
        tk.customFont.configure(family =self.list_font.get(self.list_font.curselection()))
        self.st.config(font = tk.customFont)
        self.font_count = 1
    def change_size(self,event):
        tk.customFont = font.Font(family = "Helvetica",size = 12,weight = "normal",slant = "roman",underline =0)
        size = tk.customFont["size"]
        tk.customFont.configure(size =self.list_size.get(self.list_size.curselection()))
        self.st.config(font = tk.customFont)
        self.size_count = 1
        
    def change_shape(self,event):
        tk.customFont = font.Font(family = "Helvetica",size = 12,weight = "normal",slant = "roman",underline =0)
        slant = tk.customFont["slant"]
        tk.customFont.configure(slant =self.list_shape.get(self.list_shape.curselection()))
        self.st.config(font = tk.customFont)
        self.shape_count =1
    def change_weight(self,event):
        tk.customFont = font.Font(family = "Helvetica",size = 12,weight = "normal",slant = "roman",underline =0)
        weight = tk.customFont["weight"]
        tk.customFont.configure(weight =self.list_weight.get(self.list_weight.curselection()))
        self.st.config(font = tk.customFont)
        self.shape_count =1
    def change(self):#注意:Button绑定的事件处理函数不需要event参数,此处为滚动文本框self.st对象动态增加font属性
        self.st["font"]=(self.list_size.get(self.list_size.curselection()))
        self.st["font"]=(self.list_font.get(self.list_font.curselection()))
        self.st["font"]=(self.list_shape.get(self.list_shape.curselection()))
    def exit_subwindow(self):#同上
        self.t_font.destroy()
    def about(self,event=None):
        tk.messagebox.showinfo(title="当前版本为1.0",message="作者:大哥\n状态:继续努力ing")
if __name__=="__main__":
    win_list=[]
    root=None
    editor(root).t.mainloop()#mainloop()只能存在Tk类中，所以是editor类实例属性调用
    


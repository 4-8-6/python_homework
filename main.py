import tkinter as tk
from tkinter import  Checkbutton
import tkinter.messagebox
import requests
import torch
import json

import train
from request import crawler
import os
from train import Train,resize
from model import Model  #用于加载模型
from PIL import Image
app = tk.Tk() #根窗口的实例(root窗口)
app.geometry("300x450")
app.title('张溯_201930345012') #根窗口标题

#final_dict={'cat':'野猫','cup':'水杯','ship':'船','orange':'橙子','car':'汽车','plane':'飞机'}

C1= tk.IntVar()
C2 = tk.IntVar()
C3 = tk.IntVar()
C4 = tk.IntVar()
C5 = tk.IntVar()
C6 = tk.IntVar()
project_name = tk.StringVar()
picture_num = tk.StringVar()
predict_picture = tk.StringVar()
predict_project = tk.StringVar()
predict_model = tk.StringVar()
def p():        #备用函数
    pass
#创建项目
#检查项目名字；检查数量是否足够，4个起
def make_project():
    pro_name = project_name.get()
    try:
        num = int(picture_num.get())
    except:
        tkinter.messagebox.showinfo(app,message='请在图片数输入数字')
        return
    dic = {}
    if not os.path.exists(os.path.join('projects',pro_name)):
        if C1.get() == 1:
            dic['cat'] = '野猫'
        if C2.get() == 1:
            dic['cup'] = '水杯'
        if C3.get() == 1:
            dic['ship'] = '船'
        if C4.get() == 1:
            dic['orange'] = '橙子'
        if C5.get() == 1:
            dic['car'] = '汽车'
        if C6.get() == 1:
            dic['plane'] = '飞机'
        if len(dic) >= 3:
            tkinter.messagebox.showinfo(app,message='开始训练，请稍后再来看')
            cra = crawler(pro_name,dic,num)
            cra.craw()
            Train(pro_name)
        else:
            tkinter.messagebox.showinfo(app,message='请至少选择三个种类')
            return
    else:
        b = tkinter.messagebox.askyesno(app,message='此项目已经被创建过了,是否重新进行训练')
        if b:
            Train(pro_name)
        else:
            return
def predict():
    try:
        with open(os.path.join('projects', predict_project.get(), 'config.json')) as f:
            pre_dict = json.load(f)
            print(type(pre_dict))
    except:
        tkinter.messagebox.showinfo(app, message='没有找到对应的项目')
        return
    try:
        num = int(predict_model.get())
    except:
        tkinter.messagebox.showinfo(app,message='请在图片数输入数字')
        return
    model = Model(dim = len(pre_dict),size=resize)
    path = os.path.join('projects',predict_project.get(),'models')
    s = 'run_' + str(num)
    boolean = False
    for name in os.listdir(path):
        if s == name[:len(s)]:
            model.load_state_dict(torch.load(os.path.join(path,name)))
            boolean = True
    if boolean:
        th = predict_picture.get()
        if th[:4]=='http':
            try:
                req = requests.get(th).content
                with open('temp.jpg','wb') as f:
                    f.write(req)
            except:
                tkinter.messagebox.showinfo(app, message='无法从网络获取图片')
                return
        else:
            try:
                img = Image.open(th)
                img.save('temp.jpg')
            except:
                tkinter.messagebox.showinfo(app, message='无法获取指定的系统图片')
        tex = train.predict(model=model,pic='temp.jpg',dic=pre_dict)
        tkinter.messagebox.showinfo(app, message=tex)
        os.remove('temp.jpg')
    else:
        tkinter.messagebox.showinfo(app, message='没有找到对应的模型')
        return


L1 = tk.Label(app,text='项目名：')
L2 = tk.Label(app,text='图片数：')
L3 = tk.Label(app,text='项目：')
L4 = tk.Label(app,text='使用模型：')
L5 = tk.Label(app,text='预测图片')
c1 = Checkbutton(app,text='猫',variable=C1,command = p)
c2 = Checkbutton(app,text='水杯',variable=C2,command = p)
c3 = Checkbutton(app,text='船',variable=C3,command = p)
c4 = Checkbutton(app,text='橙子',variable=C4,command = p)
c5 = Checkbutton(app,text='汽车',variable=C5,command = p)
c6 = Checkbutton(app,text='飞机',variable=C6,command = p)
b1 = tk.Button(app,text='创建项目',command=make_project)
b2 = tk.Button(app,text='预测',command=predict)
project = tk.Entry(app,textvariable=project_name)
picture = tk.Entry(app,textvariable=picture_num)
pre_pro = tk.Entry(app,textvariable=predict_project)
pre_pic = tk.Entry(app,textvariable=predict_picture)
pre_num = tk.Entry(app,textvariable=predict_model)


picture.insert(0,'150')
L1.pack()
project.pack()
L2.pack()
picture.pack()
c1.pack()
c2.pack()
c3.pack()
c4.pack()
c5.pack()
c6.pack()
b1.pack()
L3.pack()
pre_pro.pack()
L4.pack()
pre_num.pack()
L5.pack()
pre_pic.pack()
b2.pack()
app.mainloop()
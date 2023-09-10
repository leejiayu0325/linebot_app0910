# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 11:39:57 2023

@author: USER
"""

import tkinter as tk
from tkinter import ttk
from tools import init_app
from train import get_train_data,get_stations,get_datime
from datetime import datetime

data=None

def get_train():
    global data
    ticket=True if check_var.get()!='0' else False
    try:
        df=get_train_data(startStation.get(),endStation.get(),rideDate.get(),
                           startTime.get(),endTime.get(),ticket)
        if df is not None:           
            data=df.iloc[:,[0,1,2,3,4,5,9,-1]]
        result.config(text='查詢成功',fg='blue') 
        #print(df,data)
        
        train_link()
        
    except Exception as e:
        print(e)
        result.config(text='查詢失敗',fg='red') 
    return data
def train_link():
    
    #------------程式外框---------------
    app=tk.Toplevel(tran_app)
    app.geometry('500x600')
    app.title('台鐵訂票系統')
    #------------設定內容---------------
    list_var=tk.StringVar()
    frame2=tk.Frame(app,width=500,height=600)
    frame2.pack(fill='both',expand=1)
    listbox = tk.Listbox(
        frame2, listvariable=list_var, font=font3, bg="aliceblue", fg="black"
        
    )
    list_var.set(data.values.tolist())
    listbox.pack(fill="both",expand=1)
    
    app.mainloop()
    
font0=('標楷體',20)
font1=('標楷體',18)
font2=('標楷體',16)
font3=('標楷體',14)

tran_app=init_app(size='400x600',title='台鐵查詢系統')

station=get_stations()
da_time=get_datime()
list_var=tk.StringVar()
check_var=tk.StringVar() 

frame1=tk.Frame(tran_app,width=300,height=600)
frame1.pack()

tk.Label(frame1,text='起始站點名稱：',font=font0).pack(pady=5)
startStation=ttk.Combobox(frame1,font=font1, values=[i for i in station],justify='center')
startStation.pack(pady=5)
startStation.current(0)

tk.Label(frame1,text='終止站點名稱：',font=font0).pack(pady=5)
endStation=ttk.Combobox(frame1,font=font1, values=[i for i in station],justify='center')
endStation.pack(pady=5)
endStation.current(9)

tk.Label(frame1,text='乘車時間(ex:2023/7/30)',font=font0).pack(pady=5)
rideDate=tk.Entry(frame1,font=font1,width=22,justify='center')
rideDate.pack(pady=5)
rideDate.insert(0,datetime.now().strftime('%Y/%m/%d'))

tk.Label(frame1,text='查詢起始時間：',font=font0).pack(pady=5)
startTime=ttk.Combobox(frame1,font=font1, values=da_time,justify='center')
startTime.pack(pady=5)
startTime.current(0)

tk.Label(frame1,text='查詢終止時間：',font=font0).pack(pady=5)
endTime=ttk.Combobox(frame1,font=font1, values=da_time,justify='center')
endTime.pack(pady=5)
endTime.current(48)

check_btn1 = tk.Checkbutton(frame1,variable=check_var, text='需有票',font=font3)    # 放入第一個單選按鈕
check_btn1.pack(pady=5)


tk.Button(frame1,text='查詢',font=font2,command=get_train).pack(pady=12)
result=tk.Label(frame1,text='查詢結果',font=font3)
result.pack(pady=5)


tran_app.mainloop()

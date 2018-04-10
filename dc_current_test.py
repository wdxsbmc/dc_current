#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter
from tkinter import *
import com
from com import *
import time

test_run = 0

root = tkinter.Tk()
root.title("DC Current TestV1.0.0")
SERIAL = com()


# button sttart
def button_start():
    print("test start>>>")
    # init com

    SERIAL.init_com('com' + en_com.get())
    SERIAL.port_open()

    # start test
    data = []
    data.append(int(en_model.get()))
    n_hz = int(en_hz.get())
    data.append(n_hz & 0xFF)
    n_hz >>= 8
    data.append(n_hz & 0xFF)  

    n_time = int(en_time.get())
    data.append(n_time & 0xFF)
    n_time >>= 8
    data.append(n_time & 0xFF)
    n_time >>= 8
    data.append(n_time & 0xFF)
    n_time >>= 8
    data.append(n_time & 0xFF)

    data_len = len(data)
    ret = SERIAL.cmd_send_recv(en_pld_borad.get(),en_pld_port.get(),0x07,data_len,data,0x87)

    if(ret == 1):
        # thread for recv
        test_run = 1
        thread.start_new_thread(SERIAL.read_data,())  
        pkt_offset = 0
     
        while test_run:  
            time.sleep(1)  
            print(SERIAL.message)
            # parse message
            while(pkt_offset < len(SERIAL.message)):
                pkt_head = SERIAL.message[pkt_offset:1]
                while head != '0x68':
                    pkt_offset = pkt_offset + 1
                    head = SERIAL.message[pkt_offset:1]

                pkt_len =  SERIAL.message[pkt_offset+4:1]   
                pkt_data = SERIAL.message[pkt_offset+6:pkt_len-5]
                pkt_offset = pkt_offset + pkt_len

            # save data  
            with open(".\dc_current_data.txt",'a') as fp:   
                for i in range(0,len(pkt_data)):
                    fp.write(pkt_data[i:2]+',')  


        # send stop cmd
        data1 = []
        ret = SERIAL.cmd_send_recv(en_pld_borad.get(),en_pld_port.get(),0x08,0,data1,0x88)

        # close port
        SERIAL.port_close()

# button stop
def button_stop():
    test_run = 0
    time.sleep(10)
    root.destroy()     
    print("test stop<<<")


# centrer 
def center_window(root, width, height):  
    screenwidth = root.winfo_screenwidth()  
    screenheight = root.winfo_screenheight()  
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)  
    #print(size)  
    root.geometry(size)  


# param
grid_column = 0
grid_row = 0
lb1 = Label(root, text="电流测试参数：") 
lb1.grid(column = grid_column,row = grid_row)


# com
grid_column = 0
grid_row = grid_row + 1
lb_pld_borad = Label(root, text="COM") 
lb_pld_borad.grid(column = grid_column,row = grid_row,pady=10)


grid_column = grid_column + 1
en_com = Entry(root)
en_com.grid(column = grid_column,row = grid_row,pady=10)
en_com.insert(10,"0")

# pld board
grid_column = 0
grid_row = grid_row + 1
lb_pld_borad = Label(root, text="PLD板编号") 
lb_pld_borad.grid(column = grid_column,row = grid_row,pady=10)


grid_column = grid_column + 1
en_pld_borad = Entry(root)
en_pld_borad.grid(column = grid_column,row = grid_row,pady=10)
en_pld_borad.insert(10,"1")

# pld board port
grid_column = 0
grid_row = grid_row + 1
lb_pld_port = Label(root, text="PLD板端口编号") 
lb_pld_port.grid(column = grid_column,row = grid_row,pady=10)


grid_column = grid_column + 1
en_pld_port = Entry(root)
en_pld_port.grid(column = grid_column,row = grid_row,pady=10)
en_pld_port.insert(10,"1")

# dc model
grid_column = 0
grid_row = grid_row + 1
lb2 = Label(root, text="电流模式：0小电流1大电流") 
lb2.grid(column = grid_column,row = grid_row,pady=10)


grid_column = grid_column + 1
en_model = Entry(root)
en_model.grid(column = grid_column,row = grid_row,pady=10)
en_model.insert(10,"0")

# dc hz
grid_column = 0
grid_row = grid_row + 1
lb3 = Label(root, text="采样频率（HZ）：") 
lb3.grid(column = grid_column,row = grid_row,pady=10)

grid_column = grid_column + 1
en_hz = Entry(root)
en_hz.grid(column = grid_column,row = grid_row,pady=10)
en_hz.insert(10,"1000")

# dc total time
grid_column = 0
grid_row = grid_row + 1
lb4 = Label(root, text="采样时长（秒）：") 
lb4.grid(column = grid_column,row = grid_row,pady=10)

grid_column = grid_column + 1
en_time = Entry(root)
en_time.grid(column = grid_column,row = grid_row,pady=10)
en_time.insert(10,"5")

# button
grid_row = grid_row + 3
grid_column = 0
button1 = Button(root, text='Start', width=25, command=button_start)  
button1.grid(column = grid_column,row = grid_row, sticky=E, pady=40)
grid_column = grid_column + 1
button = Button(root, text='Stop', width=25, command=button_stop)  
button.grid(column = 1,row = grid_row, sticky=E, pady=40)

# layout weight
root.columnconfigure(1,weight = 1)


# main UI
center_window(root, 400, 440)
# 进入消息循环
root.mainloop()
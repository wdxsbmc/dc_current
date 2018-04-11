#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter
from tkinter import *
import com
from com import *
import time
import _thread


test_run = 0

root = tkinter.Tk()
root.title("DC Current TestV1.0.0")
SERIAL = com()

# read save data thread
def read_data_thd(SERIAL, test_run):
    time.sleep(1)
    while test_run:       
        SERIAL.read_data()
        time.sleep(1)


def parse_save_thd(SERIAL, test_run):

    pkt_offset = 0 
    time.sleep(1)  
    old_len = 0
    old_offset = 0
    parse_msg = SERIAL.message[old_len:]
    b_find = 0

    while test_run:       
        
        # get pkt
        parse_msg.extend(SERIAL.message[old_len:])
        old_len = len(parse_msg)

        # parse message
        while(pkt_offset < len(parse_msg)): 

            # wait next pkt or stop
            if(pkt_offset + 4 > len(parse_msg)):
                if(old_offset != pkt_offset):
                    #print('break at:',pkt_offset)
                    old_offset = pkt_offset
                break

            # find pkt head
            print(pkt_offset,len(parse_msg))
            b_find = 0
            for i in range(pkt_offset,len(parse_msg)):
                if(parse_msg[i - 1] == 0xFE and parse_msg[i] == 0x68):
                    pkt_offset = i #move offset
                    b_find = 1
                    break
            if(b_find == 0):
                break

            # get pkt data len
            print(pkt_offset)
            pkt_data_len =  parse_msg[pkt_offset + 4]
            if(pkt_data_len == 0):
                pkt_offset = pkt_offset + 6  #skip first rsp
                continue

            # get pkt data
            pkt_data_len = pkt_data_len - 5  #skip Seq(4bytes)+CUR_MOD(1byte)    
            pkt_data = parse_msg[pkt_offset+9:pkt_offset+9+pkt_data_len]
            pkt_offset = pkt_offset + 9 + pkt_data_len 
            print(pkt_data)

            # save data  
            with open(".\dc_current_data.txt",'a') as fp:   
                for i in range(0,len(pkt_data),2):
                    #dcL dcH =>int16
                    dc_value = 0
                    dc_value = pkt_data[i+1] 
                    dc_value <<= 8 
                    dc_value = dc_value | pkt_data[i]
                    fp.write(str(dc_value) + ',')  


            

        

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
    ret = SERIAL.cmd_send(en_pld_borad.get(),en_pld_port.get(),0x07,data_len,data,0x87)

    if(ret == 1):
        # thread for recv
        test_run = 1
        _thread.start_new_thread(read_data_thd,(SERIAL, test_run))  
        time.sleep(1)
        _thread.start_new_thread(parse_save_thd,(SERIAL, test_run))  




# button stop
def button_stop():
    test_run = 0
    time.sleep(10)
    # send stop cmd
    data1 = []
    ret = SERIAL.cmd_send_recv(en_pld_borad.get(),en_pld_port.get(),0x08,0,data1,0x88)

    # close port
    SERIAL.port_close()


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
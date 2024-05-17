import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from SerialList import serial_ports as GetAvailableSerialPorts
import subprocess as ter





PORT = 8

command = ['esptool' ,  
           '--before', 'default_reset', 
           '--after' , 'hard_reset' ,
           '--chip', 'esp8266' ,
           '--port', '' ,
           '--baud', '115200' ,
           '--connect-attempts' ,'0' ,
           'write_flash', '0x0' ,
            ''  ]
def open_file():
   file = filedialog.askopenfile(mode='r', filetypes=[('Binary Files', '*.bin')])
   if file:
       global command
       
       command[-1] = file.name
       ChosenFilePath.delete(1.0, "end-1c")
       ChosenFilePath.insert('1.0' , file.name)
       ChosenFilePath['state'] = 'disabled'



def butn():
    command[PORT] = ListOfPorts.get()
    if command[PORT][:3] == 'COM':
        s = ter.run(command , text=True , capture_output=True )
        OutputText.insert('1.0', ' '.join(str(e) for e in command) + 
                          '\n-------------------------------------------------\n' +  
                          s.stdout + 
                          '\n-------------------------------------------------\n')
    else:
        OutputText.insert('1.0', 'ERROR: Wrong Port')
    # print(command)


main_window = tk.Tk()

ListOfPortsText = ttk.Label(main_window , text='Port', font = ('normal' , 10)).grid(
    column=0 , row=5  ,padx = 10, pady = 25)

 

ListOfPorts = ttk.Combobox(main_window , width=27 , )
ListOfPorts.grid(column = 1, row = 5 , padx=10 , pady=25) 

l = GetAvailableSerialPorts()
ListOfPorts['values'] = l

BrowseButton = ttk.Button(main_window, text="Browse", command=open_file).grid(row=7,column=0,pady=25 , padx=10)
ChosenFilePath = tk.Text(main_window ,  height=1 , width=50  )
ChosenFilePath.grid(row=7 ,column= 1 ,  padx=10 , pady=25)

#ListOfPorts['values'] = GetAvailableSerialPorts()

SendButton = ttk.Button(main_window , text='Send' ,command=butn )
SendButton.grid(column=1 , row = 10 , padx=10 , pady=25)

OutputText = tk.Text(main_window, height=10 , width=50)
OutputText.grid(row=11 , column=1 , padx=10 , pady=25)



main_window.mainloop()
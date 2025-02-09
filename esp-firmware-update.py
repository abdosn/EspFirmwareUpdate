import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from SerialList import serial_ports as GetAvailableSerialPorts
import subprocess as ter
import time
import threading

TSendCommandEvent = threading.Event()
main_window = tk.Tk()
main_window.title( 'Esp Firmware Update')

PORT = 8
running = True
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
       ChosenFilePath['state'] = 'normal'
       ChosenFilePath.delete(1.0, "end-1c")
       ChosenFilePath.insert('1.0' , file.name)
       ChosenFilePath['state'] = 'disabled'


def SendCommand():
    while running:

        if TSendCommandEvent.is_set():
            TSendCommandEvent.clear()
            command[PORT] = ListOfPorts.get()
            if command[PORT][:3] == 'COM' or command[PORT][:8] == '/dev/tty':
                # s = ter.run(command , text=True , capture_output=True )
                OutputText.insert('end', ' '.join(str(e) for e in command) + '\n-------------------------------------------------\n')
                time.sleep(1)
                popen = ter.Popen(command , stdout=ter.PIPE , stderr=ter.STDOUT )
                Output = ''
                for stdout_line in iter(popen.stdout.readline, ""):
                    if stdout_line.decode('utf-8') == '':
                        break
                    OutputText.insert('end',    stdout_line.decode('utf-8'))
                    OutputText.see('end')
                
                exitcode = popen.returncode
            else:
                OutputText.insert('end',    '\n-------------------------------------------------\n' +
                                            'ERROR: Wrong Port' )
            OutputText.insert('end',    '\n-------------------------------------------------\n')
            # print(command)
            OutputText.see('end')
        time.sleep(0.1)


def butn():
    TSendCommandEvent.set()


def Quit():
    main_window.destroy()
    global running
    running = False
TSendCommand = threading.Thread(target=SendCommand)
TSendCommand.start()


ListOfPortsText = ttk.Label(main_window , text='Port', font = ('normal' , 10)).grid(
    column=0 , row=5  ,padx = 10, pady = 25)

 

ListOfPorts = ttk.Combobox(main_window , width=27 , )
ListOfPorts.grid(column = 1, row = 5 , padx=10 , pady=25) 

l = GetAvailableSerialPorts()
ListOfPorts['values'] = l

BrowseButton = ttk.Button(main_window, text="Browse", command=open_file).grid(row=7,column=0,pady=25 , padx=10)
ChosenFilePath = tk.Text(main_window ,  height=1 , width=50   )
ChosenFilePath.grid(row=7 ,column= 1 ,  padx=10 , pady=25)

#ListOfPorts['values'] = GetAvailableSerialPorts()

SendButton = ttk.Button(main_window , text='Send' ,command=butn )
SendButton.grid(column=1 , row = 10 , padx=10 , pady=25 )


vbar = ttk.Scrollbar(main_window , orient='vertical', )
vbar.grid(row=11 , column=2 , sticky='nsew')
OutputText = tk.Text(main_window, height=15 , width=50 , yscrollcommand=vbar.set  )
vbar['command'] = OutputText.yview
OutputText.grid(row=11 , column=1 ,sticky='nsew', padx=10 , pady=25)


QuitButton = ttk.Button(main_window , text='Quit' ,command=Quit ).grid(row=20 , column=1 , padx=10 , pady=25)

main_window.protocol('WM_DELETE_WINDOW', Quit)  
main_window.mainloop()
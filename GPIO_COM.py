import sys
import os
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

import RPi.GPIO as pi
import serial
ser = serial.Serial(port='/dev/ttyAMA0',
                    baudrate =9600,
                    bytesize =serial.EIGHTBITS,
                    parity   =serial.PARITY_NONE,
                    stopbits =serial.STOPBITS_ONE,
                    timeout  =0)

kNullCursorData="""
  #define t_cur_width 1
  #define t_cur_height 1
  #define t_cur_x_hot 0
  #define t_cur_y_hot 0
  static unsigned char t_cur_bits[] = { 0x00};
  """
pin_red = 17
pin_green = 27
pin_blue = 22

class Fullscreen_Window:

    def __init__(self):
        pi.setmode(pi.BCM)
        pi.setup(pin_red,pi.IN)
        pi.setup(pin_green,pi.IN)
        pi.setup(pin_blue,pi.IN)

        self.intensityR = 0
        self.intensityG = 0
        self.intensityB = 0
        self.shutterR = 0
        self.shutterG = 0
        self.shutterB = 0
        self.shutterW = 0 # LED on/off
        
        self.tk = Tk()
        # Should clean this up on quit
        os.umask(0177) # octal
        f=open("testcursor","w")
        f.write(kNullCursorData)
        f.close()
        #self.t=Text(self.tk,bg="white",cursor="@testcursor white")
        #self.t.pack()
        self.tk.configure(cursor="@testcursor white")
    
        self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        
        self.tk.configure(background='black')
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.bind("<F10>", self.toggle_color)
        self.state = True
        self.tk.attributes("-fullscreen", True)
        self.update()


    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def toggle_color(self, event=None):
        if(self.tk["bg"]=='black'):
            self.tk.configure(background='blue')
        elif(self.tk["bg"]=='blue'):
            self.tk.configure(background='red')
        elif(self.tk["bg"]=='red'):
            self.tk.configure(background='green')
        elif(self.tk["bg"]=='green'):
            self.tk.configure(background='black')
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
    
    def update(self):
        """colorcode + number: change channel intensity
           colorcode + T: set channel shutter ON (True)
           colorcode + F: set channel shutter OFF (False)"""
        rcv=ser.read(2)
        if len(rcv)==2:
            colorcode = rcv[0]
            parameter = rcv[1]
           
            if parameter == 'F':#False
                if colorcode == 'r':
                    self.shutterR = 0
                elif colorcode == 'g':
                    self.shutterG = 0
                elif colorcode == 'b':
                    self.shutterB = 0
                elif colorcode == 'w':
                    self.shutterR = 0
                    self.shutterG = 0
                    self.shutterB = 0
            elif parameter == 'T': #True
                if colorcode == 'r':
                    self.shutterR = 1
                elif colorcode == 'g':
                    self.shutterG = 1
                elif colorcode == 'b':
                    self.shutterB = 1
                elif colorcode == 'w':
                    self.shutterR = 1
                    self.shutterG = 1
                    self.shutterB = 1
            else:#parameter is number
                intensity = ( int(rcv[1])+1 )*255/10
                if colorcode == 'r':
                    self.intensityR = intensity
                elif colorcode == 'g':
                    self.intensityG = intensity
                elif colorcode == 'b':
                    self.intensityB = intensity
                elif colorcode == 'w':
                    self.intensityR = intensity
                    self.intensityG = intensity
                    self.intensityB = intensity

            colorRGB='#%02x%02x%02x' % (self.intensityR*self.shutterR,
                                        self.intensityG*self.shutterG,
                                        self.intensityB*self.shutterB)
            self.tk["bg"]=colorRGB

        self.tk.after(100,self.update)

if __name__ == '__main__':
    w = Fullscreen_Window()
    w.tk.mainloop()

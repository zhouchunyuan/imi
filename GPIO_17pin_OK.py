import sys
import os
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

import RPi.GPIO as pi

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
        """Runs every 100ms to update the state of the GPIO inputs"""
        if pi.input(pin_red):
            self.tk.configure(background='red')
        elif pi.input(pin_green):
            self.tk.configure(background='green')
        elif pi.input(pin_blue):
            self.tk.configure(background='blue')
        else:
            self.tk.configure(background='black')
        self.tk.after(100,self.update)

if __name__ == '__main__':
    w = Fullscreen_Window()
    w.tk.mainloop()

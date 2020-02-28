import tkinter as tk
from tkinter import Checkbutton,IntVar
from tkinter.ttk import Notebook
from tkinter.constants import *
import time

from tkinter.colorchooser import askcolor

'''
from pathfinding1.core.diagonal_movement import DiagonalMovement
from pathfinding1.core.grid import Grid
from pathfinding1.finder.a_star import AStarFinder
'''
import multiprocessing as mp

import pybresenham as pyb

import pathlib as plib


_d={}

_d['main_dir']=plib.Path.cwd()

_d['g_dir']=plib.Path(_d['main_dir'],'Game Files')

_d['t_dir']=plib.Path(_d['g_dir'],'Textures')

_d['icon_dir']=plib.Path(_d['main_dir'],'Icon images')

_d['unit_t_dir']=plib.Path(_d['t_dir'],'Unit textures')

_d['tile_t_dir']=plib.Path(_d['t_dir'],'Tile textures')

_d['f_dir']=plib.Path(_d['g_dir'],'Factions')

_d['m_dir']=plib.Path(_d['t_dir'],'Maps')

'''class Main_Menu:
    def __init__(self,master,iconpath,Main):
        self.Main=Main
        self.master=master
        self.iconpath=iconpath
        self.main_image=tk.PhotoImage(file=self.iconpath+'Main_Image.gif')
        self.menu_frame=tk.Frame(self.master,
                                 height=500,
                                 width=500,
                                 bg='blue')
        self.image_label=tk.Label(self.menu_frame,image=self.main_image)
        self.image_label.pack(fill=BOTH,expand=YES)
        self.menu_frame.pack(fill=BOTH,expand=YES)

        self.menu=tk.Menu(tearoff=0)
        self.File=tk.Menu(tearoff=0)
        self.New_Game=tk.Menu(tearoff=0)
        self.New_Game.add_command(label='Demo',command=self.Main.to_game)
        self.File.add_cascade(label='New Game',menu=self.New_Game)
        self.File.add_separator()
        self.File.add_command(label='Quit',command=self.master.destroy)
        
        self.menu.add_cascade(label='File',menu=self.File)
        
        
        self.master.config(menu=self.menu)'''
        

class base_window_0:
    #The action frames are:
    #/
    #self.tool_f
    #self.view_f
    #
    #Scrollbars
    #/
    #self.scr_v
    #self.scr_h
    
    def __init__(self,master):


        self.fg_color='#444444'
        self.bg_color=''

        self.frames={}
        


        self.fullscreen_state=False

        self.toolbar_state=True

        self.screen_size=tk.BitmapImage(file=plib.Path(_d['icon_dir'],'screen_size_icon.xbm'),
                                        foreground=self.fg_color)
        self.toolbar=tk.BitmapImage(file=plib.Path(_d['icon_dir'],'toolbar_icon.xbm'),
                                    foreground=self.fg_color)

        self.master=master

        self.frames['tool_f']=tk.Frame(self.master,bg='cyan',width=150)
        self.frames['tool_f'].pack(side=LEFT,fill=Y)

        self.frames['main_f']=tk.Frame(self.master)
        self.frames['main_f'].pack(fill=BOTH,expand=YES,side=RIGHT)
        
        self.frames['top_f']=tk.Frame(self.frames['main_f'])
        self.frames['top_f'].pack(fill=BOTH,expand=YES)

        
        self.frames['bottom_f']=tk.Frame(self.frames['main_f'])
        self.frames['bottom_f'].pack(fill=X)       

        

        
        
        
        self.frames['view_f']=tk.Frame(self.frames['top_f'],bg='green')
        self.frames['view_f'].pack(side=LEFT,fill=BOTH,expand=YES)
       
        
        self.screen_b=tk.Button(self.frames['bottom_f'],
                                image=self.screen_size,
                                command=self.screen_tgl)
        self.screen_b.pack(side=RIGHT)
        

        self.toolbar_b=tk.Button(self.frames['bottom_f'],
                                 image=self.toolbar,
                                 command=self.toolbar_tgl)
        self.toolbar_b.pack(side=LEFT)

        self.scr_v=tk.Scrollbar(self.frames['top_f'],orient=VERTICAL)
        self.scr_v.pack(side=RIGHT,fill=Y)

        self.scr_h=tk.Scrollbar(self.frames['bottom_f'],orient=HORIZONTAL)
        self.scr_h.pack(fill=X,side=LEFT,expand=YES)


    def toolbar_tgl(self,event=None):
        if self.toolbar_state==False:
            #self.tool_f=tk.Frame(self.master,width=100,bg='cyan')
            self.frames['tool_f'].pack(side=LEFT,fill=Y)
            self.toolbar_state=not self.toolbar_state
        else:
            self.frames['tool_f'].forget()
            self.toolbar_state=not self.toolbar_state


    def screen_tgl(self,event=None):
        self.fullscreen_state=not self.fullscreen_state
        self.master.attributes('-fullscreen',self.fullscreen_state)
            
        

#-----------------------------



        
        
        
class game_windows(base_window_0):
    def __init__(self,master,mode):
        #self.f=tk.PhotoImage(file=r'D:\User assets\Pictures\img_example.gif')
        super().__init__(master)







        
 

        #self.c=tk.Canvas(self.frames['view_f'],bg='#222222',highlightthickness=0)
        self.c=tk.Canvas(self.frames['view_f'],bg='gray',highlightthickness=0)
        self.t=tk.Text(self.frames['view_f'],bg='black',fg='white',insertbackground='white')
        self.screen_options(mode)



        
        
    def screen_options(self,mode):
        if mode=='window':

            self.canvas_window()
        elif mode=='text':

            self.text_window()



 



    def canvas_window(self,event=None):
        for i in self.frames['view_f'].winfo_children():
            i.forget()
        #self.frames['view_f'].winfo_children()[0].forget()
        #c_height=self.row_height*self.rows
        #c_width=self.col_width*self.cols
        self.c.pack(fill=BOTH,expand=True,side=LEFT)
        #self.c.create_image(0,0,anchor=NW,image=self.f)
        self.c.config(yscrollcommand=self.scr_v.set)
        self.c.config(xscrollcommand=self.scr_h.set)
            
        self.scr_v.config(command=self.c.yview)
        self.scr_h.config(command=self.c.xview)
            
        self.c.bind('<Configure>',self.window_config)
        #self.c.config(scrollregion=self.c.bbox('all'))
        #self.c.bind('<Button-1>',self.grid_click)

    def text_window(self,event=None):
        for i in self.frames['view_f'].winfo_children():
            i.forget()
        #self.frames['view_f'].winfo_children()[0].forget()
        self.t.pack(fill=BOTH,expand=YES)
        self.t.config(yscrollcommand=self.scr_v.set)
        self.t.config(xscrollcommand=self.scr_h.set)

        self.t.config(wrap=None)
        
        self.scr_v.config(command=self.t.yview)
        self.scr_h.config(command=self.t.xview)
            
    def window_config(self,event=None):
        self.c.config(scrollregion=self.c.bbox('all'))
        #self.c.config(scrollregion=self.c.bbox('tile0','tile1'))







if __name__=='__main__':
    #iconpath=r'D:\User assets\Scripts\Python\Icon images\\'
    root=tk.Tk()
    win=game_windows(root,'text')
    root.mainloop()

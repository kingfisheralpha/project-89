import esper

import time

from tkinter.constants import *

from game_window_framework import *



from xml.etree import ElementTree as et

import pathlib as plib

import itertools as it
from PIL import Image,ImageDraw,ImageTk,ImageOps,ImageFont
from PIL import ImageColor as ic

import multiprocessing as mp

import os

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import pybresenham as pyb

'''
def calc_path0(grid):
        
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path_coords=[]
    while True:
        x0,y0,x1,y1,span_x,span_y,_object=p1.get()

        #table=Grid(matrix=grid,span_x=span_x,span_y=span_y)
        table=Grid(matrix=grid,span_x=span_x,span_y=span_y)

        start=table.node(x0,y0)
        end=table.node(x1,y1)
        #finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        
        path, runs = finder.find_path(start, end, table)

        path_coords.clear()
        for i in path:
            j=((i[0]*col_width+col_width//2,
                i[1]*row_height+row_height//2))
            path_coords.append(j)

        a=(_object,path_coords,)

            
        q.put(a)
'''
_d={}

_d['main_dir']=plib.Path.cwd()

_d['g_dir']=plib.Path(_d['main_dir'],'Game Files')

_d['t_dir']=plib.Path(_d['g_dir'],'Textures')

_d['icon_dir']=plib.Path(_d['g_dir'],'Icon images')

_d['unit_t_dir']=plib.Path(_d['t_dir'],'Unit textures')

_d['tile_t_dir']=plib.Path(_d['t_dir'],'Tile textures')

#_d['f_dir']=plib.Path(_d['g_dir'],'Factions')

_d['m_dir']=plib.Path(_d['t_dir'],'Maps')


def visi_grid(width,height,r):
    x0,y0=0,0

    width=int(width)
    height=int(height)
    r=int(r)



        


    '''    
    width=1
    height=1



    r=4
    '''
    


    list1=[[0 for i in range((r * 2)+width)]for j in range((r * 2)+height)]


    c=list(pyb.circle(x0,y0,r))

    c1=[]

    for i in c:
        if i[0]>=0:
            a=i[0]+height-1
        else:
            a=i[0]
        if i[1]>=0:
            b=i[1]+width-1
        else:
            b=i[1]

        c1.append((a,b))

    #c1.append((0,0))

    for i in range(width-1):

        
        
        
        
        c1.append((x0-r,y0+i))
        c1.append((x0+r+height-1,y0+i))
        
        
        

        

    for i in range(height-1):
        
        
        


        c1.append((x0+i,y0-r))
        c1.append((x0+i,y0+r+width-1))
        

        
        pass



        



       
        

    c2=list(pyb.translatePoints(c1,r,r))



    
    c3=list(pyb.floodFill(c2,r,r))
    #c3.append((r,r))


    for i in c3:
        list1[i[0]][i[1]]=1

    print(c3)

    return [r,c3]


#visi_grid(2,2,0)


        



def calc_path(data,q,grid):

    print('initiation')
    units={}
    for i in data:
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)



        table=Grid(matrix=grid)


        start=table.node(data[i][0][0],data[i][0][1])
        end=table.node(data[i][1][0],data[i][1][1])

        path, runs = finder.find_path(start, end, table)
        #units.append([i,path])
        units[i]=path
        
    q.put(units)
        
    
class Game_select:
    def __init__(self,master):

        self.master=master
        pass





class Start_Game:
    def __init__(self,master):
        self.master=master

        self.w=esper.World()

        #base game window

        

        self._map='map1.xml'

        self.faction_list=[{'name':'Military',
                            'bg':'',
                            'icon_dir':'Military_textures',
                            'fg':'blue',
                            'visible':'true',
                            'Units':{'Infantry':{
                                     'icon':'infantry.xbm',
                                     'movable':'true',
                                     'visi_radius':'2',
                                     'speed':'2',
                                     'auto_scripts':{'visibility':['1','1','4']},
                                     'move_mod':'4'}}}]
        for i in self.faction_list:
            for j in i['Units']:
               


                

                img0=Image.open(plib.Path(_d['unit_t_dir'],i['icon_dir'],i['Units'][j]['icon']))

                
                img=ImageTk.BitmapImage(image=img0,background=i['bg'],foreground=i['fg'])

                                        
                i['Units'][j]['image']=img
                
                
        



        self.comm_list=[['faction1','player',['Military']]]


        

        self.ui=self.w.create_entity()

        self.w.add_component(self.ui,
                             game_windows(self.master,'window'))




        self.w.add_component(self.ui,Game_Manager(self.w,self._map))

        self.control=self.w.component_for_entity(self.ui,Game_Manager)

        self.w.add_processor(Movement(self.w,self.control))

        self.w.add_processor(Visibility(self.w,self.control))


        self.w.add_processor(TickRate(self.w,self.ui))



        self.create_factions()
        self.create_commands()

        #def add_unit(self,faction,unit_name,x0,y0)

        self.control.add_unit('Military','Infantry',5,2)

        self.control.add_unit('Military','Infantry',5,2)

        

        




    def create_factions(self):
        a=self.w.component_for_entity(self.ui,Game_Manager)
        
        
        for i in self.faction_list:
            a.add_faction(i)
            
    def create_commands(self):
        b=self.w.get_processor(Movement)
        for i in self.comm_list:
            if i[1]=='player':
                a=self.w.create_entity()
                self.w.add_component(a,Player(self.w,a,i[2]))
                b.add_queue(a)



















iconpath=r'D:\User assets\Scripts\Python\Icon images\\'

class Auto_Scripts(esper.Processor):
    def __init__(self,world):
        self.w=world

    def process(self):

        a=self.w.get_component(Unit)
        for i in a:
            pass

        pass

class Visibility(esper.Processor):
    def __init__(self,world,control):
        self.w=world
        

        self.factions=control.factions



        self.m_grid=control.m_grid

    def process1(self):
    
        a=self.w.get_components(Player)
        for i in a:
            pass
        pass


    def process(self):
        a=self.w.get_component(Unit)
        for i in a:
            a1=i[1]
            r=a1.stats['visi_radius']
            visi_grid=a1.stats['visi_grid']

            x0,y0=a1.stats['pos']

            list1=[]

            for i in visi_grid:
                x=x0-r+i[0]
                y=y0-r+i[1]
                if 0<=x<len(self.m_grid[0]) and 0<=y<len(self.m_grid):
                    list1.append((x,y))
            for i in list1:
                for i in self.m_grid[i[1]][i[0]]:
                    print('unit discovered',i)
                
                
                
            


class TickRate(esper.Processor):
    def __init__(self,world,ui):
        self.tickrate=1000
        self.w=world
        self.root=self.w.component_for_entity(ui,game_windows).master

        move=self.w.get_processor(Movement)



        
        self.root.after(self.tickrate,self.process)

    def process(self):
        self.w.get_processor(Movement).process()

        #self.w.get_processor(Visibility).process()


        
        self.root.after(self.tickrate,self.process)


class Movement(esper.Processor):
    def __init__(self,world,control):
        self.w=world
        self.queues={}
        
        self.grid=control.grid
        self.m_grid=control.m_grid
        self.col_width=control.col_width
        self.row_height=control.row_height
        self.c=control.c
        self.move_q={}
        self.selections=[]

        self.unit_removal=[]
        #self.c.after(1000,self.process)
        #wueues{ent:[mp.Queue(),bool,unit/path list}
        pass
    def add_queue(self,ent):
        self.queues[ent]=[True,mp.Queue(),{}]
        pass

    def config_pathlines(self,data):

        self.c.itemconfig('pathlines',state=HIDDEN)
        
        c_w=self.col_width
        r_h=self.row_height
        for i in data:
            ent=i
            list1=data[ent]
            a=self.w.component_for_entity(ent,Unit)
            pathlines=a.stats['pathlines']
            endpoint=a.stats['endpoint']
            len1=len(pathlines)
            
            len2=len(list1)-1

            print('pathlines',len1,'list1',len2)
            if len2>0:
                #continue
                for i in range(min([len1,len2])):
                    self.c.coords(pathlines[i],list1[i][0]*c_w+c_w//2,
                                        list1[i][1]*r_h+r_h//2,
                                        list1[i+1][0]*c_w+c_w//2,
                                        list1[i+1][1]*r_h+r_h//2
                                  )


                
                for i in range(len1,len2):
                    pathlines.append(self.c.create_line(list1[i][0]*c_w+c_w//2,
                                                list1[i][1]*r_h+r_h//2,
                                                list1[i+1][0]*c_w+c_w//2,
                                                list1[i+1][1]*r_h+r_h//2,
                                                tags='pathlines',
                                                state=HIDDEN)
                                  )
                


                #below should be separate
                _min=min([len(pathlines),len2])
                
                '''
                
                
                for i in range(_min):
                    
                    self.c.itemconfig(pathlines[i],state=NORMAL)
                    pass
                '''


                x=list1[-1][0]
                y=list1[-1][1]


                self.c.coords(endpoint,x*self.col_width,
                              y*self.row_height+self.row_height//2,

                              x*self.col_width+self.col_width//2,
                              y*self.row_height,

                              x*self.col_width+self.col_width,
                              y*self.row_height+self.row_height//2,

                              x*self.col_width+self.col_width//2,
                              y*self.row_height+self.row_height)

                
                self.put_in_q(ent,list1,_min)

                
                    
                    


        pass
    def put_in_q(self,ent,list1,_min):
        speed=1
        a=self.w.component_for_entity(ent,Unit)
        speed=a.stats['speed']
        pathlines=a.stats['pathlines']
        endpoint=a.stats['endpoint']
        self.move_q.update({ent:[0,0,_min,list1]})

        if ent in self.selections:
            self.c.itemconfig(endpoint,state=NORMAL)
            
            #for i in range(0,_min):
            a=self.move_q[ent]
            for i in range(a[1],a[2]):
                    
                self.c.itemconfig(pathlines[i],state=NORMAL)
                pass

        else:
            print('not in selections')
                
        
        
        
    
    def calc(self,ent,data):
        q=self.queues[ent]
        if q[0]==True:
            p=mp.Process(target=calc_path,args=(data,q[1],self.grid,))
            p.start()
            q[0]=False

    def path_cost(self,path,_index,mod):
        elem=path[_index]
        elem1=int(self.grid[elem[1]][elem[0]])**(1/mod)
        elem2=round(elem1,2)
        return elem2
        

    def unit_move(self,_dict,selections):
        returned_list=[]
        for i in _dict:
            ent=i
            a=_dict[i]
            unit=self.w.component_for_entity(ent,Unit)
            #a=self.move_q[ent]
            

            visible=False

            if ent in selections:
                visible=True
            else:
                visible=False

            pathlines=unit.stats['pathlines']
            speed=round(unit.stats['speed'],2)
            endpoint=unit.stats['endpoint']

            
            a[0]+=speed

            
            a2=0

            mod=float(unit.stats['move_mod'])

            
            while a[0]>=self.path_cost(a[3],a[1]+a2,mod)and a[2]>a[1]+a2:
                
                
                a[0]-=self.path_cost(a[3],a[1]+a2,mod)
                a2+=1
                

            
                

            




            #move init
            x0,y0=a[3][a[1]]
            x1,y1=a[3][a[1]+a2]
            

            #move graphics
            x,y=((x1-x0)*self.col_width,(y1-y0)*self.row_height)
            
            self.c.move(unit.stats['icon'],x,y)
            self.c.move(unit.stats['healthbar'],x,y)

            if visible==True:
                for i in range(a[1],a[1]+a2):
                    self.c.itemconfig(pathlines[i],state=HIDDEN)
            a[1]+=a2

            #if x0!=x1 and y0!=y1:

            del self.m_grid[y0][x0][self.m_grid[y0][x0].index(ent)]


            self.m_grid[y1][x1].append(ent)

            
            
            unit.stats['pos']=(x1,y1)

            if a[2]==a[1]:
                if visible==True:
                    self.c.itemconfig(endpoint,state=HIDDEN)
                returned_list.append(ent)
                
        return returned_list

        
        
        
    """else:
        #del self.move_q[ent]
        pass"""
        
    def process(self):
        


        for i in self.unit_move(self.move_q,self.selections):

            del self.move_q[i]
        print('move_q',self.move_q)

            

            

        for i in self.queues:
            q=self.queues[i]
            try:
                a=q[1].get(False)

                q[2].update(a)
                print('deployed')
                q[0]=True
                self.config_pathlines(q[2])
                q[2].clear()
        
                    
                    
                    
            except Exception:
                print('nothing')
                pass

        #contienue
                
        #self.c.after(1000,self.process)
        pass
    


class Player:
    def __init__(self,world,ent,f_list):
        self.w=world
        self.ent=ent
        a=self.w.get_component(Game_Manager)[0]
        self.c_ent=a[0]
        self.c=a[1].c

        self.col_width=a[1].col_width
        self.row_height=a[1].row_height

        self.grid=a[1].grid

        self.move=self.w.get_processor(Movement)

        

        self.box={}
        self.c.create_rectangle(0,0,50,50,state=HIDDEN,tags=('selectbox',))
        self.c.tag_raise('selectbox')

        self.factions=[]

        self.selection=[]


        #self.c.config('selectbox',state='hidden')
        

        #self.c.bind('<Button-1>',self.draw_)

        for i in f_list:
            self.factions.append(i)

        
        
        self.c.bind('<B1-Motion>',self.rectbox)

        self.c.bind('<Button-1>',self.rectbox)

        
        

        self.c.bind('<ButtonRelease-1>',self.rectbox_release)

        self.c.bind('<ButtonRelease-3>',self.r_click)




    def add_unit(self):
        #self.c_ent
        a=self.w.component_for_entity(self.c_ent)
        
        
        pass












    def r_click(self,event=None):
        #self.c.itemconfig('healthbar',state=HIDDEN)
        #self.c.itemconfig('pathlines',state=HIDDEN)
        #self.c.itemconfig('endpoint',state=HIDDEN)



        #if point==None:
        x=int(self.c.canvasx(event.x))
        y=int(self.c.canvasy(event.y))
        x0=x//self.col_width
        y0=y//self.row_height
        #print(x//self.col_width,y//self.row_height)

        
        #a=[[x0,y0],self.selection]
        b3={}
        
        self.c.itemconfig('pathlines',state=HIDDEN)
        self.c.itemconfig('endpoint',state=HIDDEN)


        for i in self.selection:
            if i in self.move.move_q:
                del self.move.move_q[i]
                

            b2=self.w.component_for_entity(i,Unit)
            if b2.stats['movable']==True:
                b3[i]=[b2.stats['pos'],[x0,y0]]


        #calc_path(b3,self.grid)
        self.move.calc(self.ent,b3)
        

        pass





    def rectbox(self,event=None):
        #print('yo')
        self.c.after(50)
            
        x=int(self.c.canvasx(event.x))
        y=int(self.c.canvasy(event.y))

        




        if len(self.box.keys())==0:

            self.box[0]=x
            self.box[1]=y

            

            self.c.coords('selectbox',self.box[0],self.box[1],self.box[0],self.box[1])

        else:
            self.c.itemconfig('selectbox',state=NORMAL)

            self.box[2]=x
            self.box[3]=y
            self.c.coords('selectbox',self.box[0],self.box[1],self.box[2],self.box[3])


    def rectbox_release(self,event=None):
        
        if len(self.box.keys())==4:
            self.c.itemconfig('selectbox',state=HIDDEN)

            a=self.c.find_overlapping(self.box[0],
                                             self.box[1],
                                             self.box[2],
                                             self.box[3])
            

                        

            
            
            

        else:
            x=int(self.c.canvasx(event.x))
            y=int(self.c.canvasy(event.y))

            a=self.c.find_closest(x,y)

        self.box.clear()




        
        a1=[]
        for i in a:
            b=self.c.gettags(i)
            if b[0]=='Unit':
                if b[1] in self.factions:
                    a1.append(int(b[2]))
        if len(a1)>0:
            self.c.itemconfig('healthbar',state=HIDDEN)
            self.c.itemconfig('pathlines',state=HIDDEN)
            self.c.itemconfig('endpoint',state=HIDDEN)
            for i in a1:

                
                
                
                
                
                a2=self.w.component_for_entity(i,Unit)
                #print('a2',a2)
                
                
                self.c.itemconfig(a2.stats['healthbar'],state=NORMAL)
            self.selection=a1
            self.move.selections=self.selection





    
            for i in self.selection:
                if i in self.move.move_q:
                    a3=self.move.move_q[i]
                    a4=self.w.component_for_entity(i,Unit)
                    pathlines=a4.stats['pathlines']
                    endpoint=a4.stats['endpoint']
                    self.c.itemconfig(endpoint,state=NORMAL)
                    
                    for j in range(a3[1],a3[2]):
                    
                        self.c.itemconfig(pathlines[j],state=NORMAL)
                              
        print(self.selection)
        
        

        




class Faction:
    def __init__(self,data):


        self.data=data
        self.stats={}
        

        


        self.stats['visible']=bool(data['visible'])
        self.stats['unit_list']=[]
        self.stats['units']=data['Units']

        self.stats['bg']=data['bg']

        self.stats['fg']=data['fg']

        self.stats['name']=data['name']

        
        
        #store units faction_attributes name colors
        #self.attrs{name,bg,fg}
        pass

'''
class Command:
    def __init__(self):
        pass

    def select_units(self):
        pass
'''
class Unit:
    def __init__(self,g_m,ent,faction,unit_name,x0,y0):

        
        world=g_m.w
        self.stats={}
        f=world.component_for_entity(g_m.factions[faction],Faction)

        width=1
        height=1
        speed=float(f.stats['units'][unit_name]['speed'])
        movable=bool(f.stats['units'][unit_name]['movable'])

        if f.stats['visible']==True:
            visible=NORMAL
        else:
            visible=HIDDEN

        move_mod=f.stats['units'][unit_name]['move_mod']

        col_width=g_m.col_width
        row_height=g_m.row_height

        c=g_m.c

        m_grid=g_m.m_grid

        

        

        """img0=Image.open(plib.Path(_d['unit_t_dir'],
                                  f.data['icon_dir'],
                                  f.data['Units'][unit_name]['icon']))"""

        """self.img=ImageTk.BitmapImage(image=img0,background=f.data['bg'],
                            foreground=f.data['fg'])"""



        endpoint=c.create_polygon(x0*col_width,
                                  y0*row_height+row_height//2,

                                  x0*col_width+col_width//2,
                                  y0*row_height,

                                  x0*col_width+col_width,
                                  y0*row_height+row_height//2,

                                  x0*col_width+col_width//2,
                                  y0*row_height+row_height,
       

                                  fill='',
                                  outline='black',
                                  
                                  state=HIDDEN,
                                  tags=('endpoint',))
        

        icon=c.create_image(x0*col_width,
                                 y0*row_height,
                                 anchor=NW,
                            state=visible,
                                 image=f.stats['units'][unit_name]['image'],
                            
                            tags=('Unit',f.stats['name'],ent,))

        

        healthbar=c.create_rectangle(x0*col_width,
                                       y0*row_height,
                                        (x0+width)*col_width,
                                       (y0*row_height)+4,
                                     state=HIDDEN,
                                       #fill='green',
                                         
                                       fill='#00ff00',
                                       tags='healthbar')


        f.stats['unit_list'].append(ent)

        
       
        self.stats['icon']=icon

        self.stats['healthbar']=healthbar

        self.stats['speed']=speed

        #self.stats['pos']=(x0,y0)
        self.stats['endpoint']=endpoint
        self.stats['size']=(width,height)

        self.stats['pos']=(x0,y0)
        m_grid[y0][x0].append(ent)

        self.stats['pathlines']=[]

        self.stats['move_mod']=move_mod

        self.stats['movable']=movable

        self.stats['visi_radius']=int(f.stats['units'][unit_name]['visi_radius'])

        self.stats['visi_grid']=visi_grid(1,1,self.stats['visi_radius'])
        

        
                                 
        
        
        

        pass

class Game_Manager:
    def __init__(self,world,_map):
        self.w=world
        a=self.w.get_component(game_windows)[0]
        self.c_ent=a[0]
        self.c=a[1].c

        #name, entity
        self.factions={}

        self.add_map(_map)

        self.scripts={'visibility':visi_grid}
        



        

        #self.add_faction('Military')

        

        #self.add_unit('Military',3,5)

        #self.add_faction()

    def add_unit(self,faction,unit_name,x0,y0):
        #self,g_m,ent,faction,x0,y0
        ent=self.w.create_entity()

        self.w.add_component(ent,Unit(self,ent,faction,unit_name,x0,y0))
        pass


    def add_faction(self,data):
        

        ent=self.w.create_entity()

        self.factions[data['name']]=ent
        

        self.w.add_component(ent,Faction(data))

        '''if assignment!=None:
            a=self.w.components_for_entity(assignment)[0]
            a.factions.add(name)
            print('factions',a.factions)
            pass'''

    

        



    def add_map(self,_map,event=None):

        print('map initiated')

        c=et.parse(plib.Path(_d['m_dir'],_map))

        root=c.getroot()

        j=root.findall('map')

        """for i in j:
            print('map attrib',i.attrib)"""

        a=j[0].findall('grid')

        b=a[0].attrib['grid'].split('\n')


        t_style0=j[0].findall('text_styles')
        t_style=t_style0[0].findall('text_style')
        #print('t_style',t_style,t_style[0].attrib)


        c_t_style0=j[0].findall('texts')
        c_t_style=c_t_style0[0].findall('text')
        """
        for i in c_t_style:
            print('texts',i.attrib)"""
        #print('texts',c_t_style[0].attrib)




        #print(b)
        text_dict={}
        attribs=j[0].attrib

        #print('attribs',attribs)

        del b[-1]

        #print('hahaha',j[0].find('textures'))

        for i in j[0].findall('textures')[0].findall('texture'):
            
            _v=i.attrib
            text_dict.update({_v['canvas_id']:{'bg':_v['bg'],'fg':_v['fg'],'bitmap':_v['bitmap'],
                                               'grid_id':_v['grid_id']}})



        grid_size=[len(b[0]),len(b)]

        self_grid=[[int(attribs['default_empty_value']) for i in range(grid_size[0])] for j in range(grid_size[1])]

        

        
                


        




        #c=tk.Canvas(root,width=500,height=500)



        images1={}
        #os.chdir(pathlib.Path(_d['m_dir'],attribs['path']))

        for i in text_dict:
            a1=text_dict[i]['bitmap']
            images1[i]=Image.open(plib.Path(_d['tile_t_dir'],attribs['path'],a1))

        #print('images',images1)

        self.col_width=int(attribs['column_width'])

        self.row_height=int(attribs['row_height'])



        map0=Image.new('RGB',(grid_size[0]*self.col_width,
                              grid_size[1]*self.row_height),
                       color=attribs['map_bg'])

        map1=ImageDraw.Draw(map0)




        for row in range(len(b)):
            for col in range(len(b[row])):
                if b[row][col]!='.':
                    elem=text_dict[b[row][col]]
                    if elem['bg']=='':
                        bg=None
                    else:
                        bg=elem['bg']





                    

                    self_grid[row][col]=elem['grid_id']

                    fg=elem['fg']
                    
                    size=images1[b[row][col]].size
                    
                    map1.rectangle((self.col_width*col,
                                    self.row_height*row,
                                    self.col_width*col+size[0],
                                    self.row_height*row+size[1]),
                                    fill=bg,
                                   width=-1)
                                    
                                    




                                    
                    map1.bitmap((self.col_width*col,
                                 self.row_height*row
                                 ),
                                bitmap=images1[b[row][col]],
                                fill=fg)

        #add text to image
        '''for i in t_style:
            print('stylesss',i.attrib)'''

        for i in c_t_style:
            #print('ct style',i)
            
            _t=i.attrib
            _style_id=int(_t['style'])
            _style_dict=t_style[int(_style_id)].attrib
            _t_size=int(int(_style_dict['size'])*1.3)
            _t_color=_style_dict['color']

            fnt=ImageFont.truetype(font='arial',size=_t_size)

            map1.text((int(_t['cx']),int(_t['cy'])),
                      text=_t['text'],font=fnt,fill=_t_color)
            
            
            #print('textsss',i.attrib)

        #map1.text
        

        self.map_=ImageTk.PhotoImage(image=map0)

        self.grid=self_grid
        self.m_grid=[]
        for j in self.grid:
            a=[]
            for i in j:
                a.append([])
            self.m_grid.append(a)
        print('self.grid',len(self.grid),len(self.grid[0]))
        print('self.m_grid',len(self.m_grid),len(self.m_grid[0]))
            
                

        
            
                

        self.c.create_image(0,0,anchor='nw',image=self.map_,tags=('map',))
        

        



                        





if __name__=='__main__':
    root=tk.Tk()

    g=Start_Game(root)

    #print(g.__repr__())


    root.mainloop()





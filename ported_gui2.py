# PyDia Latex plugin 
# Copyright (c) 2018, Adi man
#
#  This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import dia, math, string
import pygtk
#from EpsImagePlugin import split
#from test.test_cookie import cases
pygtk.require("2.0")
import gtk
import os
import csv


def tex_compile(latex_string,Ind,build_d,Miktex_path):
    tex_code = ""
    tex_code = tex_code + """
\\documentclass[
multi={mymath},
border=0pt
]{standalone}

\\usepackage{anyfontsize}
    
\\newenvironment{mymath}{$\displaystyle}{$}
    
\\begin{document}
    
\\begin{mymath} 
{\\fontsize{60}{72} \\selectfont """+latex_string+"""}
\\end{mymath}
    
\\end{document}
"""
    out_file = build_d+str(Ind)
    if not os.path.exists(build_d):  # create the build directory if not existing
        os.makedirs(build_d)
    print build_d
    print tex_code
    f=open(out_file+".tex",'w')  # saves tex_code to output file
    f.write(tex_code)
    f.close()
    os.system(Miktex_path+"latex.exe -output-directory \""""+os.path.normpath(build_d)+"\" \""+os.path.realpath(out_file)+"\"")
    os.system(Miktex_path+"latex.exe -output-directory \""""+os.path.normpath(build_d)+"\" \""+os.path.realpath(out_file)+"\"")
    os.system(Miktex_path+"dvipng.exe -D 900 -bg Transparent -o \""""+os.path.realpath(out_file+".png")+"\" \""+os.path.realpath(out_file+".dvi")+"\"")
    return os.path.realpath(out_file+".png")

def savedB(fil_path,applist,not_loaded):
    f=open(fil_path, "wa")
    csvwriter = csv.writer(f)
    for i in range(0,len(applist)):
        if applist[i].get_ind()>0:
            csvwriter.writerow([applist[i].get_ind(),applist[i].entered_val,applist[i].image_loc])
    for i in range(0,len(not_loaded)):
            csvwriter.writerow(not_loaded[i])
    f.close()

class FrameObject :
    def __init__(self, wino, d, data) :
        self.diagram = d
        self.data = data
        self.Index=0 #this acts like an identity
        self.arr_pos=0 #this is the position in the array of loaded objects
        self.wino=wino
        self.entered_val=""
        self.image_loc="./test/1.png"
        self.dia_object=""

        self.frm = gtk.Frame()
        self.frm.show()
        
        wino.box_out.pack_start(self.frm)


        self.box1 = gtk.HBox()
        self.frm.add(self.box1)
#        win.add(box1)
        self.box1.show()

        self.box2 = gtk.HBox(spacing=10)
        self.box2.set_border_width(10)
        self.box1.pack_start(self.box2, expand=0)
        self.box2.show()
        
        self.entry = gtk.Entry()
        self.entry.set_text("0.0")
        self.box2.pack_start(self.entry)
        self.entry.show()

        self.button = gtk.Button("Preview")
        self.button.connect("clicked", self.call_tex_compile)
        self.box2.pack_start(self.button)
        self.button.set_flags(gtk.CAN_DEFAULT)
        self.button.grab_default()
        self.button.show()
        
        self.buttonP = gtk.Button("Delete")
        self.buttonP.connect("clicked",  self.del_row)
        self.box2.pack_start(self.buttonP)
        self.buttonP.set_flags(gtk.CAN_DEFAULT)
        self.buttonP.grab_default()
        self.buttonP.show()
        
        self.image1 = gtk.Image()
        self.update_image()
        
    def call_tex_compile(self, *args):
        self.entered_val=self.entry.get_text()
        self.image_loc=tex_compile(self.entered_val,self.Index,self.wino.project+self.wino.build_d,self.wino.Miktex_path)
#        self.on_rotate(self, *args)
#        imloc=tex_compile(self.entry.get_text(),1,self.build_d,self.Miktex_path)
#        print self.entry.get_text()
        self.update_image()
        self.dia_object.properties['image_file']=self.image_loc
        self.wino.data.update_extents()
        savedB(self.wino.db_fil,self.wino.applist,self.wino.not_loaded)
#        t=diagram.get_sorted_selected()
    def update_image(self):
        self.image1.clear()
#        self.image1 = gtk.Image()
        self.image1.set_from_file(self.image_loc)
        self.box2.pack_start(self.image1)
        self.image1.show()
        
    def del_row(self,*args):
        #Ind=self.Index
        Ind=self.arr_pos
        self.wino.del_routine(Ind+1)
    
    def set_ind(self,ind,arr_pos):
        self.Index=ind
        self.arr_pos=arr_pos
        
    def get_ind(self):
        return self.Index
        
    def on_delete (self, *args) :
        self.win.destroy ()

class LatexObjectDialog :
    def __init__(self, d, data) :
        self.Miktex_path="C:\\"+""""Program Files"\\"MiKTeX 2.9"\\miktex\\bin\\x64\\"""
        
        self.applist=[]
        self.no_apps=0 #number of objects loaded.
        self.no_apps_nl=0 #number of objects not loaded.
        self.unused_ind=[]
        
        win = gtk.Window()
        win.connect("delete_event", self.on_delete)
        win.set_title("Latex plugin")

        self.diagram = d
        self.data = d.data
        self.win = win
        self.dia_obj_filpath=[]
        self.not_loaded=[]
        
        self.obj_list=self.data.get_sorted_selected()
        
        load_all=True
        
        if self.obj_list:
            load_all=False
        else:
            self.obj_list=self.data.layers[0].objects #change it all layers
  
#sort images
        temp=[]
        #dia_obj_filpath=[]
        for i in range(0,len(self.obj_list)):
            if str(self.obj_list[i].type)=="Standard - Image":
                temp=temp+[self.obj_list[i]]
                shrt_path=os.path.normpath(self.obj_list[i].properties.get('image_file').value)
                spl=shrt_path.split('\\')
                s='\\'
                shrt_path=s.join(spl[(len(spl)-2):(len(spl))])
                self.dia_obj_filpath=self.dia_obj_filpath+[shrt_path]
        self.obj_list=temp
        
        print self.obj_list
        print self.dia_obj_filpath
        
        #dlg.obj_list[1].properties['image_file']='C:\\Users\\User\\Pictures\\images\\3.png'
        self.Seperator="/"
        #project = "./" # specify the project folder
        if os.name=='nt': #if windows
            self.Seperator="\\"            
        project=self.Seperator 
        dia_fil=self.diagram.filename
        spl=dia_fil.split(self.Seperator)
        project=project.join(spl[0:(len(spl)-1)])
        self.project=project+self.Seperator
        spl=spl[-1].split(".")
        self.build_d = spl[0]+self.Seperator
        if not os.path.exists(os.path.normpath(self.project+self.build_d)):
            os.makedirs(os.path.normpath(self.project+self.build_d))     
        self.db_fil=self.project+self.build_d+"dBfil.csv"
        f = open(self.db_fil, 'a+')
        f.close()
        print project
        print self.project
        print self.db_fil
        self.sw = gtk.ScrolledWindow()
#        self.win.add(sw)
        
#        self.darea = gtk.DrawingArea()
        #darea.connect("expose-event", self.expose)
        self.win.add(self.sw)
        self.box_out = gtk.VBox()
        
        self.box_add = gtk.HBox(spacing=10)
        self.box_add.show()
        self.box_add.pack_start(self.box_out, expand=0)

#        frm.add(box1)
#        win.add(box1)
        self.box_out.show()
        
        self.button_add = gtk.Button("Add")
        self.button_add.connect("clicked", self.Add_latex_object)
        self.box_add.pack_start(self.button_add)
        self.button_add.set_flags(gtk.CAN_DEFAULT)
        self.button_add.grab_default()
        self.button_add.show()
        self.sw.add_with_viewport(self.box_add)
        #loaddB()
        if os.path.isfile(self.db_fil):
            self.loaddB(self.db_fil,self.dia_obj_filpath,load_all)
#        FrameObject(self,d,data)
        self.win.show_all()
    
    def on_delete (self, *args) :
        self.no_apps=0
        self.win.destroy ()
        
    def del_routine(self,Ind):
        layer = self.data.active_layer
        layer.remove_object(self.applist[Ind-1].dia_object)
        self.unused_ind.append(self.applist[Ind-1].get_ind())
        self.applist[Ind-1].button.destroy()
        self.applist[Ind-1].entry.destroy()
        self.applist[Ind-1].buttonP.destroy()
        self.applist[Ind-1].image1.destroy()
        self.applist[Ind-1].box2.destroy()
        self.applist[Ind-1].box1.destroy()
        self.applist[Ind-1].frm.destroy()
        self.applist[Ind-1].set_ind(0,0)
        self.applist[Ind-1].entered_val=""
#        self.applist[Ind-1].label.destroy()
        self.no_apps=self.no_apps-1        
        savedB(self.db_fil,self.applist,self.not_loaded)
        print "in delete"+str(len(self.applist))  
        
    def ret_int_var(self, ret_var_ind):
        switcher={
            1:self.applist,
            2:self.no_apps
                }
        return switcher.get(ret_var_ind, "")
    
    def Add_row(self):
        already_set=0
        self.no_apps=self.no_apps+1
        row_num=0
        for i in range(0,len(self.applist)):
            if self.applist[i].get_ind()==0:
                self.applist[i]=FrameObject(self,self.diagram,self.data)
                already_set=1
                row_num=i
                #self.applist[i].set_ind(self.no_apps+self.no_apps_nl,row_num)
                #                self.applist[i].frame.grid(row=i+1, column=0)
                #row_obj(self.applist[i])
                break
        if already_set==0:
            self.applist=self.applist+[(FrameObject(self,self.diagram,self.data))]
            row_num=self.no_apps-1
            #self.applist[-1].set_ind(self.no_apps+self.no_apps_nl,row_num)
            
        return row_num
#            self.applist[-1].frame.grid(row=self.no_apps, column=0)
#        savedB(self.db_fil,self.applist)
#            row_obj(self.applist[-1])

    def loaddB(self,fil_path,dia_obj_filpath,load_all):
        used_ind=[]
        f=open(fil_path, "r")
        csvreader = csv.reader(f)
        for row in csvreader:
            if row:
                used_ind.append(int(row[0]))
                shrt_path=os.path.realpath(row[2])
                spl=shrt_path.split(self.Seperator)
                s=self.Seperator
                shrt_path=s.join(spl[(len(spl)-2):(len(spl))])
                set_already=False
                for ind in range(0,len(dia_obj_filpath)):
                    if shrt_path==dia_obj_filpath[ind]:
                        row_num=self.Add_row()
                        self.applist[row_num].Index=str(row[0])
                        self.applist[row_num].entered_val=str(row[1])
                        self.applist[row_num].entry.set_text(str(row[1]))
                        self.applist[row_num].image_loc=os.path.realpath(row[2])
                        self.applist[row_num].update_image()
                        self.applist[row_num].dia_object=self.obj_list.pop(ind)
                        del dia_obj_filpath[ind]
                        set_already=True
                        break
                if not set_already:
                    if load_all:
                        row_num=self.Add_row()
                        self.applist[row_num].Index=str(row[0])
                        self.applist[row_num].entered_val=str(row[1])
                        self.applist[row_num].entry.set_text(str(row[1]))
                        self.applist[row_num].image_loc=os.path.realpath(row[2])
                        self.applist[row_num].update_image()
                        #Need to write code to create image in dia
                        ot = dia.get_object_type("Standard - Image")
                        o, h1, h2 = ot.create (0,0)
                        o.properties['image_file']=os.path.realpath(row[2])
                        layer = self.data.active_layer
                        layer.add_object(o)
                        layer.update_extents()
                        self.data.update_extents()
                        self.applist[row_num].dia_object=o
                    else:
                        self.no_apps_nl=self.no_apps_nl+1
                        self.not_loaded=self.not_loaded+[row]
        f.close()
        if used_ind:
            all_ind=range(1,max(used_ind)+1)
            self.unused_ind=[x for x in all_ind if x not in used_ind]
        savedB(self.db_fil,self.applist,self.not_loaded)
        
    def Add_latex_object(self,*args):
        row_num=self.Add_row()
        def_val="0.0"
        if not self.unused_ind:
            self.applist[row_num].set_ind(self.no_apps+self.no_apps_nl,row_num)
        else:
            self.applist[row_num].set_ind(self.unused_ind.pop(),row_num)
        self.applist[row_num].entered_val=def_val
        self.applist[row_num].entry.set_text(def_val)
        self.applist[row_num].image_loc=tex_compile(def_val,self.applist[row_num].get_ind(),self.project+self.build_d,self.Miktex_path)
        #tex_compile(self.entered_val,self.Index,self.wino.project+self.wino.build_d,self.wino.Miktex_path)
        self.applist[row_num].update_image()
        ot = dia.get_object_type("Standard - Image")
        o, h1, h2 = ot.create (0,0)
        o.properties['image_file']=self.applist[row_num].image_loc
        layer = self.data.active_layer
        layer.add_object(o)
        layer.update_extents()
        self.data.update_extents()
        self.applist[row_num].dia_object=o
        savedB(self.db_fil,self.applist,self.not_loaded)        
        


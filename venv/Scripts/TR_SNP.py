#=====================================================================================================
#=====================================================================================================
#an interface to select tree ring data form the cleaned version of ITRDB and create a sub-dataset
#can be selected by year in this first version
#created by Yizhao Chen 2019/6/5   Win10/Python 3.7.3/Pycharm 2019.1.2
#test version update 2019/6/10
#put regions and species as options
#lat,lon options
#test version update 2019/6/14
#remove the lat,lon options temporally, need better logic representation
#link the selected dataset to a plot function
#need to put the functions into classes
#test version update 2019/6/17
#add a selection in "plot" button to plot the result from all data selected
#refine the plot scheme: add labels and legend
#test version update 2019/6/18
#output the plot data as .csv files
#add setup.py to build excutable & installation files
#give dpi to the output plot file
#test version update 2019/7/1
#add the button to plot the custmized dataset directly
#test version update 2019/12/22
#add the exact lat/lon input for global synthesis
#=====================================================================================================
#=====================================================================================================

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from shutil import copyfile
import fnmatch
import os

#local functions
import GFNWE
import open_metafile
import plot_all_temporal
from plot_all_temporal import *
from plot_all_allometry import *
from plot_age_only import *
#import search_reorganize

#for rpy2 test Yizhao 2019/7/2
import platform
import rpy2.situation
#for rpy2 test Yizhao 2019/7/3
import sys

#define the global variables
#namelist =[]
returnlist = []
namelist = []
global year_in
global year_out
global lat_in
global lon_in
global comboxlist
global comboxlist1
global comboxlist2
global fd

#for rpy2 test Yizhao 2019/7/2
#lib_path = rpy2.situation.get_r_home()
#print(lib_path)
#for rpy2 test Yizhao 2019/7/3
if getattr(sys, 'frozen', False):
    # The application is frozen
    # reset R_HOME and try to find a R installation using the fallback mechanisms
    del os.environ['R_HOME']
    os.environ['R_HOME'] = rpy2.situation.get_r_home()
lib_path = rpy2.situation.get_r_home()
print(lib_path)


def metafile():    #read the metafile
    year_in = entry.get()
    year_out = entry1.get()
    lat_in = entry2.get()
    lon_in = entry3.get()
    #lat_s = entry2.get()
    #lat_e = entry3.get()
    #lon_s = entry4.get()
    #lon_e = entry5.get()
    reg_in = comboxlist1.get()
    spec_in = comboxlist.get()
    print(reg_in)
    mf = filedialog.askopenfilename()
    #namelist = open_metafile.om(mf, year_in, year_out, reg_in,spec_in)
    #namelist = open_metafile.om(mf,year_in,year_out,lat_s,lat_e,lon_s,lon_e,reg_in,spec_in)
    namelist = open_metafile.om(mf, year_in, year_out, lat_in, lon_in, reg_in, spec_in)
    print(namelist)
    #print(year_in)
    #print(year_out)
    #print(spec_in)
    return namelist
  #open metafile


def select_folder():
    fd = filedialog.askdirectory()
    print(fd)
    return fd

#def select_region():
def search_create():
    returnlist = metafile()
    if returnlist == []:                                      #no matched data
        messagebox.showerror("error","no data fit")
        return
    fd = filedialog.askdirectory(title = "select the target repository") #select_folder()
    if not entry.get() or not entry1.get():             #to check if the inputs of years
        messagebox.showerror("error","plz enter years")         #pump a box out
        return                                          #end if nothing there
    if fd == "":
        messagebox.showerror("error", "plz select the target repository")
        return

    with open(fd+"//sub_log.txt",'w') as f:
        for i in range(0,len(returnlist)):
            f.write(str(returnlist[i]))
            f.write('\n')
    path = filedialog.askdirectory(title = "select the source repository")
    if path == "":
        messagebox.showerror("error", "plz select the source repository")
        return
    else:
    #path = "D:\MEGA\Live_cases\Hybrid\Tree_ring_data_collection_NOAA_ITRDB\Appendix S1\Cleaned datasets\itrdb-v713-cleaned-rwl"
        path_list = os.walk(path)
        for root, dirs, files in path_list:
            flength = len(files)
            for i in range(0,flength):
                fname = GFNWE.getFileNameWithoutExtension(files[i])
                fname1 = files[i]
                if fname in returnlist:
                    copyfile(root+"\\"+ fname1,fd+"\\"+fname1)
                    dir = fd + "\\" + fname1
                    print(fname1)                #the select files
        plot_R(fd,returnlist,fname1)
    #Button(text='save', command=lambda:plot_R(returnlist)).grid(row=1, column=4)

def plot_R(fd,returnlist,fname1):
    Button(text='plot', command=lambda:on_click(fd,returnlist,fname1)).grid(row=1, column=4)
    #window pop-up for plot
    #print(returnlist)

def on_click(fd,returnlist,fname1):
    tl = Toplevel()
    tl.geometry('300x100')
    comvalue2 = tk.StringVar()
    #Label(tl, text='test').pack()
    comboxlist2 = ttk.Combobox(tl,textvariable=comvalue2)  # 初始化
    #comboxlist2.bind("<<ComboboxSelected>>",getvaluetest)
    returnlist.insert(0,"all")
    comboxlist2["values"] = returnlist
    comboxlist2.grid(row=1,column = 5)
    print(returnlist)
    comboxlist2.current(0)  #select the first one as default
    #kk = comboxlist2.get()
    tk.Button(tl, text='go', command=lambda: plot_all(fd,comboxlist2.get(),returnlist)).grid(row=2,column =5)
    #go(comboxlist2,fd,fname1)
    tl.wait_window()
    return


#a temporal module to plot the customized tree ring data directly
#add BAI(basal area increment) plot Yizhao 2019/7/10
def file_select():
    fk = filedialog.askopenfilenames(title = "select TR files")
    print(fk)
#add lat_in lon_in for global synthesis 2019/12/22
    #for TRW
    #plot_all(fk)
    #for biomass
    plot_allometry(fk)
    #for age
    #plot_age_only(fk)

#interface design
root = Tk()
root.title('ITRDB_search')      #create an interface
root.geometry('650x100')       #size and position

#select by year
Label(text='start year：    ').grid(row=0,column=0)
entry = Entry()#enter the start year
entry.grid(row=0,column=1)#position for entry
Label(text='end year：    ').grid(row=0,column=2)
entry1 = Entry()#enter the end year
entry1.grid(row=0, column=3)#position for entry1

#select by lat/lon
#Label(text='lat_s：    ').grid(row=1,column=0)
#entry2 = Entry()#enter the start year
#entry2.grid(row=1,column=1)#position for entry2
#Label(text='lat_e:    ').grid(row=1,column=2)
#entry3 = Entry()#enter the end year
#entry3.grid(row=1, column=3)#position for entry3
#Label(text='lon_s：    ').grid(row=2,column=0)
#entry4 = Entry()#enter the start year
#entry4.grid(row=2,column=1)#position for entry4
#Label(text='lon_e:    ').grid(row=2,column=2)
#entry5 = Entry()#enter the end year
#entry5.grid(row=2, column=3)#position for entry5

#select by single lat/lon
Label(text='lat：    ').grid(row=1,column=0)
entry2 = Entry()#enter lat
entry2.grid(row=1,column=1)#position for entry2
Label(text='lon:    ').grid(row=1,column=2)
entry3 = Entry()#enter the end year
entry3.grid(row=1, column=3)#position for entry3

#region combobox
Label(text='region    ').grid(row=2,column=0)
comvalue1 = tk.StringVar()
comboxlist1=ttk.Combobox(root,textvariable=comvalue1) #初始化
comboxlist1["values"]=("all","africa","asia","australia","canada","europe","mexico","southamerica","usa")
comboxlist1.grid(row=2,column=1)
comboxlist1.current(0)  #选择第一个

#species combobox
Label(text='species    ').grid(row=2,column=2)
comvalue = tk.StringVar()
comboxlist=ttk.Combobox(root,textvariable=comvalue) #初始化
comboxlist["values"]=("all","ABAL","ABAM","ABBA","ABBO","ABCE","ABCI","ABCO","ABFO","ABLA","ABMA","ABNO",
                      "ABPI","ABPN","ABRC","ABSB","ABSP","ACRU","ACSH","ADHO","ADUS","AGAU","ARAR",
                      "ATCU","ATSE","AUCH","BELE","BEPU","BEUT","CABU","CACO","CADE","CADN","CASA",
                      "CDAT","CDBR","CDDE","CDLI","CEAN","CEBR","CEMC","CESP","CHER","CHLA","CHNO",
                      "CHOB","CMJA","CPBE","CUCH","CYGL","CYOV","DABI","div.DRLO","FAGR","FASY",
                      "FICU","FOHO","FREX","GOGL","HABI","HEHE","JUAU","JUEX","JUFO","JUOC","JUOS",
                      "JUPH","JUPR","JURE","JUSC","JUSP","JUTI","JUTU","JUVI","LADA","LADE","LAGM",
                      "LAGR","LALA","LALY","LAOC","LASI","LASP","LGFR","LIBI","LIDE","LITU","MIXD",
                      "NOBE","NOGU","NOPB","NOPD","NOPU","NOSO","PCAB","PCCH","PCEN","PCEX","PCGL",
                      "PCGN","PCLI","PCMA","PCOB","PCOM","PCOR","PCPU","PCRU","PCSH","PCSI","PCSM",
                      "PCSP","PCTI","PHAS","PHGL","PHTR","PIAL","PIAM","PIAR","PIAZ","PIBA","PIBN",
                      "PIBR","PICE","PICM","PICO","PICU","PIDE","PIEC","PIED","PIFL","PIGE","PIGR",
                      "PIHA","PIHE","PIHR","PIJE","PIKE","PIKO","PILA","PILE","PILO","PIMA","PIMG",
                      "PIMK","PIMR","PIMU","PIMZ","PINE","PINI","PIPA","PIPE","PIPI","PIPN","PIPO",
                      "PIPU","PIRE","PIRI","PIRO","PISF","PISI","PISP","PIST","PISY","PITA","PITB",
                      "PITO","PIUN","PIUV","PIVI","PIWA","PLRA","PPDE","PPGR","PPSP","PPTM","PPTR",
                      "PRMA","PROS","PSMA","PSME","PTAN","PTLE","QUAL","QUCA","QUCE","QUCF","QUCN",
                      "QUCO","QUDG","QUFA","QUFG","QUHA","QULO","QULY","QUMA","QUMC","QUMO","QUMU",
                      "QUPA","QUPE","QUPR","QUPU","QURO","QURU","QUSH","QUSP","QUST","QUVE","SALA",
                      "SAPC","species","TABA","TADI","TAMU","TEGR","THOC","THPL","TSCA","TSCR",
                      "TSDI","TSDU","TSHE","TSME","ULSP","VIKE","WICE")

comboxlist.grid(row=2,column=3)
comboxlist.current(0)  #select the first one as default
#comboxlist.bind("<<ComboboxSelected>>")  #绑定事件,(下拉列表框被选中时，绑定go()函数)
#comboxlist.pack()
#Button(text='select metafile',command=metafile).grid(row=1,column=0)   #read in the metafile
#Button(text='select target folder', command=select_folder).grid(row=1,column=1)        #select output folder
Button(text='search & create', command=search_create).grid(row=0,column=4) #search &create the target sub-dataset
#Button(text='select by region', command=select_region).grid(row=0,column=4) #search &create the target sub-dataset
#Button(text='plot', command=).grid(row=0,column=4) #search &create the target sub-dataset
Button(text='file_select', command=file_select).grid(row=4,column=4)
#Button(text='list_id',command=list_id).grid(row=2,column=2)            #put a id list to the target sub-dataset
loop = mainloop()#go!








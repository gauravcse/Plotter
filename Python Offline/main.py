from Tkinter import *
from ttk import *
import sqlite3 as sq
import tkMessageBox
import functools

class Data :
    def __init__(self,city,lat,lon) :
        self.city = city
        self.lat = lat
        self.lon = lon
    def getCity(self) :
        return self.city

class DataList :
    def __init__(self,filename) :
        self.item = list()
        self.inp = open(filename).read()
        self.line = self.inp.split("\n")
        for element in self.line :
            individual = element.split(",")
            data = Data(individual[0],float(individual[1]),float(individual[2]))
            self.item.append(data)
    def search(self,lat,lon) :
        self.city = list()
        for i in self.item :
            if(abs(i.lat - lat) <= 2.0 and abs(i.lon - lon) <= 2.0) :
                self.city.append(i)
                print i.city
        return self.city
    def getItem(self) :
        return self.item
    def length(self) :
        return len(self.item)
        


class Display :
    def __init__(self,width,height,dataList) :
        self.newDisplay = ""
        self.height = height
        self.width = width
        self.master = Tk("Plot")
        self.canvas = Canvas(self.master,width = self.width, height = self.height)
        self.canvas.grid(row = 3)
        self.var = IntVar()
        self.item = dataList
        self.scroll = Scrollbar()
        self.conn = sq.connect("cities.sqlite")
        self.cur = self.conn.cursor()
        self.currentCityList = list()
    def display(self) :
        self.l1 = Label(self.master, text="Latitude").grid(row=0,column=1)
        self.l2 = Label(self.master, text="Longitude").grid(row=1,column=1)
        self.l3 = Label(self.master, text="City Name").grid(row=0,column=3)
        self.e1 = Entry(self.master)
        self.e2 = Entry(self.master)
        self.e3 = Entry(self.master)
        self.e1.grid(row=0, column=2)
        self.e2.grid(row=1, column=2)
        self.e3.grid(row=0, column=4)
        Button(self.master, text='Quit', command=self.master.quit).grid(row=2, column=4, sticky=W, pady=4)
        Button(self.master, text='Show', command=self.show_entry_fields).grid(row=2, column=3, sticky=W, pady=4)
        self.r1 = Radiobutton(self.master,text="By Name",variable=self.var,value=1,command=self.radioclick)
        self.r2 = Radiobutton(self.master,text="By Coordinates",variable=self.var,value=2,command=self.radioclick)
        self.r1.grid(row=2,column=1)
        self.r2.grid(row=2,column=2)
        self.img = PhotoImage(file="map.gif")
        self.canvas.create_image(0,0,anchor=NW,image=self.img)
        tv = Treeview(self.master)
        tv['columns'] = ('city','latitude', 'longitude','elevation','population','precipitation','prec_days','humidity','area','high','mean','low')
        #tv.heading("#0", text='City', anchor='w')
        #tv.column("#0", anchor="w")
        tv.heading('city', text='City Name')
        tv.column('city', anchor='center', width=75)
        tv.heading('latitude', text='Latitude')
        tv.column('latitude', anchor='center', width=50)
        tv.heading('longitude', text='Longitude')
        tv.column('longitude', anchor='center', width=50)
        tv.heading('longitude', text='Longitude')
        tv.column('longitude', anchor='center', width=50)
        tv.heading('elevation', text='Elevation')
        tv.column('elevation', anchor='center', width=50)
        tv.heading('population', text='Population')
        tv.column('population', anchor='center', width=50)
        tv.heading('precipitation', text='Precipitation')
        tv.column('precipitation', anchor='center', width=50)
        tv.heading('prec_days', text='Prec Days')
        tv.column('prec_days', anchor='center', width=50)
        tv.heading('humidity', text='Humidity')
        tv.column('humidity', anchor='center', width=50)
        tv.heading('area', text='Area')
        tv.column('area', anchor='center', width=50)
        tv.heading('high', text='Year High')
        tv.column('high', anchor='center', width=50)
        tv.heading('mean', text='Year Mean')
        tv.column('mean', anchor='center', width=50)
        tv.heading('low', text='Year Low')
        tv.column('low', anchor='center', width=50)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.scroll.configure(command = self.treeview.xview)
        self.treeview.configure(xscrollcommand = self.scroll.set)
        self.treeview.grid(row = 3,column = 1,columnspan = 4)
        mainloop()
    def radioclick(self) :
        print self.var.get()
    def show_entry_fields(self) :
        if self.var.get() == 2 :
            self.lat = float(self.e1.get())
            self.lon = float(self.e2.get())
            self.allcities = self.item.search(self.lat,self.lon)
            self.showCities(self.allcities,self.lat,self.lon)
        else :
            self.lat,self.lon = 0.0,0.0
            for city in self.item.item :
                if(city.city == self.e3.get()) :
                    self.lat = city.lat
                    self.lon = city.lon
                    break
            self.allcities = self.item.search(self.lat,self.lon)
            self.showCities(self.allcities,self.lat,self.lon)

    def showCities(self,citylist,lat,lon) :
        self.currentCityList = list()
        r = 3
        for city in citylist :
            pix_X = city.lat - 6.4
            pix_Y = city.lon - 68.7
            X = int(pix_X * 17.8)
            Y = int(pix_Y * 16.8)
            X = 555 - X
            #print 'City : {} \nLatitude : {}\nLongitude : {}'.format(city.city,X,Y)
            if(abs(city.lat - lat) <= 1.0 and abs(city.lon - lon) <= 1.0) :
                self.canvas.create_oval ( Y-r, X-r, Y+r, X+r,fill="#ff0000",tags=city.city)
                self.canvas.tag_bind(city.city, '<ButtonPress-1>', functools.partial(self.onObjectClick, param=city.city))
            else :
                self.canvas.create_oval ( Y-r, X-r, Y+r, X+r,fill="#00ff00",tags=city.city)
                self.canvas.tag_bind(city.city, '<ButtonPress-1>', functools.partial(self.onObjectClick, param=city.city))
            self.insertRow(city.city)
    def onObjectClick(self,event,param):
        vb = StringVar()
        print('Got object click', event.x, event.y)
        print(event.widget.find_withtag("current"))
        print(event.widget.find_closest(event.x, event.y))
        #label = Message(self.master,textvariable=vb)
        #vb.set(param)
        #label.grid(row=3,column=1,columnspan=3)
        listOfEntriesInTreeView = self.treeview.get_children()
        for each in listOfEntriesInTreeView:
            cit = str(self.treeview.item(each)["values"][0])
            if(cit == param) :
                print cit
                self.treeview.focus(each)
                self.newDisplay = NewDisplay(self.master,cit)
                self.newDisplay.display(self.item,self.currentCityList)

    def insertRow(self,city) :
        self.currentCityList.append(city)
        self.cur.execute("SELECT * FROM Cities WHERE city = ?",(city.rstrip(),))
        row = self.cur.fetchall()[0]
        self.treeview.insert('','end',text = row[1],values = (str(row[1]),str(row[6]),str(row[7]),str(row[4]),str(row[9]),str(row[16]),str(row[14]),str(row[15]),str(row[2]),str(row[11]),str(row[13]),str(row[12])))


class NewDisplay :
    def __init__(self,root,city) :
        self.root = root
        self.city = city
        self.scroll = Scrollbar()
        self.window = Toplevel(root)
        self.window.wm_title("%s" % city)
        self.conn = sq.connect("cities.sqlite")
        self.cur = self.conn.cursor()
        self.attribute = dict()
        self.columnList = ['','','Area Total (2)','Language (3)','Elevation (4)','Date Established (5)','Latitude (6)','Longitude (7)','Population Metro (8)','Population Total (9)','Leader Party (10)','Record High (11)','Record Low (12)','Record Mean (13)','Precipitation Days (14)','Humidity (15)','Precipitation (16)','Image (17)']
        self.dbcolumnList = ['','','area_total_km2','language','elevation','date_established','latitude','longitude','population_metro','population_total','leader_party','year_record_high','year_record_low','year_record_mean','precipitation_days','humidity','precipitation','image']
        
    def display(self,item,currentCityList) :
        self.citylist =  [item.getItem()[i].getCity() for i in xrange(item.length())]
        #var = StringVar()
        #var.set("%s" % self.city)
        labelMain = Label(self.window,text = self.city + " Null Values : ").grid(row = 0,column = 0)
        self.e1 = Entry(self.window)
        self.e2 = Entry(self.window)
        labelMain1 = Label(self.window,text = "Weighted Latitude").grid(row = 2,column = 2)
        labelMain2 = Label(self.window,text = "Weighted Longitude").grid(row = 3,column = 2)
        self.e1.grid(row = 2, column = 3)
        self.e2.grid(row = 3, column = 3)
        Button(self.window, text='Compute', command=functools.partial(self.show_entry_fields_weighted_topbottom,currentCityList)).grid(row = 3, column = 4, sticky = W, pady = 4)
        self.index = self.checkNull()
        self.nullist = "  "
        for i in xrange(len(self.index)) :
            self.nullist = self.nullist + " , " + self.columnList[self.index[i]]
        labelNull = Label(self.window,text = self.nullist).grid(row = 0,column = 1)
        self.cur.execute("SELECT city, " + self.dbcolumnList[self.index[0]] + " FROM Cities")#,(self.dbcolumnList[self.index[0]],))
        self.tv = Treeview(self.window)
        self.tv['columns'] = ('city',self.dbcolumnList[self.index[0]])
        self.tv.heading('city', text='City Name')
        self.tv.column('city', anchor='center', width=100)
        self.tv.heading(self.dbcolumnList[self.index[0]], text=self.columnList[self.index[0]])
        self.tv.column(self.dbcolumnList[self.index[0]], anchor='center', width = 200)
        self.scroll.configure(command = self.tv.yview)
        self.tv.configure(yscrollcommand = self.scroll.set)
        self.tv.grid(row = 1,column = 0,columnspan = 2)
        rows = self.cur.fetchall()
        for row in rows :
            if row[0] in currentCityList :
                self.tv.insert('','end',text = row[0],values = (str(row[0]),str(row[1])))
                #tup = (str(row[0]),str(row[1]))
                self.attribute[str(row[0])] = str(row[1])
    def checkNull(self) :
        self.cur.execute("SELECT * FROM Cities WHERE city = ?",(self.city.rstrip(),))
        row = self.cur.fetchall()[0]
        index = list()
        for i in xrange(2,17) :
            if row[i] is None :
                index.append(i)
        return index

    def show_entry_fields_weighted_topbottom(self,currentCityList) :
        latweight = float(self.e1.get())
        lonweight = float(self.e2.get())
        print latweight,lonweight
        

if __name__ == "__main__" :
    data = DataList("city.txt")
    disp = Display(479,555,data)
    disp.display()
    

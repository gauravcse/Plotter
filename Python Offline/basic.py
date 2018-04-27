from Tkinter import *
import sqlite3 as sq
import tkMessageBox
import functools

canvas_width = 479
canvas_height = 555
item = list()

option = False  #If false latitude and longitude is default else City Name

class Data :
    def __init__(self,city,lat,lon) :
        self.city = city
        self.lat = lat
        self.lon = lon

def filllist() :
    inp = open("city.txt").read()
    line = inp.split("\n")
    for element in line :
        individual = element.split(",")
        data = Data(individual[0],float(individual[1]),float(individual[2]))
        item.append(data)
filllist()


master = Tk("Plot")
canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.grid(row=3)
var = IntVar()

def search(lat,lon) :
    city = list()
    for i in item :
        if(abs(i.lat - lat) <= 2.0 and abs(i.lon - lon) <= 2.0) :
            city.append(i)
            print i.city
    return city

def onObjectClick(event,param):
    vb = StringVar()
    print('Got object click', event.x, event.y)
    print(event.widget.find_withtag("current"))
    print(event.widget.find_closest(event.x, event.y))
    label = Message(master,textvariable=vb)
    vb.set(param)
    label.grid(row=3,column=1,columnspan=3)
    
def showCities(citylist,lat,lon) :
    r = 3
    for city in citylist :
        pix_X = city.lat - 6.4
        pix_Y = city.lon - 68.7
        X = int(pix_X * 17.8)
        Y = int(pix_Y * 16.8)
        X = 555 - X
        #print 'City : {} \nLatitude : {}\nLongitude : {}'.format(city.city,X,Y)
        if(abs(city.lat - lat) <= 1.0 and abs(city.lon - lon) <= 1.0) :
            canvas.create_oval ( Y-r, X-r, Y+r, X+r,fill="#ff0000",tags=city.city)
            canvas.tag_bind(city.city, '<ButtonPress-1>', functools.partial(onObjectClick, param=city.city))
        else :
            canvas.create_oval ( Y-r, X-r, Y+r, X+r,fill="#00ff00",tags=city.city)
            canvas.tag_bind(city.city, '<ButtonPress-1>', functools.partial(onObjectClick, param=city.city))

def show_entry_fields() :
    global option
    print option
    #print 'Latitude : {}\nLongitude : {}'.format(e1.get(),e2.get())
    if option is False :
        lat = float(e1.get())
        lon = float(e2.get())
        allcities = search(lat,lon)
        showCities(allcities,lat,lon)
    else :
        lat,lon = 0.0,0.0
        for city in item :
            if(city.city == e3.get()) :
                lat = city.lat
                lon = city.lon
                break
        allcities = search(lat,lon)
        showCities(allcities,lat,lon)

def radioclick() :
    global option
    if(var.get() == 1) :
        option = True   #By Name
    else :
        option = False  #By Coordinates
    print var.get(),option

l1 = Label(master, text="Latitude").grid(row=0,column=1)
l2 = Label(master, text="Longitude").grid(row=1,column=1)
l3 = Label(master, text="City Name").grid(row=0,column=3)
e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e1.grid(row=0, column=2)
e2.grid(row=1, column=2)
e3.grid(row=0, column=4)
Button(master, text='Quit', command=master.quit).grid(row=2, column=4, sticky=W, pady=4)
Button(master, text='Show', command=show_entry_fields).grid(row=2, column=3, sticky=W, pady=4)
r1 = Radiobutton(master,text="By Name",variable=var,value=1,command=radioclick)
r2 = Radiobutton(master,text="By Coordinates",variable=var,value=2,command=radioclick)
r1.grid(row=2,column=1)
r2.grid(row=2,column=2)

img = PhotoImage(file="map.gif")
canvas.create_image(0,0,anchor=NW,image=img)


mainloop()


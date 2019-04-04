import matplotlib
import matplotlib.animation as animation
import time as t
import mysql.connector
from matplotlib import style
from threading import Thread
from tkinter import*
from tkinter import messagebox as msg
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


global p
p=0
global bp
bp=0
global count
count=0
def prescribe(entry):
    pre = mysql.connector.connect(host="localhost",user="root",passwd="",database=UID)
    precursor = pre.cursor()
    doc = mysql.connector.connect(host="localhost",user="root",passwd="",database='reception_desk')
    doccursor = doc.cursor()
    doccursor.execute("SELECT * FROM doctor_shift")
    docresult = doccursor.fetchall()
    now=int(t.ctime()[11:13])
    now=int(now/8)
    tt="Dr. "+docresult[now][0]
    sql = "INSERT INTO prescription_record (date ,time ,doctor , prescription) VALUES (%s,%s,%s, %s)"
    val = (t.ctime()[:10]+t.ctime()[19:],t.ctime()[11:19],tt,entry)
    precursor.execute(sql, val)
    pre.commit()
    report()
    
def report():
    j=0
    pre = mysql.connector.connect(host="localhost",user="root",passwd="",database=UID)
    precursor = pre.cursor()
    precursor.execute("SELECT * FROM prescription_record")
    preresult = precursor.fetchall()
    for i in range(len(preresult)-1,-1,-1):
        j=j+1
        if(j<6):
            tt=preresult[i][3]+" by "+preresult[i][2]+" at "+preresult[i][1]
            Label(ICU,text="                                                  ",font='Helvatica 18',bg='grey',fg="black").place(x=1355,y=610-(40*j),anchor='se')
            Label(ICU,text=tt,font='Helvatica 18',bg='grey',fg="black").place(x=1355,y=610-(40*j),anchor='se')
    doc = mysql.connector.connect(host="localhost",user="root",passwd="",database='reception_desk')
    doccursor = doc.cursor()
    doccursor.execute("SELECT * FROM doctor_shift")
    docresult = doccursor.fetchall()
    now=int(t.ctime()[11:13])
    now=int(now/8)
    tt="Dr. "+docresult[now][0]
    tt1="Specialised in "+docresult[now][3]
    tt2="Contact :- "+docresult[now][2]
    Label(ICU,text=tt,font='Helvatica 18',bg="steelblue1",fg="black").place(x=960,y=180,anchor='sw')
    Label(ICU,text=tt1,font='Helvatica 18',bg="steelblue1",fg="black").place(x=960,y=210,anchor='sw')
    Label(ICU,text=tt2,font='Helvatica 18',bg="steelblue1",fg="black").place(x=960,y=240,anchor='sw')
    
def msg_em():
    #set alarm to trigger
    msg.showinfo('Emergency','Alarm Triggered')
    
def msg_rp():
    msg.showinfo('Called Reception','Nurse Will be there in a moment')
    rp = mysql.connector.connect(host="localhost",user="root",passwd="",database='reception_desk')
    rpcursor = rp.cursor()
    sql = "INSERT INTO Call_updates (Date ,Time,UID) VALUES (%s,%s, %s)"
    val = (t.ctime()[:10]+t.ctime()[19:],t.ctime()[11:19],UID)
    rpcursor.execute(sql, val)
    rp.commit()
    
def back():
    #link main window
    ICU.destroy()
    
def animate(i):
    i=[]
    j=[]
    k=[]
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database=UID)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Readings")
    myresult = mycursor.fetchall()
    for x in range(len(myresult)-1,len(myresult)-10,-1):
        i.append(myresult[x][1][3:])
        j.append(myresult[x][2])
        k.append(myresult[x][3])
    i=i[::-1]
    #j=j[::-1]
    k=k[::-1]
    ax1.clear()
    ax2.clear() 
    ax1.plot(i,j)
    ax2.plot(i,k)


def update(mydb,mycursor):
    global p
    global bp
    global count
    count=count+1
    sql = "INSERT INTO Readings (DATE ,TIME , PULSE ,BP) VALUES (%s,%s, %s,%s)"
    val = (t.ctime()[:10]+t.ctime()[19:],t.ctime()[11:19],p,bp)
    mycursor.execute(sql, val)
    mydb.commit()
    if(int(count/8)==0):
        p=p+1
        bp=bp+1
    elif(count==15):
        count=0
    elif(int(count/8)==1):
        p=p-1
        bp=bp-1
    t.sleep(1)
    update(mydb,mycursor)

    
available_id=[]
global UID
#UID="a"+input('Enter your UID')
UID='atest13'

mydb = mysql.connector.connect(host="localhost",user="root",passwd="")
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    available_id.append(x[0])
if((UID in available_id)==True):
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database=UID)
    mycursor = mydb.cursor()
    
    style.use('ggplot')
    f= Figure(figsize=(6,7), dpi=90)
    ax1= f.add_subplot(211)
    ax2=f.add_subplot(212)
    global ICU
    ICU=Tk()
    ICU.title('ICU')
    ICU.geometry('1200x700')
    ICU.configure(background="steelblue1")
    Label(ICU,text='\n ').place(x=0,y=130)
    Label(ICU,text='INTENSIVE CARE UNIT',font='Vemana2000 30 bold italic underline',bg="steelblue1",fg='green').place(x=420,y=10)
    Label(ICU,text='Patient Details',font='Helvatica 22 bold underline',bg="steelblue1",fg="black").place(x=560,y=85)
    Label(ICU,text='Doctor Appointed',font='Helvatica 22 bold underline',bg="steelblue1",fg="black").place(x=960,y=85)
    
    report()
    e=Entry(ICU,font='Arial 20 bold italic',width='30')
    e.place(x=680,y=624,anchor='sw')
    Button(ICU,text='Submit',font='Arial 19 bold italic',fg="blue",bg="black",width='10',height='1',command=lambda:prescribe(e.get())).place(x=1160,y=585)
    Button(ICU,text='Back',font='Arial 22 bold italic',fg="black",bg="green",width='10',height='1',command=back).place(x=660,y=640)
    Button(ICU,text='Reception',font='Arial 22 bold italic',fg="black",bg="green",width='10',height='1',command=msg_rp).place(x=910,y=640)
    Button(ICU,text='Emergency',font='Arial 22 bold italic',fg="black",bg="red",width='10',height='1',command=msg_em).place(x=1150,y=640)
    t2=Thread(target = update, args=(mydb,mycursor))
    t2.start()
    canvas= FigureCanvasTkAgg(f,ICU)
    canvas.draw()
    canvas.get_tk_widget().place(x=-30,y=80)
    ani=animation.FuncAnimation(f,animate,interval=1000)
    
else:
    ICU=Tk()
    ICU.title('ICU')
    ICU.geometry('1200x700')
    Label(ICU,text='\n ').place(x=0,y=130)
    Label(ICU,text='INTENSIVE CARE UNIT',font='Helvatica 30 bold italic underline',fg='green').place(x=420,y=5)
    Label(ICU,text='UID NOT REGISTERED',font='Helvatica 20 bold underline',fg="black").place(x=515,y=130)
    Button(ICU,text='Back',font='Arial 25 bold italic',fg="blue",bg="black",width='10',height='1',command=back).place(x=578,y=500)
    
'''else:
    mycursor.execute("CREATE DATABASE "+UID)
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database=UID)
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE Readings (DATE VARCHAR(255),TIME VARCHAR(255),PULSE VARCHAR(255), BP VARCHAR(255))")
    mycursor.execute("CREATE TABLE prescription_record (date VARCHAR(255),time VARCHAR(255),doctor VARCHAR(255),prescription VARCHAR(255))")
'''   

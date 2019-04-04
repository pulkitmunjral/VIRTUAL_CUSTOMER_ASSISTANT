from tkinter import *
import time
import mysql.connector
from tkinter import messagebox
import matplotlib.pyplot as plt
import time as t
def front1():
    global ro1
    try:
        ro1.destroy()
    except:
        pass
    try:
        ro2.destroy()
    except:
        pass
    
    ro1=Tk()
    ro1.title("Reception_desk")
    ro1.geometry('1200x700')
    ro1.configure(background='dark slate gray')
    Label(ro1,text='RESECPTION DESK',font='Likhan 40 bold ',bg='dark slate gray',fg='black').place(x=180,y=50)
    Label(ro1,text='ENTER YOUR UNID\t\t:-',font='Vemana2000 13 bold',bg='dark slate gray').place(x=80,y=300)
    Button(ro1,text='BACK',font='Arial 10 bold').place(x=880,y=600)
    e1=Entry(ro1,width='35',bd=4)
    e1.place(x=480,y=300)
    Button(ro1,text='SUBMIT',font='Arial 10 bold',command=lambda:welcome1(e1.get())).place(x=400,y=400)

def welcome1(UID):
    available_id=[]
    UID="a"+UID
    pre = mysql.connector.connect(host="localhost",user="root",passwd="")
    precursor = pre.cursor()
    precursor.execute("SHOW DATABASES")
    for x in precursor:
        available_id.append(x[0])
    if((UID in available_id)==True):
        a=messagebox.showinfo("INFO", "UID ALREADY EXIST")
        welcome()
    else:
        precursor.execute("CREATE DATABASE "+UID)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database=UID)
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE Readings (DATE VARCHAR(255),TIME VARCHAR(255),PULSE VARCHAR(255), BP VARCHAR(255))")
        mycursor.execute("CREATE TABLE prescription_record (date VARCHAR(255),time VARCHAR(255),doctor VARCHAR(255),prescription VARCHAR(255))")
        welcome()

def welcome():
    global ro2
    try:
        ro1.destroy()
    except:
        pass
    try:
        ICU.destroy()
    except:
        pass
    try:
        r1.destroy()
    except:
        pass
    try:
        ro2.destroy()
    except:
        pass
    try:
        ro5.destroy()
    except:
        pass
    
    ro2=Tk()
    ro2.title("Reception_desk")
    ro2.geometry('1200x700')
    ro2.configure(background='dark slate gray')
    Label(ro2,text='CHOOSE YOUR DOMAIN',font='Likhan 40 bold ',bg='dark slate gray',fg='black').place(x=220,y=50)
    Button(ro2,text='BACK',font='Arial 10 bold',height=2,width=10,command=lambda:ro2.destroy()).place(x=880,y=600)
    Button(ro2,text='ICU',font='Arial 25 bold',height=3,width=20,command=icu1).place(x=150,y=200)
    Button(ro2,text='DOCTOR CONTROL',font='Arial 25 bold',height=3,width=20,command=lambda:front()).place(x=650,y=200)
    Button(ro2,text='PHARMACY',font='Arial 25 bold',height=3,width=20,command=lambda:pharmacy()).place(x=150,y=410)
    Button(ro2,text='RECEPTION',font='Arial 25 bold',height=3,width=20,command=lambda:front1()).place(x=650,y=410)

def icu1():
    global ro5
    try:
        ro1.destroy()
    except:
        pass
    try:
        ro2.destroy()
    except:
        pass
    try:
        ICU.destroy()
    except:
        pass
    
    ro5=Tk()
    ro5.title("Reception_desk")
    ro5.geometry('1200x700')
    ro5.configure(background='dark slate gray')
    Label(ro5,text='WELCOME TO ICU',font='Likhan 40 bold ',bg='dark slate gray',fg='black').place(x=200,y=50)
    Label(ro5,text='ENTER YOUR UNID\t\t:-',font='Vemana2000 13 bold',bg='dark slate gray').place(x=80,y=300)
    Button(ro5,text='BACK',font='Arial 10 bold',command=welcome).place(x=880,y=600)
    e1=Entry(ro5,width='35',bd=4)
    e1.place(x=480,y=300)
    Button(ro5,text='SUBMIT',font='Arial 10 bold',command=lambda:icu(e1.get())).place(x=400,y=400)

 
def icu(UID):
    try:
        ro5.destroy()
    except:
        pass
    
    import matplotlib
    import matplotlib.animation as animation
    import time as t
    import mysql.connector
    from matplotlib import style
    from threading import Thread
    from tkinter import messagebox as msg
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    UID="a"+UID
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
        
    def back(UID):
        #link main window
        icu1()
        
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
    #global UID
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
        Button(ICU,text='Back',font='Arial 22 bold italic',fg="black",bg="green",width='10',height='1',command=lambda:back(UID)).place(x=660,y=640)
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


def front():
    global r1
    try:
        r1.destroy()
    except:
        pass
    try:
        ro2.destroy()
    except:
        pass
    try:
        r2.destroy()
    except:
        pass
    try:
        r3.destroy()
    except:
        pass
    global e1
    r1=Tk()
    r1.title('Editor')
    r1.geometry('1200x700')
    r1.configure(background='dark slate gray')
    Label(r1,text='DOCTOR\'S CONTROL',font='Likhan 40 bold ',bg='dark slate gray',fg='black').place(x=180,y=50)
    Label(r1,text='ENTER YOUR UNID\t\t:-',font='Vemana2000 13 bold',bg='dark slate gray').place(x=80,y=300)
    Button(r1,text='BACK',font='Arial 10 bold',command=lambda:welcome()).place(x=880,y=600)
    e1=Entry(r1,width='35',bd=4)
    e1.place(x=480,y=300)
    Button(r1,text='SUBMIT',font='Arial 10 bold',command=lambda:page1(e1.get())).place(x=400,y=400)
def page1(dunid):
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="doctor"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    myresult = mycursor.fetchall()
    length=len(myresult)
    #print(length)
    for i in range(length):
        mycursor1 = mydb.cursor(buffered=True)
        mycursor1.execute("SELECT * FROM " + myresult[i][0])
        myresult1=mycursor1.fetchone()
        #print(myresult1[0])
        if(myresult1[0]==dunid):
            global bb
            global aa
            aa=myresult[i][0]
            bb=myresult1
            break
        else:
            pass
        if(i==(length-1)):
            messagebox.showinfo("error", "INVALID UNID")
            front()
        else:
            pass

    if(bb[0]==dunid):
        print(aa)
        print(i)
        global r2
        global e2
        try:
            r1.destroy()
        except:
            pass
        try:
            r3.destroy()
        except:
            pass
        try:
            r2.destroy()
        except:
            pass
    
        r2=Tk()
        r2.title('Editor1')
        r2.geometry('1200x700')
        
        #can=Canvas(r2,background='dark slate gray')
        r2.configure(background='dark slate gray')
        Button(r2,text='BACK',font='Arial 10 bold',command=lambda:front()).place(x=150,y=550)
        Button(r2,text='SUPPORT',font='Arial 10 bold',command=front,width=20).place(x=150,y=500)
        Button(r2,text='PAITENT\'S TERMINAL',font='Arial 10 bold',command=lambda:patient_terminal(dunid),width=20).place(x=150,y=450)
        #can.create_line(100,0,100,100,fill='black')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM " + aa)
        myresult = mycursor.fetchall()
        i=0
        j=0
        lis=['NAME :-','OCCUPATION :-','SPECIALIZATON :-']
        for x in myresult[1]:
            Label(r2,text=lis[j],font='Vemana 13 bold',bg='dark slate gray').place(x=300,y=120+i)
            Label(r2,text=x,font='Vemana2000 12 bold ',bg='dark slate gray').place(x=500,y=120+i)
            i=i+30
            j=j+1
            if(j==3):
                break
        pic2=PhotoImage(file=myresult[2][0])
        l2=Label(r2,image=pic2)
        l2.place(x=10,y=50)
        
        
        Label(r2,text='APPOINTMENTS',font='HELVETICA 20 bold underline',bg='dark slate gray',fg='black').place(x=800,y=30)
        Label(r2,text='MEETINGS',font='HELVETICA 20 bold underline',bg='dark slate gray',fg='black').place(x=800,y=400)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT appointments , meetings FROM " + aa)
        result_appoint = mycursor.fetchall()
        print(result_appoint)
        i=1
        for j in range(3,len(result_appoint)):
            if(i>0):     
                Label(r2,text='{}.'.format(result_appoint[j][0]),font='Vemana2000 13 bold',bg='dark slate grey').place(x=800,y=(40*i)+80,anchor='sw')
                Label(r2,text='{}.'.format(result_appoint[j][1]),font='Vemana2000 13 bold',bg='dark slate grey').place(x=800,y=(40*i)+450,anchor='sw')
                i=i+1
 
        r2.mainloop()
def patient_terminal(dunid):
    try:
        r2.destroy()
    except:
        pass
    global r3
    try:
        r3.destroy()
    except:
        pass
    try:
        r4.destroy()
    except:
        pass
    global e3
    r3=Tk()
    r3.title('Editor1')
    r3.geometry('1200x700')
    r3.configure(background='dark slate gray')
    Label(r3,text='ENTER PATIENT\'S UNID',font='Vemana2000 30 bold ',bg='dark slate gray',fg='black').place(x=400,y=150)        
    e3=Entry(r3,width='35',bd=4)
    e3.place(x=480,y=300)
    Button(r3,text='SUBMIT',font='Arial 10 bold',command=lambda:patient(dunid,e3.get())).place(x=370,y=400)
    Button(r3,text='BACK',font='Arial 10 bold',command=lambda:page1(dunid)).place(x=400,y=550)

    
def patient(dunid,punid):
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd=""
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    available_id=[]
    for i in mycursor:
       available_id.append(i[0])
    
    if((punid in available_id)==True):
        global r4
        global e4
        global e5
        global e6
        try:
            r3.destroy()
        except:
            pass
        try:
            r4.destroy()
        except:
            pass
        
        
        r4=Tk()
        r4.title('Editor1')
        r4.geometry('1200x700')
        r4.configure(background='dark slate gray')
        Label(r4,text='DETAILS',font='HELVETICA 20 bold underline',bg='dark slate gray',fg='black').place(x=80,y=30)
        Label(r4,text='RECORD',font='HELVETICA 20 bold underline',bg='dark slate gray',fg='black').place(x=400,y=30)
        
        Label(r4,text='PRESCRIBE HERE',font='HELVETICA 20 bold underline',bg='dark slate gray',fg='black').place(x=800,y=30)
        Label(r4,text='Medicine',font='HELVETICA 12',bg='dark slate gray',fg='black').place(x=820,y=100)
        Label(r4,text='/Day',font='HELVETICA 12',bg='dark slate gray',fg='black').place(x=1050,y=100)
        
        Label(r4,text='Days',font='HELVETICA 12',bg='dark slate gray',fg='black').place(x=1200,y=100)
        e4=Entry(r4,width='20',bd=4)
        e4.place(x=820,y=140)
        e5=Entry(r4,width='5',bd=4)
        e5.place(x=1050,y=140)
        e6=Entry(r4,width='5',bd=4)
        e6.place(x=1200,y=140)
        report(punid)
        
        Button(r4,text='SUBMIT',font='Arial 10 bold',command=lambda:prescribe(e4.get(),e5.get(),e6.get(),punid,dunid)).place(x=1000,y=200)
        Button(r4,text='BACK',font='Arial 10 bold',command=lambda:patient_terminal(dunid)).place(x=1100,y=600)
        
    else:
        messagebox.showinfo("error", "INVALID UNID")
        patient_terminal(dunid)
def prescribe(e4,e5,e6,punid,dunid):
    entry=e4 +" *" +e5+" x"+e6+"days"
    pre = mysql.connector.connect(host="localhost",user="root",passwd="",database=punid)
    precursor = pre.cursor()
    doc = mysql.connector.connect(host="localhost",user="root",passwd="",database='doctor')
    doccursor = doc.cursor()
    doccursor.execute('SHOW TABLES')
    myresult = doccursor.fetchall()
    length=len(myresult)
    #print(length)
    for i in range(length):
        mycursor1 = doc.cursor(buffered=True)
        mycursor1.execute("SELECT * FROM " + myresult[i][0])
        myresult1=mycursor1.fetchone()
        #print(myresult1[0])
        if(myresult1[0]==dunid):
            global bb
            global aa
            aa=myresult[i][0]
            bb=myresult1
            break
        else:
            pass
    mycursor = doc.cursor()
    mycursor.execute("SELECT * FROM " + aa)
    myresult = mycursor.fetchall()
    
    now=int(t.ctime()[11:13])
    now=int(now/8)
    tt="Dr. "+myresult[1][0]
    sql = "INSERT INTO prescription_record (date ,time ,doctor , prescription) VALUES (%s,%s,%s, %s)"
    val = (t.ctime()[:10]+t.ctime()[19:],t.ctime()[11:19],tt,entry)
    precursor.execute(sql, val)
    pre.commit()
    report(punid)
def report(punid):
    j=0
    pre = mysql.connector.connect(host="localhost",user="root",passwd="",database=punid)
    precursor = pre.cursor()
    precursor.execute("SELECT * FROM prescription_record")
    preresult = precursor.fetchall()
    for i in range(len(preresult)-1,-1,-1):
        j=j+1
        if(j<10):
            tt=preresult[i][3]+" by "+preresult[i][2]+" at "+preresult[i][1]
            Label(r4,text="                                                  ",font='Helvatica 18',bg='grey',fg="black").place(x=400,y=610-(40*j),anchor='sw')
            Label(r4,text=tt,font='Helvatica 10',bg='grey',fg="black").place(x=400,y=610-(40*j),anchor='sw')
welcome()

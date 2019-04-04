from tkinter import *
import requests
import mysql.connector
from tkinter import messagebox
import webbrowser
global root
global root1
global root2
global root3
global e1
global e2
def showstock(pswrd):
    if (pswrd=='rajat'):
        #requests.get('http://localhost/phpmyadmin/sql.php?server=1&db=stock&table=medicines&pos=0')
        webbrowser.open_new_tab("http://localhost/phpmyadmin/sql.php?server=1&db=stock&table=medicines&pos=0")
    else:
        messagebox.showinfo('msg','Wrong Password.Try Again')
        owner()
def owner():
    global root
    global root3
    try:
        root.destroy()
    except:
        pass
    try:
        root3.destroy()
    except:
        pass
    root3=Tk()
    root3.title('Pharmacy')
    root3.geometry("1200x700")
    root3.configure(background="dark slate gray")
    l1=Label(root3,bg="black",fg="white",text="Enter Your Password ",font="Vemana2000 30 underline")
    l1.place(x=150,y=200)
    e2=Entry(root3,bd=2,width=20,font="Vemana2000 30",show="*")
    e2.place(x=550,y=200)
    pswrd=e2.get()
    b1=Button(root3,text="Submit",bg='Mint Cream',fg='black',width='10',height='1',font="Vemana2000 20 bold",command=lambda:showstock(e2.get()))
    b1.place(x=330,y=500)
    b2=Button(root3,text="Back",bg='Mint Cream',fg='black',width='10',height='1',font="Vemana2000 20 bold",command=front)
    b2.place(x=630,y=500)
def stock(uid1):
    
    medi=[]
    mydb1 = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database=uid1
    )

    mycursor2 = mydb1.cursor()
    sql = "SELECT prescription FROM prescription_record"

    mycursor2.execute(sql)

    myresult = mycursor2.fetchall()
    for y in myresult:
        medi.append(y[0])
    med=medi[len(medi)-1]
    medic=med.split(', ')
    mydb2 = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="stock"
    )

    mycursor3 = mydb2.cursor()
    mycursor3.execute("SELECT name FROM medicines")
    r=mycursor3.fetchall()
    
    for x in range(0,len(medic)):
        sql1="SELECT quantity FROM medicines WHERE name = %s"
        val1=(medic[x], )
        mycursor3.execute(sql1, val1)
        ff = mycursor3.fetchall()
        d=int(ff[0][0])
        e=d-1
        if (e<125):
            med="only "+str(e)+" "+str(medic[x])+" left"+"  PLACE ODER?"
            a=messagebox.askyesno('msg',med)
            if(a==True):
                print("yes")
        else:
            sql2 = "UPDATE medicines SET quantity = %s WHERE name = %s"
            val2 = (e, medic[x])
            mycursor3.execute(sql2, val2)
            mydb2.commit()
    patient()
    

def medicine(uid):
    global root
    global root1
    global root2
    a=[]
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd=""
    )

    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        a.append(x[0])
    if uid in a:
        try:
            root1.destroy()
        except:
            pass
        root2=Tk()
        root2.title('Pharmacy')
        root2.geometry("1200x700")
        root2.configure(background="dark slate gray")
        mydb1 = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="",
          database=uid
        )
        
        mycursor1 = mydb1.cursor()
        mycursor1.execute("SELECT * FROM prescription_record")

        preresult = mycursor1.fetchall()
        j=0
        for i in range(len(preresult)-1,-1,-1):
            j=j+1
            if(j<6):
                tt=preresult[i][3]+" by "+preresult[i][2]+" at "+preresult[i][1]
                Label(root2,text="                                                  ",font='Helvatica 18',bg='grey',fg="black").place(x=600,y=610-(40*j),anchor='se')
                Label(root2,text=tt,font='Helvatica 18',bg='grey',fg="black").place(x=600,y=610-(40*j),anchor='se')
        b2=Button(root2,text="Back",bg='Mint Cream',fg='black',width='10',height='1',font="Vemana2000 20 bold",command=patient)
        b2.place(x=600,y=620)
        b3=Button(root2,text="Proceed",bg='Mint Cream',fg='black',width='10',height='1',font="Vemana2000 20 bold",command=lambda:stock(uid))
        b3.place(x=400,y=620)
    else:
        messagebox.showinfo('msg','ID not registered')
        patient()
def front():
    global root
    global root1
    global root2
    try:
        root1.destroy()
    except:
        pass
    try:
        root3.destroy()
    except:
        pass
    root=Tk()
    root.title('Pharmacy')
    root.geometry("1200x700")
    root.configure(background="dark slate gray")
    l1=Label(root,bg="black",fg="white",text="Nanak Medical Store",font="Vemana2000 70 underline")
    l1.place(x=150,y=10)

    b1=Button(root,text="Patient's zone",bg='Mint Cream',fg='black',width='20',height='4',font="Vemana2000 20 bold",command=patient)
    b1.place(x=460,y=230)

    #b2=Button(root,text="General Medicines",bg='Mint Cream',fg='black',width='20',height='2',font="Vemana2000 20",command=general)
    #b2.place(x=460,y=500)
    b3=Button(root,text="Owner Login",bg='Mint Cream',fg='black',width='20',height='4',font="Vemana2000 20 bold",command=owner)
    b3.place(x=460,y=500)

def patient():
    global root
    global root1
    global root2
    global root3
    try:
        root.destroy()
    except:
        pass
    try:
        root1.destroy()
    except:
        pass
    try:
        root2.destroy()
    except:
        pass
    root1=Tk()
    root1.title('Pharmacy')
    root1.geometry("1200x700")
    root1.configure(background="dark slate gray")
    l1=Label(root1,bg="black",fg="white",text="Enter Your UniqueID ",font="Vemana2000 30 underline")
    l1.place(x=150,y=200)
    e1=Entry(root1,bd=2,width=20,font="Vemana2000 30")
    e1.place(x=550,y=200)
    b1=Button(root1,text="Submit",bg='Mint Cream',fg='black',width='10',height='1',font="Vemana2000 20 bold",command=lambda:medicine(e1.get()))
    b1.place(x=330,y=500)
    b2=Button(root1,text="Back",bg='Mint Cream',fg='black',width='10',height='1',font="Vemana2000 20 bold",command=front)
    b2.place(x=630,y=500)
    uid=e1.get()
    
front()

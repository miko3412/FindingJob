from tkinter import *
from tkinter import ttk
import scrap
import webbrowser
import threading

#Changing page
def changepage(i,root,e=[]):
    for widget in root.winfo_children():
        widget.destroy()
    if i == 1:
        page1(root)
    if i==2:
        page2(root)
    if i==3:
        page3(root,e)
    
#First page making
def page1(root):

    #Command called on button press
    def buttonCommand(selection,job,seniority,city,km):
        x=scrap.Soup('https://www.pracuj.pl')
        l=x.get_jobs_pracuj(job,city,seniority,0)
        changepage(3,root,l)
        
    global l
    l=[]
    top=root
    main_label = Label(top,text="Welcome to data scraping app which helps you to find the perfect job for you",pady=10)
    main_label.pack()

    second_label = Label(top,text="Choose site:",pady=5)
    second_label.pack()

    listing=["All","Pracuj.pl"]
    variable = StringVar(top)
    variable.set(listing[1])
    combobox = OptionMenu(top,variable,*listing)
    combobox.pack()

    job_label=Label(top,text="Write a position or programing language:",pady=5)
    job_label.pack()

    job_entry=Entry(top)
    job_entry.pack()

    city_label=Label(top,text="Write a city:",pady=5)
    city_label.pack()

    city_entry=Entry(top)
    city_entry.pack()

    seniority_label=Label(top,text="Write seniority:",pady=5)
    seniority_label.pack()

    seniority_entry=Entry(top)
    seniority_entry.pack()

    km_label=Label(top,text="Write a max distance from city you chose:",pady=5)
    km_label.pack()

    km_entry = Entry(top)
    km_entry.pack(pady=5)

    submit = Button(top,text="Szukaj",padx=3,pady=2,command=lambda:[threading.Thread(target=buttonCommand,args=(variable.get(),job_entry.get(),seniority_entry.get(),city_entry.get(),km_entry.get())).start(),changepage(2,root)])
    submit.pack()

#This function is making a loading page
def page2(root):
    top=root
    main_label = Label(top,text="Please wait. We are loading the page",pady=10)
    main_label.pack()
    my_progress = ttk.Progressbar (root, orient=HORIZONTAL, length=300 ,mode='determinate')
    my_progress.pack(pady=15)
    my_progress.start(10)
#This function is loading last page with results
def page3(root,results):
    top=root
    def back():
        changepage(1,root)
    my_button = Button(top,text="Back",command=back)
    my_button.pack(pady=10)
    my_listbox=Listbox(top)
    my_listbox.pack(pady=15,padx=15)
    my_listbox.config(width=80, height=20)
    def select():
        a=my_listbox.curselection()
        url=results[a[0]][4]
        my_label.config(text=my_listbox.get(ANCHOR))
        link1.config(text=url)
        link1.bind("<Button-1>",lambda e,url=url:open_url(url))
    def open_url(url):
        webbrowser.open(url)
    f=0
    for item in results:
        my_listbox.insert(END, item[0]+' in company: '+item[1])

    for i in range(my_listbox.size()):
        if i%2 == 0:
            my_listbox.itemconfig(i, {'bg':'light green'})
    
    my_button2 = Button(top,text="Choose",command=select)
    my_button2.pack(pady=10)
    my_label = Label(top, text='')
    my_label.pack(pady=5)
    link1 = Label(top, text="", fg="blue", cursor="hand2")
    link1.pack()

top = Tk()
top.geometry("800x600")
top.title("Welcome to my app")
page1(top)
top.mainloop()
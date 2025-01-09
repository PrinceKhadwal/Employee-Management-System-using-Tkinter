from tkinter import *
from tkinter.ttk import *
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox
from  datetime import date
from dateutil import parser


# query = '''
# create table employee(
# 	Department varchar(40),
# 	Designation varchar(30),
#     Address varchar(50),
#     DOB date,
#     Adhaar bigint unique,
#     Ename varchar(40),
#     Email varchar(40) unique,
#     Marital_Status varchar(30),
#     DOJ date,
#     Gender varchar(12),
#     Phone_no bigint unique,
#     Country varchar(30),
#     Salary float
# );'''

def insert_data():
  dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="Prince@20"
  )
  cursorObject = dataBase.cursor()

  try:
    val = ( dept_var.get(), design_var.get(), address_var.get(), dob_Entry.get_date(), adhar_var.get(), name_var.get(), email_var.get(),
    marital_var.get(), doj_Entry.get_date(), gender_var.get(), phone_var.get(), country_var.get(), salary_var.get(),)

    count = 1

    for item in val:
      if not item:
        messagebox.showerror("showerror", "All fields are required")
        count = 0
        break

    if count:
      query = '''use employee;'''
      cursorObject.execute(query)

      query = '''Insert into employee
      (Department, Designation, Address, DOB, Adhaar, Ename, Email, Marital_Status, DOJ, Gender, Phone_no, Country, Salary)
      values
      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
      
      cursorObject.execute(query, val)
      dataBase.commit()
      show_data()
      dataBase.close()
      messagebox.showinfo("showinfo", "Employee added Successfully")

      reset_fields()

  except TclError:
    messagebox.showerror("showerror", "kindly enter integer data respectively")

  except:
    messagebox.showerror("showerror", "Duplicate Employee")
    


def truncate_tree_view():
  for item in treev.get_children():
   treev.delete(item)



def show_data():
  truncate_tree_view()
  
  dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="Prince@20"
  )
  cursorObject = dataBase.cursor()

  query = '''use employee;'''
  cursorObject.execute(query)

  query = '''Select * from employee;'''
  cursorObject.execute(query)
  data = cursorObject.fetchall()

  if data:
    for item in data:
      treev.insert("", END, text="", values = item)

  dataBase.commit()
  dataBase.close()


def get_cursor(event=""):
  curser_row = treev.focus()
  content = treev.item(curser_row)
  data = content['values']

  dept_var.set(data[0])
  design_var.set(data[1])
  address_var.set(data[2])

  DT = parser.parse(data[3])
  dob_Entry.set_date(DT)

  adhar_var.set(data[4])
  name_var.set(data[5])
  email_var.set(data[6])
  marital_var.set(data[7])
  
  DT2 = parser.parse(data[8])
  doj_Entry.set_date(DT2)
  
  gender_var.set(data[9])
  phone_var.set(data[10])
  country_var.set(data[11])
  salary_var.set(data[12])


def update_data():
  dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="Prince@20"
  )
  cursorObject = dataBase.cursor()

  try:
    val = ( dept_var.get(), design_var.get(), address_var.get(), dob_Entry.get_date(), adhar_var.get(), name_var.get(), email_var.get(),
    marital_var.get(), doj_Entry.get_date(), gender_var.get(), phone_var.get(), country_var.get(), salary_var.get())

    count = 1

    for item in val:
      if not item:
        messagebox.showerror("showerror", "All fields are required")
        count = 0
        break

    if count:
      query = '''use employee;'''
      cursorObject.execute(query)

      adhar_value = adhar_var.get()

      query = f'''
      Update employee SET  
      Department = '{dept_var.get()}', 
      Designation= '{design_var.get()}', 
      Address = '{address_var.get()}', 
      DOB = '{dob_Entry.get_date()}', 
      Adhaar ='{adhar_var.get()}', 
      Ename = '{name_var.get()}', 
      Email = '{email_var.get()}', 
      Marital_Status = '{marital_var.get()}', 
      DOJ = '{doj_Entry.get_date()}', 
      Gender = '{gender_var.get()}', 
      Phone_no = '{phone_var.get()}', 
      Country = '{country_var.get()}', 
      Salary = '{salary_var.get()}'
      where adhaar = '{adhar_value}' 
      '''
      
      cursorObject.execute(query)
      dataBase.commit()
      show_data()
      dataBase.close()
      messagebox.showinfo("showinfo", "Employee updated Successfully")

      reset_fields()

  except TclError:
    messagebox.showerror("showerror", "kindly enter integer data respectively")

  except:
    messagebox.showerror("showerror", "Duplicate Employee")



def delete_data():
  dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="Prince@20"
  )
  cursorObject = dataBase.cursor()

  query = '''use employee;'''
  cursorObject.execute(query)
  
  try:
    adhar = str(adhar_var.get())
    query = f'''Delete from employee where Adhaar = {adhar}'''
    cursorObject.execute(query)
    dataBase.commit()
    reset_fields()
    show_data()
  
  except:
    messagebox.showerror("showerror", "Employee not deleted")

  dataBase.close()


def reset_fields():
  variables = ( dept_var, design_var, address_var, adhar_var, name_var, email_var, marital_var, gender_var, phone_var, country_var, salary_var)

  for variable in variables:
    variable.set("")

  dob_Entry.set_date(date.today())
  doj_Entry.set_date(date.today())



def search_data():
  get_type = search_options.get()
  search_value = search_var.get()

  if search_value != "":
       
    dataBase = mysql.connector.connect(
    host ="localhost",
    user ="root",
    passwd ="Prince@20"
    )
    cursorObject = dataBase.cursor()

    query = '''use employee;'''
    cursorObject.execute(query)

    
    if get_type =="By Department":
      query = f'''Select * from employee where department = '{search_value}';'''
    elif get_type == "By Phone No":
      query = f'''Select * from employee where phone_no = '{search_value}';'''
    elif get_type == "By Marital Status":
      query = f'''Select * from employee where Marital_Status = '{search_value}';'''
    elif get_type == "By Adhaar ID":
      query = f'''Select * from employee where Adhaar = '{search_value}';'''
    elif get_type == "By Name":
      query = f'''Select * from employee where ename like '{search_value}%';'''
    elif get_type == "By Gender":
      query = f'''Select * from employee where gender = '{search_value}';'''

    cursorObject.execute(query)
    data = cursorObject.fetchall()


    if data:
      truncate_tree_view()
      for item in data:
        treev.insert("", END, text="", values = item)
    else:
      messagebox.showerror("showerror", "Data not found for input value")

    dataBase.commit()
    dataBase.close()

  else:
    show_data()



def sort_data():
  
  get_type = sort_options.get()
       
  dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="Prince@20"
  )
  cursorObject = dataBase.cursor()

  query = '''use employee;'''
  cursorObject.execute(query)
  
  if get_type =="By Department":
    query = f'''Select * from employee order by department;'''
  elif get_type == "By Marital Status":
    query = f'''Select * from employee order by Marital_Status;'''
  elif get_type == "By Adhaar ID":
    query = f'''Select * from employee order by Adhaar;'''
  elif get_type == "By Name":
    query = f'''Select * from employee order by ename;'''
  elif get_type == "By Gender":
    query = f'''Select * from employee order by gender;'''
  elif get_type == "By Salary":
    query = f'''Select * from employee order by salary desc;'''

  cursorObject.execute(query)
  data = cursorObject.fetchall()


  if data:
    truncate_tree_view()
    for item in data:
      treev.insert("", END, text="", values = item)
  else:
    messagebox.showerror("showerror", "Data not found")

  dataBase.commit()
  dataBase.close()


win = Tk()
win.title("Employee Management System")
win.minsize(1280, 720)


dept_var = StringVar()
design_var = StringVar()
address_var = StringVar()
adhar_var = IntVar()
name_var = StringVar()
email_var = StringVar()
marital_var = StringVar()
gender_var = StringVar()
phone_var = IntVar()
country_var = StringVar()
salary_var = DoubleVar()

search_var = StringVar()


#__________________________________________________Heading of the application_________________________________________
heading = Label(win, text="Employee Management System", font=("Times New Roman", 30, "bold") , foreground="red")
heading.pack(padx=10, pady=5)


#_______________________________Outer Frame_________________________________


outer_frame = Frame(win)
outer_frame.pack(expand='no', fill='both', padx=25, pady=25)

#--------------------------------------------------Employee information Section----------------------------------------

information_Frame = LabelFrame(outer_frame, text="Employee Information", relief=RIDGE)
information_Frame.pack(expand="no", fill='both', padx=5, pady=5, ipady=5)


#********************widgets

##################       Row 1


department_label = Label(information_Frame, text="Department : ",)
designation_label = Label(information_Frame, text="Designation : ",)
address_label = Label(information_Frame, text="Address : ", )

department_label.grid(row=0, column=0, sticky=W, padx=4, pady=8)
designation_label.grid(row=1, column=0, sticky=W, padx=4, pady=8)
address_label.grid(row=2, column=0, sticky=W, padx=4, pady=8)

department_Entry = Combobox(information_Frame, textvariable=dept_var, values=["Software Engineer", "HR", "Infrastructure", "Manager"])
department_Entry.set("Select Department")
designation_Entry = Entry(information_Frame, textvariable=design_var,)
address_Entry = Entry(information_Frame, textvariable=address_var,)

department_Entry.grid(row=0, column=1, sticky=EW)
designation_Entry.grid(row=1, column=1, sticky=EW)
address_Entry.grid(row=2, column=1, sticky=EW)




##################       Row 2

name_label = Label(information_Frame, text="Name : ", justify=LEFT)
email_label = Label(information_Frame, text="Email : ", justify=LEFT)
marital_label = Label(information_Frame, text="Marital Status : ", justify=LEFT)

name_label.grid(row=0, column=2, sticky=W, padx=4, pady=8)
email_label.grid(row=1, column=2, sticky=W, padx=4, pady=8)
marital_label.grid(row=2, column=2, sticky=W, padx=4, pady=8)

name_Entry = Entry(information_Frame, textvariable=name_var,)
email_Entry = Entry(information_Frame, textvariable=email_var,)
marital_Entry = Combobox(information_Frame, textvariable=marital_var, values=["Married", "Unmarried", "Widow", "Divorced"])
marital_Entry.set("Select Marital Status")

name_Entry.grid(row=0, column=3, sticky=EW)
email_Entry.grid(row=1, column=3, sticky=EW)
marital_Entry.grid(row=2, column=3, sticky=EW)



##################       Row 3


dob_label = Label(information_Frame, text="DOB : ", )
adhaar_label = Label(information_Frame, text="Adhaar Card : ", anchor=CENTER)
salary_label = Label(information_Frame, text="Salary (CTC) : ", justify=LEFT)

dob_Entry = DateEntry(information_Frame, width=12, background="darkblue", foreground="white", borderwidth=2)
adhaar_Entry = Entry(information_Frame, textvariable=adhar_var,)
salary_Entry = Entry(information_Frame, textvariable=salary_var,)


dob_label.grid(row=0, column=4, sticky=W, padx=4, pady=8)
adhaar_label.grid(row=1, column=4, sticky=W, padx=4, pady=8)
salary_label.grid(row=2, column=4, sticky=W, padx=4, pady=8)


dob_Entry.grid(row=0, column=5, sticky=EW)
adhaar_Entry.grid(row=1, column=5, sticky=EW)
salary_Entry.grid(row=2, column=5, sticky=EW)



##################       Row 4

phone_label = Label(information_Frame, text="Phone No : ", justify=LEFT)
country_label = Label(information_Frame, text="Country : ", justify=LEFT)

phone_label.grid(row=0, column=6, sticky=W, padx=4, pady=8)
country_label.grid(row=1, column=6, sticky=W, padx=4, pady=8)

phone_Entry = Entry(information_Frame, textvariable=phone_var,)
country_Entry = Entry(information_Frame, textvariable=country_var,)

phone_Entry.grid(row=0, column=7, sticky=EW)
country_Entry.grid(row=1, column=7, sticky=EW)



##################       Row 5

doj_label = Label(information_Frame, text="DOJ : ", justify=LEFT)
gender_label = Label(information_Frame, text="Gender : ", anchor=CENTER)

doj_label.grid(row=0, column=8, sticky=W, padx=4, pady=8)
gender_label.grid(row=1, column=8, sticky=W, padx=4, pady=8)


doj_Entry = DateEntry(information_Frame, width=12, background="darkblue", foreground="white", borderwidth=2)
gender_Entry = Combobox(information_Frame, textvariable=gender_var, values=["Male", "Female", "Transgender"])
gender_Entry.set("Select Gender")


doj_Entry.grid(row=0, column=9, sticky=EW)
gender_Entry.grid(row=1, column=9, sticky=EW)



##################       button column       ###############

save_btn = Button(information_Frame, text="Save", command=insert_data)
update_btn = Button(information_Frame, text="Update", command=update_data)
delete_btn = Button(information_Frame, text="Delete", command=delete_data)
reset_btn = Button(information_Frame, text="Reset", command=reset_fields)

save_btn.grid(row=3, column=0, sticky=W, padx=4, pady=8)
update_btn.grid(row=3, column=1, sticky=W, padx=4, pady=8)
delete_btn.grid(row=3, column=2, sticky=W, padx=4, pady=8)
reset_btn.grid(row=3, column=3, sticky=W, padx=4, pady=8)


#--------------------------------------------------Search Employees Information----------------------------------------


search_outer_frame = Frame(win, relief=RIDGE)
search_outer_frame.pack(expand='yes', fill='both', padx=25, pady=10)

search_Frame = LabelFrame(search_outer_frame, text="Search Employees", relief=RIDGE)
search_Frame.pack(expand='no', fill='both', padx=5, pady=5)


#***************************widgets**************************

#####################       searching data       ########################




search_label = Label(search_Frame, text="Search By : ")
search_options = Combobox(search_Frame, values=["By Department", "By Phone No", "By Marital Status", "By Adhaar ID", "By Name", "By Gender"])
search_options.set("Select options")
search_input = Entry(search_Frame, textvariable=search_var)
search_btn = Button(search_Frame, text="Search", command=search_data)
show_all_btn = Button(search_Frame, text="Show All", command=show_data)

search_label.grid(row=0, column=0, sticky=W, padx=4, pady=8)
search_options.grid(row=0, column=1, sticky=W, padx=4, pady=8)
search_input.grid(row=0, column=2, sticky=W, padx=4, pady=8)
search_btn.grid(row=0, column=3, sticky=W, padx=4, pady=8)
show_all_btn.grid(row=0, column=4, sticky=W, padx=4, pady=8)



#####################       Sorting data       ########################



sort_label = Label(search_Frame, text="Sort By : ")
sort_options = Combobox(search_Frame, values=["By Department", "By Marital Status", "By Adhaar ID", "By Name", "By Gender", "By Salary"])
sort_options.set("Select options")
sort_btn = Button(search_Frame, text="Sort", command=sort_data)

sort_label.grid(row=0, column=5, sticky=W, padx=4, pady=8)
sort_options.grid(row=0, column=6, sticky=W, padx=4, pady=8)
sort_btn.grid(row=0, column=8, sticky=W, padx=4, pady=8)




# _______________________________create table for showing data______________________________


table_frame = Frame(search_outer_frame, relief=RIDGE)
table_frame.pack(expand='yes', fill='both', padx=5, pady=5)


# ********************************actual table of employees*********************

#'''''''''''''''''''''''''''''Scroll bars'''''''''''''''''''''''''''''''''

v_scroll_bar = Scrollbar(table_frame, orient=VERTICAL, )
v_scroll_bar.pack(side = RIGHT, fill = Y)

h_scroll_bar = Scrollbar(table_frame, orient=HORIZONTAL, )   
h_scroll_bar.pack( side = BOTTOM, fill = X )  

treev = Treeview(table_frame, selectmode ='browse', xscrollcommand = h_scroll_bar.set, yscrollcommand = v_scroll_bar.set)
treev.pack(side ='left', expand=YES, fill=BOTH)

v_scroll_bar.config(command = treev.yview)
h_scroll_bar.config(command = treev.xview)
 
treev["columns"] = ("dep", 'des', 'address', 'dob', 'adhar', "name", 'email', 'married', 'doj', 'gender', 'phone', 'country', 'salary')
 
treev['show'] = 'headings'

treev.heading("dep", text ="Department")
treev.heading("des", text ="Designation")
treev.heading("address", text ="Address")
treev.heading("dob", text ="DOB")
treev.heading("adhar", text ="Adhaar card")
treev.heading("name", text ="Name")
treev.heading("email", text ="Email")
treev.heading("married", text ="Marital Status")
treev.heading("doj", text ="DOJ")
treev.heading("gender", text ="Gender")
treev.heading("phone", text ="Phone No")
treev.heading("country", text ="Country")
treev.heading("salary", text ="Salary")
 
treev.column("dep", width = 90, anchor=CENTER)
treev.column("des", width = 90, anchor=CENTER)
treev.column("address", width = 90, anchor=CENTER)
treev.column("dob", width = 90, anchor=CENTER)
treev.column("adhar", width = 90, anchor=CENTER)
treev.column("name", width = 90, anchor=CENTER)
treev.column("email", width = 90, anchor=CENTER)
treev.column("married", width = 70, anchor=CENTER)
treev.column("doj", width = 90, anchor=CENTER)
treev.column("gender", width = 70, anchor=CENTER)
treev.column("phone", width = 70, anchor=CENTER)
treev.column("country", width = 90, anchor=CENTER)
treev.column("salary", width = 90, anchor=CENTER)
 
treev.bind("<ButtonRelease>", get_cursor)

reset_fields()
show_data()

win.mainloop()
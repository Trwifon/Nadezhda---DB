import mysql.connector
import mysql.connector.locales.eng
from mysql.connector.plugins import caching_sha2_password
from mysql.connector.plugins import mysql_native_password
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import csv
import os

dict_connection = {
    # 'host': '127.0.0.1',
    'host': '192.168.5.175',
    'port': '3306',
    # 'user': 'root',
    'user': 'Tsonka',
    # 'password': 'Proba123+',
    'password': 'Tsonka123+',
    'database': 'nadejda-94'
}
connection = mysql.connector.connect(**dict_connection)
cursor = connection.cursor()

def select(treeview):
    selected_item = treeview.focus()
    details = treeview.item(selected_item)
    order = details.get('values')[1]
    return order

def move_pvc():
    if messagebox.askyesno('Преместване на данни?', 'Поръчката ще бъде преместена и данните ще бъдат изтрити!'):
        order_to_move = (select(pvc_treeview),)
        get_order = "SELECT firm, order_id, length, width, count, type FROM pvc_glass_orders WHERE order_id = %s " \
                    "AND done = 0"
        cursor.execute(get_order, order_to_move)
        rows = cursor.fetchall()
        for row in rows:
            result_treeview.insert('', 'end', values=row)
        data_update = "UPDATE pvc_glass_orders SET done = 1 WHERE order_id = %s AND done = 0"
        order_id = (select(pvc_treeview),)
        cursor.execute(data_update, order_id)
        connection.commit()
        pvc_treeview.delete(*pvc_treeview.get_children())
        cursor.execute("SELECT firm, order_id, length, width, count, type FROM pvc_glass_orders WHERE done = 0")
        rows = cursor.fetchall()
        for row in rows:
            pvc_treeview.insert('', 'end', values=row)
    return

def move_glass():
    if messagebox.askyesno('Преместване на данни?', 'Поръчката ще бъде преместена и данните ще бъдат изтрити!'):
        order_to_move = (select(glass_treeview),)
        get_order = "SELECT firm, order_id, length, width, count, type FROM glass_glass_orders WHERE order_id = %s " \
                    "AND done = 0"
        cursor.execute(get_order, order_to_move)
        rows = cursor.fetchall()
        for row in rows:
            result_treeview.insert('', 'end', values=row)
        data_update = "UPDATE pvc_glass_orders SET done = 1 WHERE order_id = %s AND done = 0"
        order_id = (select(glass_treeview),)
        cursor.execute(data_update, order_id)
        connection.commit()
        glass_treeview.delete(*glass_treeview.get_children())
        cursor.execute("SELECT firm, order_id, length, width, count, type FROM glass_glass_orders WHERE done = 0")
        rows = cursor.fetchall()
        for row in rows:
            glass_treeview.insert('', 'end', values=row)
    return

def export_result():
    file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save CSV', filetypes=(('CSV File', '*.csv'), ('all Files', '*.*')))
    with open(file_name, mode='w', newline='') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')
        for i in result_treeview.get_children():
            row = result_treeview.item(i)['values']
            row.insert(4, 'R')
            row.insert(6, row[5])
            exp_writer.writerow(row)
    messagebox.showinfo('Край', 'Файлът за разкрой е създаден!')
    cursor.close()
    connection.close()
    glass_cutting_order.destroy()
    return

glass_cutting_order = tk.Tk()

wrapper1 = tk.LabelFrame(glass_cutting_order, text = 'Поръчки PVC')
wrapper2 = tk.LabelFrame(glass_cutting_order, text = 'Поръчки Стъкла')
wrapper3 = tk.LabelFrame(glass_cutting_order, text = 'Поръчки за цех')

wrapper1.pack(side=tk.LEFT, fill='both', expand="yes", padx=1, pady=1)
wrapper2.pack(side=tk.LEFT, fill='both', expand="yes", padx=1, pady=1)
wrapper3.pack(side=tk.LEFT, fill='both', expand="yes", padx=1, pady=1)

glass_cutting_order.title = 'Файл за производство'
glass_cutting_order.geometry('1500x740')

cursor.execute("SELECT firm, order_id, length, width, count, type FROM pvc_glass_orders WHERE done = 0")
rows_pvc = cursor.fetchall()
cursor.execute("SELECT firm, order_id, length, width, count, type FROM glass_glass_orders WHERE done = 0")
rows_glass = cursor.fetchall()

pvc_treeview = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6), show='headings', height=30)
pvc_treeview.pack(side=tk.LEFT, padx=1, pady=1)
yscrollbar_pvc = ttk.Scrollbar(wrapper1, orient=tk.VERTICAL)
yscrollbar_pvc.configure(command=pvc_treeview.yview)
pvc_treeview.configure(yscrollcommand=yscrollbar_pvc.set)
yscrollbar_pvc.pack(side=LEFT,fill='y')
pvc_treeview.heading(1, text='Фирма')
pvc_treeview.heading(2, text='Поръчка')
pvc_treeview.heading(3, text='Дължина')
pvc_treeview.heading(4, text='Ширина')
pvc_treeview.heading(5, text='Брой')
pvc_treeview.heading(6, text='Вид')
pvc_treeview.column(1, width=130)
pvc_treeview.column(2, width=60)
pvc_treeview.column(3, width=60)
pvc_treeview.column(4, width=60)
pvc_treeview.column(5, width=50)
pvc_treeview.column(6, width=110)

glass_treeview = ttk.Treeview(wrapper2, columns=(1,2,3,4,5,6), show='headings', height=30)
glass_treeview.pack(side=tk.LEFT, padx=1, pady=1)
yscrollbar_glass = ttk.Scrollbar(wrapper2, orient=tk.VERTICAL)
yscrollbar_glass.configure(command=glass_treeview.yview)
glass_treeview.configure(yscrollcommand=yscrollbar_glass.set)
yscrollbar_glass.pack(side=LEFT,fill='y')
glass_treeview.heading(1, text='Фирма')
glass_treeview.heading(2, text='Поръчка')
glass_treeview.heading(3, text='Дължина')
glass_treeview.heading(4, text='Ширина')
glass_treeview.heading(5, text='Брой')
glass_treeview.heading(6, text='Вид')
glass_treeview.column(1, width=130)
glass_treeview.column(2, width=60)
glass_treeview.column(3, width=60)
glass_treeview.column(4, width=60)
glass_treeview.column(5, width=50)
glass_treeview.column(6, width=110)

for row in rows_pvc:
    pvc_treeview.insert('', 'end', values=row)

for row in rows_glass:
    glass_treeview.insert('', 'end', values=row)

result_treeview = ttk.Treeview(wrapper3, columns=(1,2,3,4,5,6), show='headings', height=30)
result_treeview.pack(side=tk.LEFT, padx=1, pady=1)
yscrollbar_result = ttk.Scrollbar(wrapper3, orient=tk.VERTICAL)
yscrollbar_result.configure(command=result_treeview.yview)
result_treeview.configure(yscrollcommand=yscrollbar_result.set)
yscrollbar_result.pack(side=LEFT,fill='y')
result_treeview.heading(1, text='Фирма')
result_treeview.heading(2, text='Поръчка')
result_treeview.heading(3, text='Дължина')
result_treeview.heading(4, text='Ширина')
result_treeview.heading(5, text='Брой')
result_treeview.heading(6, text='Вид')
result_treeview.column(1, width=130)
result_treeview.column(2, width=60)
result_treeview.column(3, width=60)
result_treeview.column(4, width=60)
result_treeview.column(5, width=50)
result_treeview.column(6, width=110)

move_pvc_button = tk.Button(wrapper1, text='Прехвърли', height=2, command=move_pvc)
move_pvc_button.pack(side=tk.BOTTOM, padx=1, pady=1)
move_pvc_button.place(x=400)
move_glass_button = tk.Button(wrapper2, text='Прехвърли', height=2, command=move_glass)
move_glass_button.pack(side=tk.BOTTOM, padx=1, pady=1)
move_glass_button.place(x=400)
export_button = tk.Button(wrapper3, text='Експорт', height=2, command=export_result)
export_button.pack(side=tk.BOTTOM, padx=1, pady=1)
export_button.place(x=415)

glass_cutting_order.mainloop()


#from 0 to 1
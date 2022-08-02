import fitz

from tkinter.filedialog import *
from tkinter import filedialog
from tkinter import ttk

class fromeDemo:

    def __init__(self):#主窗口设置参数

        def Select_Path():
            file_path = filedialog.askopenfilename()
            print(file_path)
            path_Select.set(file_path)
        def Save_Path():
            file_path = filedialog.askdirectory()
            print(file_path)
            path_Save.set(file_path)

        window = Tk()
        window_Width = window.winfo_screenwidth()
        window_Height = window.winfo_screenheight()
        window.title("PDF2Image")
        ww = 400
        wh = 180
        x = (window_Width-ww)/2
        y = (window_Height-wh)/2
        window.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

        path_Save = StringVar()
        path_Select = StringVar()

        def cmb_select(*args):
            selected_char = (cmb.get())
            var_selectedchar.set(selected_char)
        var_selectedchar = StringVar()

        def R_un():
            cmb_select()
            rotate = int(0)
            if (var_selectedchar.get()=='Full'):
                zoom_x = 2.0
                zoom_y = 2.0
            elif(var_selectedchar.get()=='Half'):
                zoom_x = 1.0
                zoom_y = 1.0

            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)

            open_file_path = path_Select
            save_file_path = path_Save

            if (open_file_path.get()!=''):
                pdf = fitz.open(open_file_path.get())
                for i in range(pdf.pageCount):
                    pm = pdf[i].getPixmap(matrix=trans, alpha=False)
                    pm.writePNG(save_file_path.get() + '/%s.png' % i)
                print('Complete')
            elif(open_file_path.get()==''):
                print('please select avilable path')

        text_label_select = Label(window, width=20, text='Selected File')
        text_label_select.place(relx=-0.08, rely=0.18, anchor='w')
        textBox_select = Entry(window, width=30, textvariable=path_Select)
        textBox_select.place(relx=0.48, rely=0.18, anchor='center')

        text_label_select = Label(window, width=20, text='Save Path')
        text_label_select.place(relx=-0.08, rely=0.4, anchor='w')
        textBox_save = Entry(window, width=30, textvariable=path_Save)
        textBox_save.place(relx=0.48, rely=0.4, anchor='center')

        bt1=Button(window, width=10, height=1, text='Select File', command=Select_Path)
        bt1.place(relx=0.87, rely=0.18, anchor='center')
        bt2=Button(window, width=10, height=1, text='Save Path', command=Save_Path)
        bt2.place(relx=0.87, rely=0.4, anchor='center')
        bt2=Button(window, width=10, height=1, text='RUN', command=R_un)
        bt2.place(relx=0.87, rely=0.65, anchor='center')

        cmb = ttk.Combobox(window, width=6)
        cmb['value'] = ('Full', 'Half')
        cmb['state'] = 'readonly'
        cmb.place(relx=0.665, rely=0.65, anchor='center')
        cmb.current(0)

        text_label_select = Label(window, width=20, text='Version 0.1 \n    Powered by yuuKi')
        text_label_select.place(relx=-0.06, rely=0.65, anchor='w')

        window.resizable(0, 0)
        window.mainloop()

fromeDemo()
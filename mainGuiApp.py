# from tkinter import *
from tkinter import END
from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Message
from tkinter import messagebox
from tkinter import font
from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Scrollbar
from tkinter import VERTICAL
from tkinter import Listbox
from tkinter import Button
from tkinter import Text
import dataPreparation.docLoader as dl
import dataPreparation.processor as pr
import lsi.preparation as prep
import lsi.conceptMatrix as cm
import lsi.querying as qr
import time


# Show document and find similar
def list_action(text, listbox, documents, texts, terms, values, U, conceptMatrix, titles, S):
    text.delete(1.0, END)
    title = listbox.get(listbox.curselection()[0])
    text.tag_configure("bold", font="Helvetica 12 bold")
    text.insert(END, title, "bold")
    text.insert(END, "\n")
    text.insert(END, "\n")
    text.insert(END, documents[title])
    queryMatrix = pr.query_to_document(texts[title], terms)
    queryMatrix = prep.add_weight_to_query(values, queryMatrix, False)
    queryConcept = cm.query_to_concept(queryMatrix, S, U, False)
    simDocs = qr.get_similar_docs(conceptMatrix, queryConcept, True, False)
    listbox.delete(0, END)
    for k, v in simDocs.items():
        if titles[v[0]] != title:
            listbox.insert(END, titles[v[0]])


# Recalculate LSI data
def recalculate(documents, U, S, conceptMatrix, values, terms, titles, texts):
    MsgBox = messagebox.askquestion("Recalculation confirmation", "Are you sure, you want to recalculate LSI model? This proces may take up to several minutes.")
    if MsgBox == 'yes':
        popup = Toplevel()
        popup.title("Computation progress")
        popup.wm_geometry("1000x500")
        promenna = StringVar()
        promenna.set("Recalculating lsi")
        w = Message(popup, text=u"Toto je relativně dlouhá zpráva", width=750, textvariable=promenna)
        w.pack(pady=150)
        popup.grab_set()
        popup.update_idletasks()
        dl.recalculate_lsi(promenna, popup)
        documents, U, S, conceptMatrix, values, terms, titles, texts = dl.load_data()
        print("done")
        promenna.set("Done")
        popup.update_idletasks()
        global data_loaded
        data_loaded = False
        win1()
        popup.destroy()




main = Tk()

mframe = Frame(main)
mframe.grid(row=0, column=0)
data_loaded = False
documents, U, S, conceptMatrix, values, terms, titles, texts = None, None, None,None,None,None,None,None

def clearwin(event=None):
    '''Clear the main windows frame of all widgets'''
    for child in mframe.winfo_children():
        child.destroy()

def win1(event=None):
    '''Create the main window'''
    popup = Toplevel()
    popup.title("Loading")
    popup.wm_geometry("1000x500")
    w = Message(popup, text=u"Loading", width=750)
    w.pack(pady=150)
    popup.grab_set()
    popup.update_idletasks()
    # ------- Init main form -------
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=13)
    main.option_add("*Font", default_font)
    main.title("LSI vector model")

    clearwin()
    label = Label(mframe, text="Select first document")
    # Get data
    global documents, U, S, conceptMatrix, values, terms, titles, texts, data_loaded
    if not data_loaded:
        documents, U, S, conceptMatrix, values, terms, titles, texts = dl.load_data()
        data_loaded = True

    # ------- Elements definition -------
    # scrollbar
    scrollbar = Scrollbar(mframe, orient=VERTICAL)
    # Listbox
    listbox = Listbox(mframe, height=23, width=60, yscrollcommand=scrollbar.set)
    i = 0
    for item in sorted(documents):
        if i != 0:
            listbox.insert(END, item)
        else:
            i = 1

    # ------- Settings + binding -------
    scrollbar.config(command=listbox.yview)
    # listbox.bind("<ButtonRelease-1>",
    #              lambda x: list_action(text=text, listbox=listbox, documents=documents, texts=texts, terms=terms,
    #                                    values=values, U=U, conceptMatrix=conceptMatrix, titles=titles, S=S))
    listbox.bind("<ButtonRelease-1>",
                 lambda x: win2(title_box=listbox.get(listbox.curselection()[0])))
    # ------- Adding to grid -------
    label.grid(row=0, column=0)
    scrollbar.grid(row=1, column=1, ipady=300)
    listbox.grid(row=1, column=0, padx=10, pady=10, ipadx=50, ipady=10)
    popup.destroy()



def win2(title_box, event=None):
    '''Create the second sub window'''
    clearwin()
    # Get data
    global documents, U, S, conceptMatrix, values, terms, titles, texts, data_loaded
    if not data_loaded:
        documents, U, S, conceptMatrix, values, terms, titles, texts = dl.load_data()
        data_loaded = True

    # ------- Elements definition -------
    # scrollbar
    scrollbar = Scrollbar(mframe, orient=VERTICAL)
    # Listbox
    listbox = Listbox(mframe, height=23, width=60, yscrollcommand=scrollbar.set)

    i = 0
    pos = 0
    for item in documents:
        listbox.insert(END, item)
        if item == title_box:
            pos = i
            break
        i += 1
    # Text
    text = Text(mframe, padx=10, pady=10)
    text.insert(END, "Select first document... ")
    # Button
    recalcButton = Button(mframe, text="Recalculate LSI", command=lambda: recalculate(documents, U, S, conceptMatrix, values, terms, titles, texts), bg="#363b40", fg="#c0c9d1")

    # ------- Settings + binding -------
    scrollbar.config(command=listbox.yview)
    listbox.bind("<ButtonRelease-1>", lambda x: list_action(text=text, listbox=listbox, documents=documents, texts=texts, terms=terms, values=values, U=U, conceptMatrix=conceptMatrix, titles=titles, S=S))

    # ------- Adding to grid -------
    scrollbar.grid(row=0, column=1, ipady=300)
    listbox.grid(row=0, column=0, padx=10, pady=10, ipadx=50, ipady=10)
    text.grid(row=0, column=2, padx=10, pady=10)
    recalcButton.grid(row=1, column=0)
    back = Button(mframe, command=win1, text='Back')
    back.grid(row=1, column=1)
    listbox.select_set(pos)
    list_action(text=text, listbox=listbox, documents=documents, texts=texts, terms=terms, values=values, U=U, conceptMatrix=conceptMatrix, titles=titles, S=S)

win1()

main.mainloop()


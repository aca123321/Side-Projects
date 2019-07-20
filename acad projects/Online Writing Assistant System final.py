from tkinter import *
from tkinter import messagebox
import enchant
from enchant.checker import SpellChecker
from nltk.corpus import wordnet as wn
import nltk
from PIL import *
    
d = enchant.Dict("en_UK")

class OWAS:
    def __init__(self,master):
        self.master = master
        self.container = Frame(master)
        self.container.pack(expand = True)
        
        self.frames = {} 

        for f in (LoginPage, StartPage, SpellPage, SynPage):
            page_name = f.__name__

            frame = f(parent = self.container, controller = self)
            frame["bg"] = "gray20"
            #here, self is an instance of the OWAS class
            self.frames[page_name] = frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame("LoginPage")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# **********************************************************************************************************************************

class LoginPage(Frame):

    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller

        self.untext = StringVar()
        self.pwtext = StringVar()

        self.label = Label(self, text = "Login", bg = "gray30" , width = 30, height = 5)
        self.label.place(x = 310, y = 50,anchor=CENTER)

        self.unframe = Frame(self)
        self.pwframe = Frame(self)
        
        self.unlabel = Label(self.unframe, text="Username:")
        self.pwlabel = Label(self.pwframe, text="Password :")
        self.unentry = Entry(self.unframe, textvariable =  self.untext,width = 25)
        self.pwentry = Entry(self.pwframe,show = "*", textvariable =  self.pwtext , width = 25)    

        self.unlabel.pack(side="left")
        self.pwlabel.pack(side="left")
        self.unentry.pack(side="left")
        self.pwentry.pack(side="left")

        self.unframe.place(x = 204, y = 150)
        self.pwframe.place(x = 204, y = 175)
        
        self.subbutton = Button(self,text ="Submit", command = lambda : self.login())
        self.subbutton.place(x = 312, y = 220,anchor=CENTER)

    def login(self):
        ut = self.untext.get()
        pt = self.pwtext.get()

        print(ut + " " + pt + "\n")
        
        if(ut == 'itone' and pt == 'rocks'):
            self.controller.show_frame("StartPage")
        elif(ut != 'itone' and pt != 'rocks'):
                messagebox.showinfo("Login Failed", "Incorrect Username and Password")
        elif(ut != 'itone' and pt == 'rocks'):
            messagebox.showinfo("Login Failed", "Incorrect Username")
        else:
            messagebox.showinfo("Login Failed", "Incorrect Password")
            


# **********************************************************************************************************************************


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller

        self.label = Label(self, text = "Choose:" , relief = "sunken" )
        self.label.pack(side= "top", fill = X)
        self.spellbutton = Button(self, text = "Spell Checker" ,  relief = "raised", command = lambda : controller.show_frame("SpellPage"))
        self.synbutton = Button(self, text = "Synonym Suggestions", relief = "raised", command = lambda : controller.show_frame("SynPage"))
        self.spellbutton.pack(side="left", expand = "True")
        self.synbutton.pack(side = "right", expand = "True")


# ***********************************************************************************************************************************

class SpellPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller

        self.tbox = Text(self,bg = "gray65")
        self.tbox.grid(row = 0,column=0,rowspan=5,columnspan=5)
       
        self.tsubmit = Button(self,text = "Check",command = self.submit)
        self.tsubmit.grid(row = 10, column = 1)
       
        self.back = Button(self, text = "Back" , command = self.backfun)
        self.back.grid(row=10, column= 3)
       
        self.resultbox = Text(self,bg = "gray65")
        self.resultbox.grid(row = 11, column = 0, rowspan = 5,columnspan =5)

    def submit(self):
        inp = self.tbox.get("1.0","end-1c")
        a = self.splitter(inp)
        a = self.checker(a,inp)
        result = ""

        for i in a:
            result = result + " " + i

        result = result[1:]
        self.resultbox.delete("1.0","end")
        self.resultbox.insert("1.0",result)
    
# Corrected words enclosed between two asterisks (*correctedword*)

    def checker(self,list,text):
        check = enchant.checker.SpellChecker("en_UK")
        check.set_text(text)

        spellfile = open("spelling.txt", "at")
        
        for i in check:
            sug = i.suggest()[0]
            if(str(i) != sug):
                i.replace("*" + sug + "*")
                temp = str(sug) + "\n"
                spellfile.write(temp)

        spellfile.close()
                
        c = check.get_text()
        a = c.split()
        return a

    def splitter(self,text):
        a = text.split()
        return a

    def backfun(self):
    #write code to delete all text from text box
        self.resultbox.delete("1.0","end")
        self.controller.show_frame("StartPage")


# *********************************************************************************************************************************


class SynPage(Frame):

    def __init__(self,parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller

        self.word = StringVar()

        self.enterframe = Frame(self)
        self.enterframe.grid(row = 0 , column = 0 , columnspan = 5)

        self.enterlabel = Label(self.enterframe, text = "Enter a word:", )
        self.enterlabel.pack(side="left")
        self.entrywidget = Entry(self.enterframe, textvariable = self.word,bg = "gray65")
        self.entrywidget.pack(side="left")

        self.suggestbutton = Button(self,text="Suggest", command = self.suggest)
        self.suggestbutton.grid(row = 2, column = 1 )

        self.backbutton = Button(self,text="Back", command = self.backfun)
        self.backbutton.grid(row = 2, column = 3 )

        self.textframe = Frame(self)
        self.textframe.grid(row  = 4, column = 0 , columnspan = 5,rowspan = 5)

        self.textwidget = Text(self.textframe,bg = "gray65")
        self.textwidget.grid(row = 0, column = 0, sticky="nsew")

    def wordgetter(self):
        return (self.word.get())

    def suggest(self):
        a = self.wordgetter()
        synonyms = []

        synfile = open("synonyms.txt", "at")
        temp = str(a) + "\n"
        synfile.write(temp)
        synfile.close

        for syn in wn.synsets(a):
            for l in syn.lemmas():
                synonyms.append(l.name())
        
        sugstr = ""

        for i in synonyms:
            sugstr = sugstr + str(i) + "\n"

        self.textsetter(sugstr)

    def backfun(self):
        self.textwidget.delete("1.0","end")
        self.controller.show_frame("StartPage")

    def textsetter(self,text):
        self.textwidget.delete("1.0","end")
        self.textwidget.insert("1.0",text)
    


win = Tk()
win.geometry("640x700")
win.title("OWAS")
app = OWAS(win)
win.mainloop()


######## A Healthcare Domain Chatbot to simulate the predictions of a General Physician ########
######## A pragmatic Approach for Diagnosis ############

# Importing the libraries
import pyttsx3
from tkinter import *
from tkinter import messagebox
import os
import webbrowser as wp
import webbrowser as wk
from tkinter import *
from PIL import Image, ImageTk
from translate import Translator 
translator=Translator(to_lang="Tamil")

import numpy as np
import pandas as pd


class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# Importing the dataset
training_dataset = pd.read_csv('Training.csv')
test_dataset = pd.read_csv('Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols     = training_dataset.columns
cols     = cols[:-1]


# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
from sklearn.tree import _tree

# Method to simulate the working of a Chatbot by extracting and formulating questions
def print_disease(node):
        #print(node)
        node = node[0]
        #print(len(node))
        val  = node.nonzero() 
        #print(val)
        disease = labelencoder.inverse_transform(val[0])
        return disease
def recurse(node, depth):
            global val,ans
            global tree_,feature_name,symptoms_present
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                yield name + " ?"
#                ans = input()
                ans = ans.lower()
                if ans == 'yes':
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    yield from recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    yield from recurse(tree_.children_right[node], depth + 1)
            else:
                strData=""
                present_disease = print_disease(tree_.value[node])
#                print( "You may have " +  present_disease )
#                print()
                resultstr=[]    
                strData="You may have : " +  str(present_disease[0])
                resultstr.append(strData)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n\n')                  
                
                red_cols = dimensionality_reduction.columns 
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
#                print("symptoms present  " + str(list(symptoms_present)))
#                print()
                strData="Symptoms present:  " + str(list(symptoms_present)[0])
                resultstr.append(strData)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n\n')                  
#                print("symptoms given "  +  str(list(symptoms_given)) )  
#                print()
                strData="Symptoms given: "  +  str(list(symptoms_given))[1:-1]
                 
                resultstr.append(strData)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n\n')                 
                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
#                print("confidence level is " + str(confidence_level))
#                print()
                strData="Confidence level is: " + str(confidence_level)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n\n')                  
#                print('The model suggests:')
#                print()                
                row = doctors[doctors['disease'] == present_disease[0]]
#                print('Consult ', str(row['name'].values))
#                print()
                strData="Suggested preventive measures are: "  +  str(row['ptip'].values[0])
                 
                resultstr.append(strData)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n\n') 
                strData='The model suggests: Consult '+ str(row['name'].values[0])
                x=strData
                

                resultstr.append(strData)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n\n')                  
#                print('Visit ', str(row['link'].values))
                #print(present_disease[0])

                
                # QuestionDigonosis.objRef.txtDigonosis.insert(END, link1.cget("button")+'\n')

                #QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n') 
                strData="Visit Profile Link: "
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)) 

                hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
                strData=str(row['link'].values[0]+'\n\n')
                def click1():
                    wk.open_new(str(row['link'].values[0]))
                QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
                strData="Google Map Refer Here: "
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)) 
                strData=str(row['hlink'].values[0]+'\n\n')
                def callback():
                    wk.open_new(str(row['hlink'].values[0]))
                QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(callback))
                strData='Click here for Voice Assistant...'
                def vm():
                    text_speech=pyttsx3.init() 
                    for x in resultstr:
                        text_speech.say(x)
                    text_speech.runAndWait()
                QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(vm))
                    
                
                # text_speech=pyttsx3.init() 
                # text_speech.say(x)
                # text_speech.runAndWait()                
                yield strData
        
def tree_to_code(tree, feature_names):
        global tree_,feature_name,symptoms_present
        tree_ = tree.tree_
        #print(tree_)
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        #print("def tree({}):".format(", ".join(feature_names)))
        symptoms_present = []   
#        recurse(0, 1)
    

def execute_bot():
#    print("Please reply with yes/Yes or no/No for the following symptoms")    
    tree_to_code(classifier,cols)



# This section of code to be run after scraping the data

doc_dataset = pd.read_csv('doctor_dataset1.csv', usecols=[0,1,2,3], names=['colA','colB','colC','colD'])


diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

doctors['disease'] = diseases['prognosis']


doctors['name'] = doc_dataset['colA']
doctors['link'] = doc_dataset['colB']
doctors['hlink'] = doc_dataset['colC']
doctors['ptip'] = doc_dataset['colD']

record = doctors[doctors['disease'] == 'AIDS']
record['name']
record['link']
record['hlink']
record['ptip']




# Execute the bot and see it in Action
#execute_bot()


class QuestionDigonosis(Frame):
    objIter=None
    objRef=None
    def __init__(self,master=None):
        master.title("Question")
        # root.iconbitmap("")
        master.state("z")
#        master.minsize(700,350)
        QuestionDigonosis.objRef=self
        super().__init__(master=master)
        self["bg"]="#85bbfa"
        self.createWidget() 
        self.iterObj=None

    def createWidget(self):
        self.lblQuestion=Label(self,text="MEDQUICK CHATBOT",width=30,fg="#064893",bg='#85bbfa',padx=10,pady=10,anchor='w',font=("Daft Brush",16,'bold'))
        self.lblQuestion.grid(row=0,column=0,columnspan=2)

        self.lblQuestion=Label(self,text="Question",width=12,bg="#064893",padx=10,pady=10,fg='white',font=("Daft Brush",13,'bold'))
        self.lblQuestion.grid(row=1,column=0,rowspan=4,padx=10)

        self.lblDigonosis = Label(self, text="Digonosis",width=12,bg="#064893",padx=10,pady=10,fg='white',font=("Daft Brush",13,'bold'))
        self.lblDigonosis.grid(row=5, column=0,sticky="n",pady=5)

        # self.varQuestion=StringVar()
        self.txtQuestion = Text(self, width=95,height=4,font=("Daft Brush",13,'bold'),fg='#064893')
        self.txtQuestion.grid(row=1, column=1,rowspan=4,columnspan=20,padx=10,pady=5)

        self.varDiagonosis=StringVar()
        self.txtDigonosis =Text(self, width=95,height=24,font=("Daft Brush",13,'bold'),fg='#064893')
        self.txtDigonosis.grid(row=5, column=1,columnspan=20,rowspan=20,padx=10,pady=5)

        self.btnNo=Button(self,text="No",width=12,bg="#064893",padx=7,pady=7,fg='white',font=("Daft Brush",13,'bold'),command=self.btnNo_Click)
        self.btnNo.grid(row=25,column=0,padx=10)
        self.btnYes = Button(self, text="Yes",width=12,bg="#064893",padx=7,pady=7,fg='white',font=("Daft Brush",13,'bold'), command=self.btnYes_Click)
        self.btnYes.grid(row=25, column=1,columnspan=20,sticky="e",padx=10)
        self.btnClear = Button(self, text="Clear",width=12,bg="#064893",padx=7,pady=7,fg='white',font=("Daft Brush",13,'bold'), command=self.btnClear_Click)
        self.btnClear.grid(row=28, column=0,pady=15,padx=10)
        self.btnStart = Button(self, text="Start",width=12,bg="#064893",padx=7,pady=7,fg='white',font=("Daft Brush",13,'bold'), command=self.btnStart_Click)
        self.btnStart.grid(row=28, column=2,columnspan=20,sticky="e",padx=10,pady=15)
    def btnNo_Click(self):
        global val,ans
        global val,ans
        ans='no'
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0,END)
        self.txtQuestion.insert(END,str1+"\n")
        
        
    def btnYes_Click(self):
        global val,ans
        ans='yes'
        self.txtDigonosis.delete(0.0,END)
        str1=QuestionDigonosis.objIter.__next__()
        
#        self.txtDigonosis.insert(END,str1+"\n")
        
    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
        self.txtDigonosis.insert(END,"Please Click on Yes or No for the Above symptoms in Question")                  
        QuestionDigonosis.objIter=recurse(0, 1)
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END,str1+"\n")


class MainForm(Frame):
    main_Root = None
    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        MainForm.main_Root = master
        super().__init__(master=master)
        width= master.winfo_screenwidth()
        height= master.winfo_screenheight() 
        master.geometry("%dx%d" % (width, height))
        master.title("Account Login")
        
        
           
        self.createWidget()
    def createWidget(self): 
        self.lblMsg=Label(self, text="Welcome to Account Registration Page", bg="white", width="100", height="2", bd="4",font=("Daft Brush",23,'bold'),fg="#57a1f8",borderwidth=1, relief="solid")
        self.lblMsg.pack()
        self.lblMsg=Label(self, text="Select the action you want to perfom",anchor="n", width="300", height="2",font=("Daft Brush", 13), fg="black")
        self.lblMsg.pack()
        self.lblMsg=Label(self,text='\n')
        self.lblMsg.pack()
        self.btnLogin=Button(self, text="Login",height="2", width="20",font=("Daft Brush",16,'bold'),fg='black', bg='#85bbfa', command=self.lblLogin_Click)
        self.btnLogin.pack()
        self.lblMsg=Label(self,text='\n')
        self.lblMsg.pack()
        self.btnRegister=Button(self, text="Register", height="2", width="20",font=("Daft Brush",16,'bold'),fg='black', bg='#85bbfa', command=self.btnRegister_Click)
        self.btnRegister.pack()
    def lblLogin_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmLogin=Login(MainForm.main_Root)
        frmLogin.pack()
    def btnRegister_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmSignUp = SignUp(MainForm.main_Root)
        frmSignUp.pack()
class Login(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        Login.main_Root=master
        super().__init__(master=master)
        width= master.winfo_screenwidth()
        height= master.winfo_screenheight() 
        master.geometry("%dx%d" % (width, height))
        master.title("Login")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Welcome to Login Portal", bg="white", width="100", height="2", bd="4",font=("Daft Brush",23,'bold'),fg="#57a1f8",borderwidth=1, relief="solid")
        self.lblMsg.pack()
        self.lblMsg=Label(self, text="Please fill in all the necessary details...",anchor="n", width="300", height="2",font=("Daft Brush", 13), fg="black")
        self.lblMsg.pack()
        self.lblMsg=Label(self,text='\n')
        self.lblMsg.pack()
        self.username=Label(self, text="Username",font=("Daft Brush",20,'bold'), fg='#57a1f8')
        self.username.pack()
        self.username_verify = StringVar()
        self.username_login_entry = Entry(self, textvariable=self.username_verify,width='30',highlightthickness=2,highlightcolor="#57a1f8")
        self.username_login_entry.pack(padx='10',pady='10')
        self.password=Label(self, text="Password",font=("Daft Brush",20,'bold'), fg='#57a1f8')
        self.password.pack()
        self.password_verify = StringVar()
        self.password_login_entry = Entry(self, textvariable=self.password_verify, show='*',width='30',highlightthickness=2,highlightcolor="#57a1f8")
        self.password_login_entry.pack(padx='10',pady='10')
        self.lblMsg=Label(self,text='\n')
        self.lblMsg.pack()
        self.btnLogin=Button(self, text="Login", width=10, height=1,font=("Daft Brush",16,'bold'),fg='black', bg='#85bbfa', command=self.btnLogin_Click)
        self.btnLogin.pack()
    def btnLogin_Click(self):
        username1 = self.username_login_entry.get()
        password1 = self.password_login_entry.get()
#        messagebox.showinfo("Failure", self.username1+":"+password1)
        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                messagebox.showinfo("Sucess","Login Sucessful")
                self.destroyPackWidget(Login.main_Root)
                frmQuestion = QuestionDigonosis(Login.main_Root)
                frmQuestion.pack()
            else:
                messagebox.showinfo("Failure", "Login Details are wrong try again")
        else:
            messagebox.showinfo("Failure", "User not found try from another user\n or sign up for new user")
class SignUp(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        SignUp.main_Root=master
        master.title("Register")
        super().__init__(master=master)
        width= master.winfo_screenwidth()
        height= master.winfo_screenheight() 
        master.geometry("%dx%d" % (width, height))
        master.title("Register")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Welcome to Registration Portal", bg="white", width="100", height="2", bd="4",font=("Daft Brush",23,'bold'),fg="#57a1f8",borderwidth=1, relief="solid")
        self.lblMsg.pack()
        self.lblMsg=Label(self, text="Please fill in all the necessary details...",anchor="n", width="300", height="2",font=("Daft Brush", 13), fg="black")
        self.lblMsg.pack()
        self.username_lable = Label(self, text="Enter Username",font=("Daft Brush",20,'bold'), fg='#57a1f8')
        self.username_lable.pack()
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username,width='30',highlightthickness=2,highlightcolor="#57a1f8")
        self.username_entry.pack(padx=10,pady=10)
        self.password_lable = Label(self, text="Enter Password",font=("Daft Brush",20,'bold'), fg='#57a1f8')
        self.password_lable.pack()
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable=self.password, show='*',width='30',highlightthickness=2,highlightcolor="#57a1f8")
        self.password_entry.pack(padx=10,pady=10)
        self.lblMsg=Label(self,text='\n')
        self.lblMsg.pack()
        self.btnRegister=Button(self, text="Register", width=10, height=1,font=("Daft Brush",16,'bold'),fg='black', bg='#85bbfa', command=self.register_user)
        self.btnRegister.pack()
    def register_user(self):
#        print(self.username.get())
#        print("Hello")
        
        
        file = open(self.username_entry.get(), "w")
        file.write(self.username_entry.get() + "\n")
        file.write(self.password_entry.get())
        file.close()
        self.destroyPackWidget(SignUp.main_Root)
        self.lblSucess=Label(root, text="Registration Success", fg="green", font=("calibri", 11))
        self.lblSucess.pack()
        self.btnSucess=Button(root, text="Click Here to proceed", command=self.btnSucess_Click)
        self.btnSucess.pack()
    def btnSucess_Click(self):

        self.destroyPackWidget(SignUp.main_Root)
        frmQuestion = QuestionDigonosis(SignUp.main_Root)

        frmQuestion.pack()



root = Tk()

frmMainForm=MainForm(root)
frmMainForm.pack()
root.mainloop()



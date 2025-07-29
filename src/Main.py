from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import numpy as np 
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from collections import defaultdict
from sklearn import metrics

main = tkinter.Tk()
main.title("Detecting Malicious Twitter Bots Using Machine Learning") #designing main screen
main.geometry("1300x1200")

global filename
global dataset

words = ['bot','cannabis','tweet me','mishear','follow me','updates','every','gorilla','forget']

def getFrequency(bow):
    count = 0
    for i in range(len(words)):
        if words[i] in bow:
            count = count + bow.get(words[i])
    return count        

def uploadDataset():
    global filename
    text.delete('1.0', END)
    filename = filedialog.askopenfilename(initialdir="Dataset")
    text.insert(END,filename+" loaded\n\n")
    
def runModule1():
    global dataset
    text.delete('1.0', END)
    dataset = pd.read_csv(filename)
    text.insert(END,str(dataset))    

def runModule2():
    text.delete('1.0', END)
    train = dataset[['screen_name','status','name','followers_count', 'friends_count', 'listedcount', 'favourites_count', 'statuses_count', 'verified']]
    details = train.values
    text.insert(END,"Possible BOT users\n\n")
    users = []
    for i in range(len(details)):
        screen = details[i,0]
        status = details[i,1]
        name = details[i,2]
        followers = int(details[i,3])
        friends = int(details[i,4])
        listed = int(details[i,5])
        favourite = int(details[i,6])
        status_count = int(details[i,7])
        verified = details[i,8]
        if not verified: #check user not verified
            bow = defaultdict(int) #bag of words
            data = str(screen)+" "+str(name)+" "+str(status)#checking screen name, tweets and name
            data = data.lower().strip("\n").strip()
            data = re.findall(r'\w+', data)
            for j in range(len(data)):
                bow[data[j]] += 1  #adding each word frequency to bag of words
            frequency = getFrequency(bow) #getting frequency of BOTS words            
            if frequency > 0 and listed < 16000 and followers < 200: #if condition true then its bots
                users.append(screen)
    text.insert(END,str(users)+"\n")            
    train_attr = dataset[
        ['followers_count', 'friends_count', 'listedcount', 'favourites_count', 'statuses_count', 'verified']]
    train_label = dataset[['bot']]

    X = train_attr
    Y = train_label.to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    logreg = LogisticRegression().fit(X_train, y_train)#logistic regression object
    actual = y_test
    pred = logreg.predict(X_test)
    accuracy = accuracy_score(actual, pred) * 100
    precision = precision_score(actual, pred) * 100
    recall = recall_score(actual, pred) * 100
    f1 = f1_score(actual, pred)
    auc = roc_auc_score(actual, pred)
    text.insert(END,'\nLogistic Regression Accuracy  : '+str(accuracy)+"\n")
    text.insert(END,'Logistic Regression Precision : '+str(precision)+"\n")
    text.insert(END,'Logistic Regression Recall is : '+str(recall)+"\n")
    text.insert(END,'Logistic Regression Area Under Curve is : '+str(auc))

    fpr, tpr, thresholds = metrics.roc_curve(actual, pred)
    auc = metrics.auc(fpr, tpr)
    plt.title('ROC')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f'% auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


def runModule3():
    text.delete('1.0', END)
    urls = []
    details = dataset.values
    for i in range(len(details)): #checking URLS in tweets
        tweets = str(details[i,14])
        if 'http' in tweets:
            urls.append(1)
        else:
            urls.append(0)

    train_attr = dataset[
        ['followers_count', 'friends_count', 'listedcount', 'favourites_count', 'statuses_count', 'verified']].copy()
    train_attr["URLS"] = urls #adding URLS to training dataset
    text.insert(END,str(train_attr))
    train_label = dataset[['bot']]
    X = train_attr
    Y = np.asarray(train_label)

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    logreg = LogisticRegression().fit(X_train, y_train) #logistic regression object
    actual = y_test
    pred = logreg.predict(X_test)
    accuracy = accuracy_score(actual, pred) * 100
    precision = precision_score(actual, pred) * 100
    recall = recall_score(actual, pred) * 100
    f1 = f1_score(actual, pred)
    auc = roc_auc_score(actual, pred)
    text.insert(END,'\nLogistic Regression Accuracy  : '+str(accuracy)+"\n")
    text.insert(END,'Logistic Regression Precision : '+str(precision)+"\n")
    text.insert(END,'Logistic Regression Recall is : '+str(recall)+"\n")
    text.insert(END,'Logistic Regression Area Under Curve is : '+str(auc))

    fpr, tpr, thresholds = metrics.roc_curve(actual, pred)
    auc = metrics.auc(fpr, tpr)
    plt.title('ROC')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f'% auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


font = ('times', 16, 'bold')
title = Label(main, text='Detecting Malicious Twitter Bots Using Machine Learning')
title.config(bg='goldenrod2', fg='black')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=50,y=120)
text.config(font=font1)

font1 = ('times', 13, 'bold')
uploadButton = Button(main, text="Upload Tweets Dataset", command=uploadDataset, bg='#ffb3fe')
uploadButton.place(x=50,y=550)
uploadButton.config(font=font1)  

module1Button = Button(main, text="Run Module 1 (Extract Tweets)", command=runModule1, bg='#ffb3fe')
module1Button.place(x=450,y=550)
module1Button.config(font=font1) 

module2Button = Button(main, text="Run Module 2 (Recognize Twitter Bots using ML)", command=runModule2, bg='#ffb3fe')
module2Button.place(x=50,y=600)
module2Button.config(font=font1) 

module3Button = Button(main, text="Run Module 3  (Recognize Malicious URLS using ML)", command=runModule3, bg='#ffb3fe')
module3Button.place(x=450,y=600)
module3Button.config(font=font1) 

main.config(bg='SpringGreen2')
main.mainloop()

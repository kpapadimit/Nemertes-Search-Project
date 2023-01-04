import requests
from bs4 import BeautifulSoup
from tkinter import *
import os
import re
import sys
import urllib.request



#Ελεγχος για την σύνδεση στο διαδίκτυο
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) 
        return True
    except:
        return False
if connect():
    print("Connected")
else:
    root0=Tk()
    internet_error=Label(root0,text="Error! \n Δεν υπάρχει σύνδεση στο διαδίκτυο.",font="Arial 15")
    root0.title("Error!")
    internet_error.pack()
    root0.mainloop()
    sys.exit()


#Συνάρτηση που κατεβάζει τα link
def extract_all_links(site):
    html=requests.get(site).text
    soup=BeautifulSoup(html,"html.parser").find_all("a")
    links=[link.get("href") for link in soup]
    return links


#Συναρτηση που ανοιγει σημειοματάριο με τα Καταχωρημένα Μεταπτυχιακά
def notedidaktorika():
    os.startfile("Καταχώρημενα Διδακτορικά.txt")




#Δημιουργία γραφικών
root = Tk()


def getInput():
    

    a = name.get()
    res = bool(re.search(r"\s", a))
    global params
    #έλεγχος για ύπαρξη <space> στο όνομα που δίνει ο χρήστης
    if res=="True":
        epitheto,onoma=a.split(" ")
        params=[epitheto,onoma]
        root.destroy()
        print("Loading...")
       
    else:
        params=[a,"-"]
        root.destroy()
        print("Loading...")

  
def grafika():
    global name
    canvas1 = Canvas(root)
    canvas1.pack(side="top",fill="both",expand="yes")
    gif1 = PhotoImage(file = "background.gif")
    canvas1.create_image(0 , 0, image = gif1, anchor = NW)




    
    label1 = Label(root, text='Πρόγραμμα Εύρεσης Διδακτορικών',bg="black",fg='white')
    label1.config(font=('Comic Sans MS', 25, "bold"))
    canvas1.create_window(335, 75, window=label1)

    label2 = Label(root, text='Πληκτρολόγησε "Επωνυμο Ονομα" συγγραφεα:',bg='black',fg='white')
    label2.config(font=('Comic Sans MS', 15, "bold"))
    canvas1.create_window(310, 150, window=label2)

    name = Entry(root,font=("Comic Sans MS",15)) 
    canvas1.create_window(310, 210 , window=name)


    
    button1 = Button(text='Search', command=getInput, bg='#FFC100', fg='black', font=('Comic Sans MS', 11, 'bold'))
    canvas1.create_window(315, 275 , window=button1)

    button2=Button(text="Κανε κλίκ για να δεις τα καταχωρημένα Διδακτορικά",bg='#01fff4',fg="black",font=('Comic Sans MS', 7),command=notedidaktorika)
    canvas1.create_window(310,325,window=button2)

    
    root.title("Προγραμμα Ευρεσης Διδακτορικών")
    root.geometry("630x350")   

    mainloop()
grafika()





#Εύρεση του link μέσω του ονόματος στα Αγγλικά-Αναζήτηση σε όλες τις σελίδες διδακτορικών της ιστοσελίδας του πανεπιστημίου
words=[params[0],params[1]]


def link_search():
    

    for i in range(1,13):
        link1=" https://nemertes.library.upatras.gr/browse/author?scope=744f82fa-a28b-446e-9e04-8616053fb4a5&bbm.page={}&bbm.sd=ASC&bbm.rpp=100".format(str(i))
        all_links=extract_all_links(link1)
        a=all_links[24:-21]
        global newlink
        newlink=[item for item in a if all((word in item) for word in words)]
        if newlink == []:
            continue
        else:
            break

link_search()

def teliko_link():
    global pdf_link
    if newlink==[]:
        root2=Tk()
        error=Label(root2,text='Error! \n Πληκτρολόγησες μη έγκυρο όνομα συγγραφέα',font='Arial 15')
        root2.title("Error")
        error.pack()
        root2.mainloop()
        sys.exit()
    else:
        arxiko="https://nemertes.library.upatras.gr"
        link2=arxiko + newlink[0]
        all_links2=extract_all_links(link2)
        link3= arxiko + all_links2[-9]
        all_link3= extract_all_links(link3)
        pdf_link=arxiko+ all_link3[-11]

teliko_link()


#Συνάρτηση που κατεβάζει τα pdf από την ιστοσελίδα
def download_pdf_file(url: str) -> bool:
   
    response = requests.get(url, stream=True)

   
    pdf_file_name = os.path.basename(url)
    if response.status_code == 200:
        
        filepath = os.path.join(os.getcwd(), pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            return True
    

#Αποθήκευση αρχείου και μετατροπή του σε pdf μέσω μετονομασίας 
if __name__ == '__main__':
    
    download_pdf_file(pdf_link)
    address= os.getcwd()
    pdf="download"
    
    old_name = r"{}".format(os.path.join(os.getcwd(),pdf))
    new_name = r"{}.pdf".format(os.path.join(os.getcwd(),params[0]+params[1]))
    os.rename(old_name, new_name)
    path=params[0]+params[1]+".pdf"
    os.startfile(path)
  



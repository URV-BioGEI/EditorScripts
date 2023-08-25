#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import messagebox as tkMessageBox # Per a mostrar els dialegs
from tkinter import *
from tkinter import filedialog as tkFileDialog
from tkinter import scrolledtext as tkst
import os 	#Importem el modul del sistema per a utilitzar comandes de la shell
import subprocess
from subprocess import Popen, PIPE
import sys
import time
import random
import inspect
#MAIN
#Paràmetres de finestra principal

class MyDialog:
    top = None
    def __init__(self, parent, stdouttxt):
        top = self.top = Toplevel(parent)
        stout = tkst.ScrolledText(
            master=top,  # incloem a la finestra fout aquest objecte
            wrap='word',  # Fem que el text sigui de paraules (?)
            width=60,  # carácters per fila
            height=12,  # linies de text
            bg='beige'  # color de fons
        )
        stout.pack(expand=TRUE, fill=BOTH, side=TOP, padx=8, pady=8)
        stout.delete(1.0, END)  # Fem un clean del text
        stout.insert(END, stdouttxt)  # Insertem el contingut del stdout

        b = Button(top, text="Close", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.top.destroy()


def EscullDirectori():
    global directori
    directori=tkFileDialog.askdirectory(
        parent=mainw,	# Fa que la nova finestra sigui pare de la finestra principal
        title="Escollir directori", #Títol de la finestra
        mustexist=TRUE )	#El directori ha d'existir
    l1.configure(text=directori) # Assignem el directori al label


#Funció Obrir Script:
# S'encarrega d'obrir l'Script a partir del nom (Entry e1) 
# i de la ruta escollida (Label l1) 
# i mostrar el contingut en el ScrolledText st
# Cal implementar el cas de que el fitxer no existeixi o no tingui l'extensió sh
# Cal implementar algun tipus de comunicació (variable global) per a que guardar Script sàpiga
# Si pot executar-se o no. (si hem obert algun script amb anterioritat)
def ObrirScript():
    global file # Fem la variable fitxer global per a modificar-la
    file=tkFileDialog.askopenfilename(initialdir=directori, title="Obrir fitxer", filetypes=[("Fitxers d'Scripts Bash", "*.sh")])
    if file:									# Si no escollim cap fitxer, llavors no entrem al if
        try:
            global nomf							# Accedim a la memoria global
            nomf = os.path.basename(file)		# Obtenim el nom del fitxer
            e1.delete(0, END)					# Borrem el contingut de l'entry
            e1.insert(0, nomf)					# I li assiggnem el nom del fitxer
            f = open (file, 'r')				# Obrir fitxer, en mode lectura
            content=f.read()					# Llegim tot el fitxer i l'emmagatzemem
            st.delete(1.0,END)					# Fem un clean del text
            st.insert(END, content)				# Insertem el contingut del fitxer
            f.close()							# Tanquem el fitxer
        except IOError:
            tkMessageBox.showerror(title="Error I/O", message="Error E/S")	# Si captem una excepció E/S mostrem el missatge


# Funció Guardar Script
# S'encarrega d'agafar el contingut del ScrolledText st i passar-lo al fitxer que ja ha sigut obert obert
# Per a executar-se un fitxer ha hagut de ser obert prèviament
def GuardarScript():
    if file!=0:					# Si el flag no es troba actiu...
        try:
            f = open(file, 'w+')		# Obrim el fitxer en mode escriptura +, farà clean abans
            text = st.get(1.0, END)		# Obtenim el text del text box
            f.write(text)				# Guardem el text al fitxer
            f.close()					# Tanquem fitxer
        except IOError:
            tkMessageBox.showerror(title="Error I/O", message="Error E/S")	# Si captem una excepció E/S mostrem el missatge
    else:								# ...Mostrem missatge d'error
        tkMessageBox.showerror(title="Error I/O", message="Per a guardar cal carregar un fitxer abans")	# Si captem una excepció (que el fitxer no existeixi) mostrem el missatge


#Genera un nou script amb el nom indicat a l'Entry e1 en el directori que indica label l1
#Cal fer dues excepcions si no hi han valors o bé el string de nom de fitxer es incorrecte
def GuardarNouScript():						
        try:
            f=tkFileDialog.asksaveasfile(initialdir=directori, title="Guardar com", defaultextension='.sh')
            if f:
                text=st.get(1.0, END)
                f.write(text)
                f.close()
        except IOError:
            tkMessageBox.showerror(title="Error I/O", message="Error E/S")	# Si captem una excepció E/S mostrem el missatge


# Crea una subfinestra per a visualitzar si existeix la sortida de la
# darrera execució de l’script.
def VeureStderr():
    r = MyDialog(mainw, stderrtxt)
    mainw.wait_window(r.top)

# Crea una subfinestra per a visualitzar si existeix la sortida de la
# darrera execució de l’script.
def VeureStdout():
    # global stout
    d = MyDialog(mainw, stdouttxt)
    mainw.wait_window(d.top)


# Executa l’script escollit amb els arguments i redireccions
# indicades de manera immediata.
def RunNow():
    global st, stdouttxt, stderrtxt						# Accedim a variables globals
    ubicacio="/tmp/tmp.sh"								# Assignem la ubicació del fitxer temporal script
    arguments = ubicacio + " " +e2.get()				# Obtenim els arguments (executar script i passar arguments)
    com = st.get(1.0, END)								# Obtenim el text del fitxer
    f = open(ubicacio, 'w+')							# Obrim el fitxer en mode escriptura +, farà un clean abans d'escriure
    f.write(com)										# Escrivim el script
    f.close()											# Tanquem el fitxer
    os.system("chmod +x /tmp/tmp.sh")					# Donem permisos d'execució
    rc = subprocess.Popen(								# Cridem al modul subprocess
    arguments, 											# Li passem les comandes (execució + parametres)
    shell=True,											# Pel tipus de crida aquest ha de ser true
    stdout=PIPE,										# Per a poder obtenir stdout
    stderr=PIPE)										# Per a poder obtenir stderr
    stdouttxt, stderrtxt = rc.communicate()				# Obtenim les sortides
# Part dels checkboxes
    if std1.get():										# Si l'usuari ha marcat el checkbox del stdout...
        if nomf!=0:										# Si s'ha obert un fitxer
            f = open (nomf+".out", 'w+')				# Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stdouttxt)							# Hi escrivim la sortida
            f.close()									# Tanquem
        else:											# Sino li donem un altre nom
            f = open ("script.out", 'w+')				# Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stdouttxt)							# Hi escrivim la sortida
            f.close()									# Tanquem
    if std2.get():										# Si l'usuari ha marcat el checkbox del stderr...
        if nomf!=0:										# Si s'ha obert un fitxer
            f = open (nomf+".err", 'w+')				# Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stderrtxt)							# Hi escrivim la sortida
            f.close()									# Tanquem
        else:											# Sino li donem un altre nom
            f = open ("script.err", 'w+')				# Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stderrtxt)							# Hi escrivim la sortida
            f.close()									# Tanquem


# Programa l’execució de l’script mitjançant la comanda «at» a una
# hora i minut determinats. Caldrà buscar informació sobre la comanda
# Obtenim el temps en el format HH:MM -> e4:e3
def RunLate():
    global st, stdouttxt, stderrtxt  # Accedim a variables globals
    try:
        rnd = random.randrange(10000)
        segons = int(e4.get())
        if(segons > 0):
            ubicacio="/tmp/" + str(rnd) + "Late.sh"
            arguments = "sleep " + str(segons) + " && " + ubicacio + " " + e2.get()  # Obtenim els arguments (executar script i passar arguments)
            com = st.get(1.0, END)  # Obtenim el text del fitxer
            f = open(ubicacio, 'w+')  # Obrim el fitxer en mode escriptura +, farà un clean abans d'escriure
            f.write(com)  # Escrivim el script
            f.close()  # Tanquem el fitxer
            os.system("chmod +x " + ubicacio)  # Donem permisos d'execució
            rc = subprocess.Popen(arguments, shell=True, stdout=PIPE, stderr=PIPE)
        else:
            tkMessageBox.showerror(title="Error de temps", message="Trieu un número vàlid de segons i major que 0.")  # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
    except Exception as e:
        tkMessageBox.showerror(title="Error de temps",
                           message="Trieu un número vàlid de segons i major que 0.")  # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
    

# Corre l'script en un moment determinat en format de at
def RunAt():	# (?) falta la part de les excepcions
    try:
        rnd = random.randrange(10000)
        commands = e7.get()
        if not commands:
            tkMessageBox.showerror(title="Error en les comandes.", message="Introduiu una comanda AT Vàlida. Tingueu en compte que l'String \"At \" ja s'afegeix automàticament.")  # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
        else:
            if directori==0:
                ubicacio = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"  # Assignem la ubicació del fitxer temporal script
            else:
                ubicacio=directori +"/"
            fitxer=ubicacio+str(rnd)+"At.sh"
            arguments = "at " + commands + " -f " + "\"" + fitxer + "\"" + e2.get() + ""  # Obtenim els arguments (executar script i passar arguments) (?) he suposat que lo de commands es loque hi ha a entry 7
            com = st.get(1.0, END)  # Obtenim el text del fitxer
            f = open(fitxer, 'w+')  # Obrim el fitxer en mode escriptura +, farà un clean abans d'escriure
            f.write(com)  # Escrivim el script
            f.close()  # Tanquem el fitxer
            os.system("chmod +x \""+ fitxer + "\"")  # Donem permisos d'execució
            rc = subprocess.Popen(arguments, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = rc.communicate()
        if err:
            tkMessageBox.showerror(title="Error", message=err)
    except Exception as e:
        tkMessageBox.showerror(title="Error en els segons.", message="Trieu un número vàlid de segons i major que 0.")  # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge


"""En la programació de l’execució de l’script de manera periòdica. Permetre
tota la potencia de descripcions del temps de la comanda «crontab». Caldrà modificar
els camps que indiquen el temps per a tenir com a mínim cinc camps strings per a
indicar el temps en que s’ha d’executar l’script. (format * * * * *)"""

def RunPeriod():
    global st, file
    rnd = random.randrange(10000)
    com = st.get(1.0, END)												# Obtenim el text del fitxer
    if directori==0:
        ubicacio = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"  # Assignem la ubicació del fitxer temporal script
    else:
        ubicacio=directori
    fitxer=ubicacio + str(rnd) + "Period.sh"
    # Obtenir informació
    correcte = 1													# Flag per entrar a la funció (comprova que tot estigui bé)
    dS = e5.get()													# Obtenim el camp dS
    if not dS:
        correcte = 0												# Si esta buit, posem un 0 per a indicar que esta malament
    Mes = e6.get()													# Així successivament
    if not Mes:
        correcte = 0
    dM = e8.get()
    if not dM:
        correcte = 0
    hh = e9.get()
    if not hh:
        correcte = 0
    mm = e10.get()
    if not mm:
        correcte = 0
    if correcte == 1:												# Mirem que tots siguin correctes
        f = open(fitxer , 'w+')										# Obrim el fitxer en mode escriptura +, farà un clean abans d'escriure
        fitxerc = "\"" + fitxer + "\""
        fitxerq = "\"" + fitxer + "\""
        f.write(com)													# Escrivim el script (?) falta el nombre aleatori
        f.close()														# Tanquem el fitxer
        os.system("chmod +x " + fitxerq)								# Donem permisos d'execució
        s_file = open(ubicacio + "/crontask", 'w+')
        s_file.write(mm + " " + hh + " " + dM + " " + Mes + " " + dS + " " +fitxerc + "\n")
        s_file.close()
        # stri = "echo \"" + mm + " " + hh + " " + dM + " " + Mes + " " + dS + " " + "\\" +fitxerc +  "\" >> " + "\"" + ubicacio + "crontask" + "\"" # Generem l'string
        # os.system(stri)
        # print stri
        print(ubicacio)
        cron = subprocess.Popen("crontab " + ubicacio + "/crontask", shell=True, stdout=PIPE, stderr=PIPE)  # Obtenim nom d'usuari
        out, err = cron.communicate()
        if err:
            tkMessageBox.showerror(title="Error", message="Format incorrecte de crontab: m correspon al minut en què es va a executar el script, el valor va de 0 a 59h l'hora exacta, es maneja el format de 24 hores, els valors van de 0 a 23, sent 0 les 12:00 de la mitjanit.diu fa referència al dia del mes, per exemple es pot especificar 15 si es vol executar cada dia 15 dow significa el dia de la setmana, pot ser numèric (0 a 7, on 0 i 7 són diumenge) o les 3 primeres lletres del dia en anglès: mon, tue, wed, thu, fri, sat, sun.")
    else:
        tkMessageBox.showerror(title="Falten dades", message="Emplena tots els camps de l'esquerra")  # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
    """except IOError:
        tkMessageBox.showerror(title="Error en els segons.", message="Trieu un número vàlid de segons i major que 0.")  # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
"""


mainw=Tk()
mainw.title("Execució d'Scripts en el temps")

#Var
file = 0						# 0 si no s'ha carregat cap fitxer, ruta al fitxer incloent el nom si ja s'ha carregat
directori = 0					# 0 si no s'ha carregat, directori de treball actual si s'ha carregat
nomf = 0						# 0 si no s'ha obert cap fitxer, nom del fitxer obert si s'ha carregat fitxer
stdouttxt = ""					# String amb stdout
stderrtxt = ""					# String amb stderr
#Elements main window
#{
f1=Frame(mainw, bg="grey")	#Creem primer frame, li donem el color gris
f1.pack(fill=X, side=TOP)	#aliniem a la part de dalt i li permetem expandir-se en X


b1=Button(f1,text='Escollir directori de treball',command=EscullDirectori)	#Creem el botó i li assignem la comanda de preguntar el directori
b1.pack(side=LEFT)	 #l'apilem a l'esquerra

l1=Label(f1,text="")	#"label" que mostra el directori actual
l1.pack(expand=TRUE, fill=X, side=RIGHT, anchor=W)	#Li permeten exapndre's al llarg de la finestra en X, l'apilem a la dreta
#}
f2=Frame(mainw) #Creem primer frame,
f2.pack(side=TOP, fill=X) #aliniem a la part de dalt i li permetem expandir-se
#{


b2=Button(f2, text="Obrir Script", command=ObrirScript) #botó per a obrir script
b2.pack(side=LEFT) #l'apilem a l'esquerra

e1=Entry(f2,width=20)	#entrada de text per a posar el nom del fitxer
e1.pack(expand=TRUE, fill=X, side=LEFT)	# li permetem expandir-se en X i l'apilem a l'esquerra


b3=Button(f2, text="Guardar l'Script", command=GuardarScript) # Botó per a dur a terme la funció de guardat
b3.pack(side=RIGHT)	#L'apilem a la dreta


b4=Button(mainw, text="Guardar en un nou script", command=GuardarNouScript)	#Botó per a generar la funció de dalt
b4.pack(side=TOP, anchor=W) #l'apilem a la part de dalt del frame on ens trobem
#}
#{
# Es una de les components principal del programa.
# Esta fet de tres objectes, un TextBox, un ScrollBar i un frame que els conté
# D'aquesta manera es com si fos un pack ja implementat amb el seus propis métodes
st=tkst.ScrolledText(
    master = mainw,	  # incloem a la finestra principal aquest objecte
    wrap   = 'word',  # Fem que el text sigui de paraules (?)
    width  = 25,      # carácters per fila
    height = 17,      # linies de text
    bg='beige'        # color de fons
)

st.pack(expand=TRUE, fill=BOTH, side=TOP, padx=8, pady=8)	#Apilem i permetem l'expansió. Els altres valors son la mida del text (?)
#}
#{
f3=Frame(mainw) #tercer frame
f3.pack(side=TOP, fill=X)	# procedim igual que els anteriors

l2=Label(f3, text="Arguments d'entrada :") # creem el label que indica els arguments d'entrada.
l2.pack(side=LEFT) 	# apilem a l'esquerra

e2=Entry(f3)	# entrada de text per als arguments
e2.pack(expand=TRUE, fill=X, side=LEFT) # l'apilem i li permeten fer-se gran

# Permet redireccionar la sortida de l'execució de l’script a un fitxer.
# El nom d’aquest fitxer serà en nom de l’script amb extensió «.out»
# Sera consultat per tots els botons run
std1 = IntVar()
cb1=Checkbutton(f3, text="Genera Stdout", variable=std1)	# checkbox per a saber si cal generar stdout en un fitxer
cb1.pack(side=LEFT)

# Permet redireccionar la sortida d’error de l'execució de l’script a un
# fitxer. El nom d’aquest fitxer serà en nom de l’script amb extensió «.err»
# Sera consultat per tots els botons run
std2 = IntVar()
cb2=Checkbutton(f3, text="Genera Stderr", variable=std2) 	# checkbox per a saber si cal generar stderr en un fitxer
cb2.pack(side=LEFT)
#}
#{
f4=Frame(mainw)	# afegim un nou frame
f4.pack(side=TOP, fill=X)	# l'apilem cap a dalt i emplenem en X


b5=Button(f4, text="Veure Stderr", command=VeureStderr) 	# Botó que executa la funció de dalt
b5.pack(side=RIGHT)		# Ho apilem a la part dreta


b6=Button(f4, text="Veure Stdout", command=VeureStdout) # Botó que executa la funció de dalt.
b6.pack(side=RIGHT) # Apilem a la dreta
#}
#{
f5=Frame(mainw)	# Afegim un nou frame
f5.pack(side=TOP, fill=X) #apilem a dalt i permetem l'expansió


b5=Button(f5, text="Run", command=RunNow)	#Executa la funció de dalt
b5.pack(side=RIGHT)		# apilem a la dreta

l3=Label(f5, text="Executa immediatament")	# label de descripció del botó b5
l3.pack(side=RIGHT)
#}
#{
f6=Frame(mainw)	#Afegim un nou frame. Aquest frame implementa tot el relacionat amb executar a n determinat temps
f6.pack(side=TOP, fill=X)	# apilem a dalt i permetem l'expansió X

b6=Button(f6, text="RunLate", command=RunLate)	#Executa la funció de dalt
b6.pack(side=RIGHT)	# Apilem a la dreta

l4=Label(f6, text="  segons. ") # label de text
l4.pack(side=RIGHT) # Apilem a la dreta

e4=Entry(f6, width=3) # entrada de text per a les hores de la funció run late
e4.pack(side=RIGHT) # Apilem a la dreta

l6=Label(f6, text="Executa d'aquí a: ")	# label
l6.pack(side=RIGHT) # Apilem a la dreta
#}
#{
f9=Frame(mainw) 	# Frame de la part opcional de executa amb format at, per això no segueix la numeració
f9.pack(side=TOP, fill=X)


b9=Button(f9, text="RunAt", command=RunAt)	# Botó per a executar la funció anterior
b9.pack(side=RIGHT) # Apilem a la dreta

l10=Label(f9, text="  de 'at'   ")	# label
l10.pack(side=RIGHT) # Apilem a la dreta

e7=Entry(f9, width=7) # entrada de text que correspon a les hores
e7.pack(side=RIGHT) # Apilem a la dreta

l11=Label(f9, text="Executa un cop amb format ")	# label
l11.pack(side=RIGHT) # Apilem a la dreta
#}
#{
f7=Frame(mainw)		# Afegim un frame. Aquest contindrà els botons per a executar l'script periodicament
f7.pack(side=TOP, fill=X)	# ho posem a la paret nort i expandim en x

b7=Button(f7, text="RunPeriod", command=RunPeriod)	# Botó per a executar la funció anterior
b7.pack(side=RIGHT) # Apilem a la dreta

l7=Label(f7, text=" crontab  ")	# label de text informatiu
l7.pack(side=RIGHT) # Apilem a la dreta

e5=Entry(f7, width=2) # entrada de text dS
e5.pack(side=RIGHT) # Apilem a la dreta

e6=Entry(f7, width=2) # entrada de text Mes
e6.pack(side=RIGHT) # Apilem a la dreta

e8=Entry(f7, width=2) # entrada de text dM
e8.pack(side=RIGHT) # Apilem a la dreta

e9=Entry(f7, width=2) # entrada de text hh
e9.pack(side=RIGHT) # Apilem a la dreta

e10=Entry(f7, width=2) # entrada de text mm
e10.pack(side=RIGHT) # Apilem a la dreta

l9=Label(f7, text="Programa cada dia amb format") # label de text informatiu
l9.pack(side=RIGHT) # Apilem a la dreta
#}
#{
f10=Frame(mainw)		# frame per als labels del camp de crontab
f10.pack(side=TOP, fill=X) # Apilem a la esquerra i permetem l'expansió X

l12=Label(f10, text="                           ") # label de text informatiu
l12.pack(side=RIGHT) # Apilem a la dreta

l13=Label(f10, text="dS") # label de text informatiu
l13.pack(side=RIGHT) # Apilem a la dreta

l14=Label(f10, text="Mes") # label de text informatiu
l14.pack(side=RIGHT) # Apilem a la dreta

l15=Label(f10, text="dM") # label de text informatiu
l15.pack(side=RIGHT) # Apilem a la dreta

l16=Label(f10, text="hh") # label de text informatiu
l16.pack(side=RIGHT) # Apilem a la dreta

l17=Label(f10, text="mm") # label de text informatiu
l17.pack(side=RIGHT) # Apilem a la dreta
#4
f8=Frame(mainw)		# frame per al botó de sortida
f8.pack(side=TOP, fill=X) # Apilem a la esquerra i permetem l'expansió X

def Sortir():
    mainw.quit()

b8=Button(f8, text="Sortir", command=Sortir)	# Si apretem aquest botó tanquem la finestra
b8.pack(side=LEFT) # Apilem a la esquerra
#}
mainw.mainloop()

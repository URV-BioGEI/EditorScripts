#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import os  # Importem el mòdul del sistema per a utilitzar comandes de la shell
import random
import subprocess
from subprocess import PIPE
from tkinter.constants import TRUE, END, LEFT, RIGHT, TOP, BOTH, X, W
from tkinter import Button, Frame, Label, Entry, Tk, IntVar, Checkbutton, filedialog, messagebox, scrolledtext as tkst

from MyDialog import MyDialog


def choose_working_directory():
    global directori
    directori = filedialog.askdirectory(
        parent=main_window,  # Fa que la nova finestra sigui pare de la finestra principal
        title="Escollir directori",  # Títol de la finestra
        mustexist=TRUE)  # El directori ha d'existir
    l1.configure(text=directori)  # Assignem el directori al label


def open_script():
    """
    Funció Obrir Script:
    S'encarrega d'obrir l'Script a partir del nom (Entry e1) i de la ruta escollida (Label l1)
    i mostrar el contingut en el ScrolledText.
    Cal implementar el cas que el fitxer no existeixi o no tingui l'extensió sh
    Cal implementar algun tipus de comunicació (variable global) perquè guardar Script sàpiga
    Si pot executar-se o no. (si hem obert algun script amb anterioritat).
    :return:
    """
    global file  # Fem la variable de fitxer global per a modificar-la
    file = filedialog.askopenfilename(initialdir=directori, title="Obrir fitxer",
                                      filetypes=[("Fitxers d'Scripts Bash", "*.sh")])
    if file:  # Si no escollim cap fitxer, llavors no entrem al if
        try:
            global file_name  # Accedim a la memoria global
            file_name = os.path.basename(file)  # Obtenim el nom del fitxer
            e1.delete(0, END)  # esborrem el contingut de entry
            e1.insert(0, file_name)  # I li assigned el nom del fitxer
            f = open(file, 'r')  # Obrir fitxer, en mode lectura
            content = f.read()  # Llegim tot el fitxer i l'emmagatzemem
            st.delete(1.0, END)  # Fem un clean del text
            st.insert(END, content)  # inserim el contingut del fitxer
            f.close()  # Tanquem el fitxer
        except Exception:
            messagebox.showerror(title="Error I/O",
                                 message="Error E/S")  # Si captem una excepció E/S, mostrem el missatge


def save_script():
    """
    Funció Guardar Script
    S'encarrega d'agafar el contingut del ScrolledText i passar-lo al fitxer que ja ha sigut obert
    Per a executar-se un fitxer ha hagut de ser obert prèviament.
    :return:
    """
    if file != 0:  # Si el flag no es troba actiu...
        try:
            f = open(file, 'w+')  # Obrim el fitxer en mode d'escriptura +, farà clean abans
            text = st.get(1.0, END)  # Obtenim el text del text box
            f.write(text)  # Guardem el text al fitxer
            f.close()  # Tanquem fitxer
        except Exception:
            messagebox.showerror(title="Error I/O",
                                 message="Error E/S")  # Si captem una excepció E/S, mostrem el missatge
    else:  # ...Mostrem missatge d'error
        # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
        messagebox.showerror(title="Error I/O",
                             message="Per a guardar cal carregar un fitxer abans")


def save_new_script():
    """
    Genera un nou script amb el nom indicat a l'Entry e1 en el directori que indica label l1. Cal fer dues excepcions si
    no hi ha valors o bé el string de nom de fitxer és incorrecte.
    :return:
    """
    try:
        f = filedialog.asksaveasfile(initialdir=directori, title="Guardar com", defaultextension='.sh')
        if f:
            text = st.get(1.0, END)
            f.write(text)
            f.close()
    except Exception:
        messagebox.showerror(title="Error I/O", message="Error E/S")  # Si captem una excepció E/S, mostrem el missatge


def see_stderr():
    """
    Crea una subfinestra per a visualitzar si existeix la sortida de la darrera execució de l’script.
    :return:
    """
    r = MyDialog(main_window, stderr_txt)
    main_window.wait_window(r.top)


def see_stdout():
    """
    Crea una subfinestra per a visualitzar si existeix la sortida de la darrera execució de l’script.
    :return:
    """
    d = MyDialog(main_window, stdout_txt)
    main_window.wait_window(d.top)


def run_now():
    """
    Executa l’script escollit amb els arguments i redireccions indicades de manera immediata.
    :return:
    """
    global st, stdout_txt, stderr_txt  # Accedim a variables globals
    location = "/tmp/tmp.sh"  # Assignem la ubicació del fitxer temporal script
    arguments = location + " " + e2.get()  # Obtenim els arguments (executar script i passar arguments)
    com = st.get(1.0, END)  # Obtenim el text del fitxer
    f = open(location, 'w+')  # Obrim el fitxer en mode d'escriptura +, farà un clean abans d'escriure
    f.write(com)  # Escrivim el script
    f.close()  # Tanquem el fitxer
    os.system("chmod +x /tmp/tmp.sh")  # Donem permisos d'execució
    rc = subprocess.Popen(  # Cridem al modul subprocess
        arguments,  # Li passem les comandes (execució + parameters)
        shell=True,  # Pel tipus de crida aquest ha de ser true
        stdout=PIPE,  # Per a poder obtenir stdout
        stderr=PIPE)  # Per a poder obtenir stderr
    stdout_txt, stderr_txt = rc.communicate()  # Obtenim les sortides

    # Checkboxes
    if std1.get():  # Si l'usuari ha marcat el checkbox del stdout...
        if file_name != "":  # Si s'ha obert un fitxer
            f = open(file_name + ".out", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stdout_txt.decode("utf-8"))  # Hi escrivim la sortida
            f.close()  # Tanquem
        else:  # i si no li donem un altre nom
            f = open("script.out", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stdout_txt.decode("utf-8"))  # Hi escrivim la sortida
            f.close()  # Tanquem
    if std2.get():  # Si l'usuari ha marcat el checkbox del stderr...
        if file_name != "":  # Si s'ha obert un fitxer
            f = open(file_name + ".err", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stderr_txt.decode("utf-8"))  # Hi escrivim la sortida
            f.close()  # Tanquem
        else:  # i si no li donem un altre nom
            f = open("script.err", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
            f.write(stderr_txt.decode("utf-8"))  # Hi escrivim la sortida
            f.close()  # Tanquem


def run_late():
    """
    Programa l’execució de l’script mitjançant la comanda «at» a una
    hora i minut determinats. Caldrà buscar informació sobre la comanda
    Obtenim el temps en el format HH:MM -> e4:e3
    :return:
    """
    global st, stdout_txt, stderr_txt  # Accedim a variables globals
    try:
        rnd = random.randrange(10000)
        segons = int(e4.get())
        if segons > 0:
            location = "/tmp/" + str(rnd) + "Late.sh"
            # Obtenim els arguments (executar script i passar arguments)
            arguments = "sleep " + str(segons) + " && " + location + " " + e2.get()
            com = st.get(1.0, END)  # Obtenim el text del fitxer
            f = open(location, 'w+')  # Obrim el fitxer en mode d'escriptura +, farà un clean abans d'escriure
            f.write(com)  # Escrivim el script
            f.close()  # Tanquem el fitxer
            os.system("chmod +x " + location)  # Donem permisos d'execució
            subprocess.Popen(arguments, shell=True, stdout=PIPE, stderr=PIPE)
        else:
            # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
            messagebox.showerror(title="Error de temps",
                                 message="Trieu un número vàlid de segons i major que 0.")
    except Exception:
        # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
        messagebox.showerror(title="Error de temps",
                             message="Trieu un número vàlid de segons i major que 0.")


def run_at():
    """
    Corre l'script en un moment determinat amb el format de la comanda at.
    :return:
    """
    try:
        err = None
        rnd = random.randrange(10000)
        commands = e7.get()
        if not commands:
            # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
            messagebox.showerror(title="Error en les comandes.",
                                 message="Introduïu una comanda AT Vàlida. Tingueu en compte que l'String \"At \" "
                                         "ja s'afegeix automàticament.")
        else:
            if directori == "":
                location = os.path.dirname(os.path.abspath(
                    inspect.getfile(inspect.currentframe()))) + "/"  # Assignem la ubicació del fitxer temporal script
            else:
                location = directori + "/"
            fitxer = location + str(rnd) + "At.sh"
            # Obtenim els arguments (executar script i passar arguments)
            arguments = "at " + commands + " -f " + "\"" + fitxer + "\"" + e2.get() + ""
            com = st.get(1.0, END)  # Obtenim el text del fitxer
            f = open(fitxer, 'w+')  # Obrim el fitxer en mode d'escriptura +, farà un clean abans d'escriure
            f.write(com)  # Escrivim el script
            f.close()  # Tanquem el fitxer
            os.system("chmod +x \"" + fitxer + "\"")  # Donem permisos d'execució
            rc = subprocess.Popen(arguments, shell=True, stdout=PIPE, stderr=PIPE)
            out, err = rc.communicate()
        if err:
            messagebox.showerror(title="Error", message=err.decode("utf-8"))
    except Exception:
        # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
        messagebox.showerror(title="Error en els segons.",
                             message="Trieu un número vàlid de segons i major que 0.")


def run_with_period():
    """
    En la programació de l’execució de l’script de manera periòdica. Permetre
    tota la potència de descripcions del temps de la comanda «crontab». Caldrà modificar
    els camps que indiquen el temps per a tenir com a mínim cinc camps strings per a
    indicar el temps en què s’ha d’executar l’script. (format * * * * *).
    :return:
    """

    global st, file
    rnd = random.randrange(10000)
    com = st.get(1.0, END)  # Obtenim el text del fitxer
    if directori == "":
        location = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))) + "/"  # Assignem la ubicació del fitxer temporal script
    else:
        location = directori
    fitxer = location + str(rnd) + "Period.sh"
    # Obtenir informació
    correcte = 1  # Flag per entrar a la funció (comprova que tot estigui bé)
    ds = e5.get()  # Obtenim el camp dS
    if not ds:
        correcte = 0  # Si està buit, posem un 0 per a indicar que està malament
    mes = e6.get()  # Així successivament
    if not mes:
        correcte = 0
    dm = e8.get()
    if not dm:
        correcte = 0
    hh = e9.get()
    if not hh:
        correcte = 0
    mm = e10.get()
    if not mm:
        correcte = 0
    if correcte == 1:  # Mirem que tots siguin correctes
        f = open(fitxer, 'w+')  # Obrim el fitxer en mode d'escriptura +, farà un clean abans d'escriure
        fitxer_c = "\"" + fitxer + "\""
        fitxer_q = "\"" + fitxer + "\""
        f.write(com)  # Escrivim el script (?) falta el nombre aleatori
        f.close()  # Tanquem el fitxer
        os.system("chmod +x " + fitxer_q)  # Donem permisos d'execució
        s_file = open(location + "/crontask", 'w+')
        s_file.write(mm + " " + hh + " " + dm + " " + mes + " " + ds + " " + fitxer_c + "\n")
        s_file.close()
        cron = subprocess.Popen("crontab " + location + "/crontask", shell=True, stdout=PIPE,
                                stderr=PIPE)  # Obtenim nom d'usuari
        out, err = cron.communicate()
        if err:
            messagebox.showerror(title="Error",
                                 message="Format incorrecte de crontab: m correspon al minut en què es va a "
                                         "executar el script, el valor va de 0 a 59h l'hora exacta, es maneja el "
                                         "format de 24 hores, els valors van de 0 a 23, sent 0 les 12:00 de la "
                                         "mitjanit.diu fa referència al dia del mes, per exemple es pot especificar "
                                         "15 si es vol executar cada dia 15 dow significa el dia de la setmana, "
                                         "pot ser numèric (0 a 7, on 0 i 7 són diumenge) o les 3 primeres lletres "
                                         "del dia en anglès: mon, tue, wed, thu, fri, sat, sun.")
    else:
        # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
        messagebox.showerror(title="Falten dades", message="Emplena tots els camps de l'esquerra")


def close_window():
    main_window.quit()


# MAIN
# Paràmetres de finestra principal
main_window = Tk()
main_window.title("Execució d'Scripts en el temps")

# Var
file = 0  # 0 si no s'ha carregat cap fitxer, ruta al fitxer incloent el nom si ja s'ha carregat
directori = ""  # 0 si no s'ha carregat, directori de treball actual si s'ha carregat
file_name = ""  # 0 si no s'ha obert cap fitxer, nom del fitxer obert si s'ha carregat fitxer
stdout_txt = ""  # String amb stdout
stderr_txt = ""  # String amb stderr

# Elements main window
# {
f1 = Frame(main_window, bg="grey")  # Creem primer frame, li donem el color gris
f1.pack(fill=X, side=TOP)  # alineem a la part de dalt i li permetem expandir-se en X

b1 = Button(f1, text='Escollir directori de treball',
            command=choose_working_directory)  # Creem el botó i li assignem la comanda de preguntar el directori
b1.pack(side=LEFT)  # l'apilem a l'esquerra

l1 = Label(f1, text="")  # "label" que mostra el directori actual
l1.pack(expand=TRUE, fill=X, side=RIGHT,
        anchor=W)  # Li permeten expandir-se al llarg de la finestra en X, l'apilem a la dreta
# }
f2 = Frame(main_window)  # Creem primer frame,
f2.pack(side=TOP, fill=X)  # alineem a la part de dalt i li permetem expandir-se
# {


b2 = Button(f2, text="Obrir Script", command=open_script)  # botó per a obrir script
b2.pack(side=LEFT)  # l'apilem a l'esquerra

e1 = Entry(f2, width=20)  # entrada de text per a posar el nom del fitxer
e1.pack(expand=TRUE, fill=X, side=LEFT)  # li permetem expandir-se en X i l'apilem a l'esquerra

b3 = Button(f2, text="Guardar l'Script", command=save_script)  # Botó per a dur a terme la funció de guardat
b3.pack(side=RIGHT)  # L'apilem a la dreta

# Botó per a generar la funció de dalt
b4 = Button(main_window, text="Guardar en un nou script", command=save_new_script)
b4.pack(side=TOP, anchor=W)  # l'apilem a la part de dalt del frame on ens trobem
# }
# {
# És una de les components principal del programa.
# Està fet de tres objectes, un TextBox, un ScrollBar i un frame que els conté
# D'aquesta manera és com si fos un contenidor ja implementat amb els seus propis mètodes
st = tkst.ScrolledText(
    master=main_window,  # incloem a la finestra principal aquest objecte
    wrap='word',  # Fem que el text sigui de paraules (?)
    width=25,  # caràcters per fila
    height=17,  # lines de text
    bg='beige'  # color de fons
)

st.pack(expand=TRUE, fill=BOTH, side=TOP, padx=8,
        pady=8)  # Apilem i permetem l'expansió. Els altres valors són la mida del text (?)
# }
# {
f3 = Frame(main_window)  # tercer frame
f3.pack(side=TOP, fill=X)  # procedim igual que els anteriors

l2 = Label(f3, text="Arguments d'entrada :")  # creem el label que indica els arguments d'entrada.
l2.pack(side=LEFT)  # apilem a l'esquerra

e2 = Entry(f3)  # entrada de text per als arguments
e2.pack(expand=TRUE, fill=X, side=LEFT)  # l'apilem i li permeten fer-se gran

# Permet reencaminar la sortida de l'execució de l’script a un fitxer.
# El nom d’aquest fitxer serà en nom de l’script amb extensió «.out»
# Sera consultat per tots els botons run
std1 = IntVar()
cb1 = Checkbutton(f3, text="Genera Stdout", variable=std1)  # checkbox per a saber si cal generar stdout en un fitxer
cb1.pack(side=LEFT)

# Permet reencaminar la sortida d’error de l'execució de l’script a un
# fitxer. El nom d’aquest fitxer serà en nom de l’script amb extensió err.
# Sera consultat per tots els botons run
std2 = IntVar()
cb2 = Checkbutton(f3, text="Genera Stderr", variable=std2)  # checkbox per a saber si cal generar stderr en un fitxer
cb2.pack(side=LEFT)
# }
# {
f4 = Frame(main_window)  # afegim un nou frame
f4.pack(side=TOP, fill=X)  # l'apilem cap a dalt i emplenem en X

b5 = Button(f4, text="Veure Stderr", command=see_stderr)  # Botó que executa la funció de dalt
b5.pack(side=RIGHT)  # Ho apilem a la part dreta

b6 = Button(f4, text="Veure Stdout", command=see_stdout)  # Botó que executa la funció de dalt.
b6.pack(side=RIGHT)  # Apilem a la dreta
# }
# {
f5 = Frame(main_window)  # Afegim un nou frame
f5.pack(side=TOP, fill=X)  # apilem a dalt i permetem l'expansió

b5 = Button(f5, text="Run", command=run_now)  # Executa la funció de dalt
b5.pack(side=RIGHT)  # apilem a la dreta

l3 = Label(f5, text="Executa immediatament")  # label de descripció del botó b5
l3.pack(side=RIGHT)
# }
# {
# Afegim un nou frame. Aquest frame implementa tot el relacionat amb executar a n determinat temps
f6 = Frame(main_window)
f6.pack(side=TOP, fill=X)  # apilem a dalt i permetem l'expansió X

b6 = Button(f6, text="RunLate", command=run_late)  # Executa la funció de dalt
b6.pack(side=RIGHT)  # Apilem a la dreta

l4 = Label(f6, text="  segons. ")  # label de text
l4.pack(side=RIGHT)  # Apilem a la dreta

e4 = Entry(f6, width=3)  # entrada de text per a les hores de la funció run late
e4.pack(side=RIGHT)  # Apilem a la dreta

l6 = Label(f6, text="Executa d'aquí a: ")  # label
l6.pack(side=RIGHT)  # Apilem a la dreta
# }
# {
f9 = Frame(main_window)  # Frame de la part opcional d'executar amb format at, per això no segueix la numeració
f9.pack(side=TOP, fill=X)

b9 = Button(f9, text="RunAt", command=run_at)  # Botó per a executar la funció anterior
b9.pack(side=RIGHT)  # Apilem a la dreta

l10 = Label(f9, text="  de 'at'   ")  # label
l10.pack(side=RIGHT)  # Apilem a la dreta

e7 = Entry(f9, width=7)  # entrada de text que correspon a les hores
e7.pack(side=RIGHT)  # Apilem a la dreta

l11 = Label(f9, text="Executa un cop amb format ")  # label
l11.pack(side=RIGHT)  # Apilem a la dreta
# }
# {
f7 = Frame(main_window)  # Afegim un frame. Aquest contindrà els botons per a executar l'script periòdicament
f7.pack(side=TOP, fill=X)  # ho posem a la paret nort i expandim en x

b7 = Button(f7, text="RunPeriod", command=run_with_period)  # Botó per a executar la funció anterior
b7.pack(side=RIGHT)  # Apilem a la dreta

l7 = Label(f7, text=" crontab  ")  # label de text informatiu
l7.pack(side=RIGHT)  # Apilem a la dreta

e5 = Entry(f7, width=2)  # entrada de text dS
e5.pack(side=RIGHT)  # Apilem a la dreta

e6 = Entry(f7, width=2)  # entrada de text Mes
e6.pack(side=RIGHT)  # Apilem a la dreta

e8 = Entry(f7, width=2)  # entrada de text dM
e8.pack(side=RIGHT)  # Apilem a la dreta

e9 = Entry(f7, width=2)  # entrada de text hh
e9.pack(side=RIGHT)  # Apilem a la dreta

e10 = Entry(f7, width=2)  # entrada de text mm
e10.pack(side=RIGHT)  # Apilem a la dreta

l9 = Label(f7, text="Programa cada dia amb format")  # label de text informatiu
l9.pack(side=RIGHT)  # Apilem a la dreta
# }
# {
f10 = Frame(main_window)  # frame per als labels del camp de crontab
f10.pack(side=TOP, fill=X)  # Apilem a l'esquerra i permetem l'expansió X

l12 = Label(f10, text="                           ")  # label de text informatiu
l12.pack(side=RIGHT)  # Apilem a la dreta

l13 = Label(f10, text="dS")  # label de text informatiu
l13.pack(side=RIGHT)  # Apilem a la dreta

l14 = Label(f10, text="Mes")  # label de text informatiu
l14.pack(side=RIGHT)  # Apilem a la dreta

l15 = Label(f10, text="dM")  # label de text informatiu
l15.pack(side=RIGHT)  # Apilem a la dreta

l16 = Label(f10, text="hh")  # label de text informatiu
l16.pack(side=RIGHT)  # Apilem a la dreta

l17 = Label(f10, text="mm")  # label de text informatiu
l17.pack(side=RIGHT)  # Apilem a la dreta
# 4
f8 = Frame(main_window)  # frame per al botó de sortida
f8.pack(side=TOP, fill=X)  # Apilem a l'esquerra i permetem l'expansió X

b8 = Button(f8, text="Sortir", command=close_window)  # Si premem aquest botó tanquem la finestra
b8.pack(side=LEFT)  # Apilem a l'esquerra
# }
main_window.mainloop()

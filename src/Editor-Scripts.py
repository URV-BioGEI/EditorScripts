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


class EditorScripts:

    def __init__(self):
        # MAIN
        # Paràmetres de finestra principal
        self.main_window = Tk()
        self.main_window.title("Execució d'Scripts en el temps")

        # Var
        self.file = ""  # 0 si no s'ha carregat cap fitxer, ruta al fitxer incloent el nom si ja s'ha carregat
        self.directori = ""  # 0 si no s'ha carregat, directori de treball actual si s'ha carregat
        self.file_name = ""  # 0 si no s'ha obert cap fitxer, nom del fitxer obert si s'ha carregat fitxer
        self.stdout_txt = ""  # String amb stdout
        self.stderr_txt = ""  # String amb stderr

        # Elements main window
        # {
        self.f1 = Frame(self.main_window, bg="grey")  # Creem primer frame, li donem el color gris
        self.f1.pack(fill=X, side=TOP)  # alineem a la part de dalt i li permetem expandir-se en X

        # Creem el botó i li assignem la comanda de preguntar el directori
        self.b1 = Button(self.f1, text='Escollir directori de treball', command=self.choose_working_directory)
        self.b1.pack(side=LEFT)  # l'apilem a l'esquerra

        self.l1 = Label(self.f1, text="")  # "label" que mostra el directori actual
        self.l1.pack(expand=TRUE, fill=X, side=RIGHT,
                     anchor=W)  # Li permeten expandir-se al llarg de la finestra en X, l'apilem a la dreta
        # }
        self.f2 = Frame(self.main_window)  # Creem primer frame,
        self.f2.pack(side=TOP, fill=X)  # alineem a la part de dalt i li permetem expandir-se
        # {

        self.b2 = Button(self.f2, text="Obrir Script", command=self.open_script)  # botó per a obrir script
        self.b2.pack(side=LEFT)  # l'apilem a l'esquerra

        self.e1 = Entry(self.f2, width=20)  # entrada de text per a posar el nom del fitxer
        self.e1.pack(expand=TRUE, fill=X, side=LEFT)  # li permetem expandir-se en X i l'apilem a l'esquerra

        # Botó per a dur a terme la funció de guardat
        self.b3 = Button(self.f2, text="Guardar l'Script", command=self.save_script)
        self.b3.pack(side=RIGHT)  # L'apilem a la dreta

        # Botó per a generar la funció de dalt
        self.b4 = Button(self.main_window, text="Guardar en un nou script", command=self.save_new_script)
        self.b4.pack(side=TOP, anchor=W)  # l'apilem a la part de dalt del frame on ens trobem
        # }
        # {
        # És una de les components principal del programa.
        # Està fet de tres objectes, un TextBox, un ScrollBar i un frame que els conté
        # D'aquesta manera és com si fos un contenidor ja implementat amb els seus propis mètodes
        self.st = tkst.ScrolledText(
            master=self.main_window,  # incloem a la finestra principal aquest objecte
            wrap='word',  # Fem que el text sigui de paraules (?)
            width=25,  # caràcters per fila
            height=17,  # lines de text
            bg='beige'  # color de fons
        )

        # Apilem i permetem l'expansió. Els altres valors són la mida del text (?)
        self.st.pack(expand=TRUE, fill=BOTH, side=TOP, padx=8, pady=8)
        # }
        # {
        self.f3 = Frame(self.main_window)  # tercer frame
        self.f3.pack(side=TOP, fill=X)  # procedim igual que els anteriors

        self.l2 = Label(self.f3, text="Arguments d'entrada :")  # creem el label que indica els arguments d'entrada.
        self.l2.pack(side=LEFT)  # apilem a l'esquerra

        self.e2 = Entry(self.f3)  # entrada de text per als arguments
        self.e2.pack(expand=TRUE, fill=X, side=LEFT)  # l'apilem i li permeten fer-se gran

        # Permet reencaminar la sortida de l'execució de l’script a un fitxer.
        # El nom d’aquest fitxer serà en nom de l’script amb extensió «.out»
        # Sera consultat per tots els botons run
        self.std1 = IntVar()
        # checkbox per a saber si cal generar stdout en un fitxer
        self.cb1 = Checkbutton(self.f3, text="Genera Stdout", variable=self.std1)
        self.cb1.pack(side=LEFT)

        # Permet reencaminar la sortida d’error de l'execució de l’script a un
        # fitxer. El nom d’aquest fitxer serà en nom de l’script amb extensió err.
        # Sera consultat per tots els botons run
        self.std2 = IntVar()
        self.cb2 = Checkbutton(self.f3, text="Genera Stderr",
                               variable=self.std2)  # checkbox per a saber si cal generar stderr en un fitxer
        self.cb2.pack(side=LEFT)
        # }
        # {
        self.f4 = Frame(self.main_window)  # afegim un nou frame
        self.f4.pack(side=TOP, fill=X)  # l'apilem cap a dalt i emplenem en X

        self.b5 = Button(self.f4, text="Veure Stderr", command=self.see_stderr)  # Botó que executa la funció de dalt
        self.b5.pack(side=RIGHT)  # Ho apilem a la part dreta

        self.b6 = Button(self.f4, text="Veure Stdout", command=self.see_stdout)  # Botó que executa la funció de dalt.
        self.b6.pack(side=RIGHT)  # Apilem a la dreta
        # }
        # {
        self.f5 = Frame(self.main_window)  # Afegim un nou frame
        self.f5.pack(side=TOP, fill=X)  # apilem a dalt i permetem l'expansió

        self.b5 = Button(self.f5, text="Run", command=self.run_now)  # Executa la funció de dalt
        self.b5.pack(side=RIGHT)  # apilem a la dreta

        self.l3 = Label(self.f5, text="Executa immediatament")  # label de descripció del botó b5
        self.l3.pack(side=RIGHT)
        # }
        # {
        # Afegim un nou frame. Aquest frame implementa tot el relacionat amb executar a n determinat temps
        self.f6 = Frame(self.main_window)
        self.f6.pack(side=TOP, fill=X)  # apilem a dalt i permetem l'expansió X

        self.b6 = Button(self.f6, text="RunLate", command=self.run_late)  # Executa la funció de dalt
        self.b6.pack(side=RIGHT)  # Apilem a la dreta

        self.l4 = Label(self.f6, text="  segons. ")  # label de text
        self.l4.pack(side=RIGHT)  # Apilem a la dreta

        self.e4 = Entry(self.f6, width=3)  # entrada de text per a les hores de la funció run late
        self.e4.pack(side=RIGHT)  # Apilem a la dreta

        self.l6 = Label(self.f6, text="Executa d'aquí a: ")  # label
        self.l6.pack(side=RIGHT)  # Apilem a la dreta
        # }
        # {
        self.f9 = Frame(
            self.main_window)  # Frame de la part opcional d'executar amb format at, per això no segueix la numeració
        self.f9.pack(side=TOP, fill=X)

        self.b9 = Button(self.f9, text="RunAt", command=self.run_at)  # Botó per a executar la funció anterior
        self.b9.pack(side=RIGHT)  # Apilem a la dreta

        self.l10 = Label(self.f9, text="  de 'at'   ")  # label
        self.l10.pack(side=RIGHT)  # Apilem a la dreta

        self.e7 = Entry(self.f9, width=7)  # entrada de text que correspon a les hores
        self.e7.pack(side=RIGHT)  # Apilem a la dreta

        self.l11 = Label(self.f9, text="Executa un cop amb format ")  # label
        self.l11.pack(side=RIGHT)  # Apilem a la dreta
        # }
        # {
        self.f7 = Frame(
            self.main_window)  # Afegim un frame. Aquest contindrà els botons per a executar l'script periòdicament
        self.f7.pack(side=TOP, fill=X)  # ho posem a la paret nort i expandim en x

        # Botó per a executar la funció anterior
        self.b7 = Button(self.f7, text="RunPeriod", command=self.run_with_period)
        self.b7.pack(side=RIGHT)  # Apilem a la dreta

        self.l7 = Label(self.f7, text=" crontab  ")  # label de text informatiu
        self.l7.pack(side=RIGHT)  # Apilem a la dreta

        self.e5 = Entry(self.f7, width=2)  # entrada de text dS
        self.e5.pack(side=RIGHT)  # Apilem a la dreta

        self.e6 = Entry(self.f7, width=2)  # entrada de text Mes
        self.e6.pack(side=RIGHT)  # Apilem a la dreta

        self.e8 = Entry(self.f7, width=2)  # entrada de text dM
        self.e8.pack(side=RIGHT)  # Apilem a la dreta

        self.e9 = Entry(self.f7, width=2)  # entrada de text hh
        self.e9.pack(side=RIGHT)  # Apilem a la dreta

        self.e10 = Entry(self.f7, width=2)  # entrada de text mm
        self.e10.pack(side=RIGHT)  # Apilem a la dreta

        self.l9 = Label(self.f7, text="Programa cada dia amb format")  # label de text informatiu
        self.l9.pack(side=RIGHT)  # Apilem a la dreta
        # }
        # {
        self.f10 = Frame(self.main_window)  # frame per als labels del camp de crontab
        self.f10.pack(side=TOP, fill=X)  # Apilem a l'esquerra i permetem l'expansió X

        self.l12 = Label(self.f10, text="                           ")  # label de text informatiu
        self.l12.pack(side=RIGHT)  # Apilem a la dreta

        self.l13 = Label(self.f10, text="dS")  # label de text informatiu
        self.l13.pack(side=RIGHT)  # Apilem a la dreta

        self.l14 = Label(self.f10, text="Mes")  # label de text informatiu
        self.l14.pack(side=RIGHT)  # Apilem a la dreta

        self.l15 = Label(self.f10, text="dM")  # label de text informatiu
        self.l15.pack(side=RIGHT)  # Apilem a la dreta

        self.l16 = Label(self.f10, text="hh")  # label de text informatiu
        self.l16.pack(side=RIGHT)  # Apilem a la dreta

        self.l17 = Label(self.f10, text="mm")  # label de text informatiu
        self.l17.pack(side=RIGHT)  # Apilem a la dreta
        # 4
        self.f8 = Frame(self.main_window)  # frame per al botó de sortida
        self.f8.pack(side=TOP, fill=X)  # Apilem a l'esquerra i permetem l'expansió X

        self.b8 = Button(self.f8, text="Sortir", command=self.close_window)  # Si premem aquest botó tanquem la finestra
        self.b8.pack(side=LEFT)  # Apilem a l'esquerra
        # }
        
        self.main_window.mainloop()

    def choose_working_directory(self):
        self.directori = filedialog.askdirectory(
            parent=self.main_window,  # Fa que la nova finestra sigui pare de la finestra principal
            title="Escollir directori",  # Títol de la finestra
            mustexist=TRUE)  # El directori ha d'existir
        self.l1.configure(text=self.directori)  # Assignem el directori al label

    def open_script(self):
        """
        Funció Obrir Script:
        S'encarrega d'obrir l'Script a partir del nom (Entry e1) i de la ruta escollida (Label l1)
        i mostrar el contingut en el ScrolledText.
        Cal implementar el cas que el fitxer no existeixi o no tingui l'extensió sh
        Cal implementar algun tipus de comunicació (variable global) perquè guardar Script sàpiga
        Si pot executar-se o no. (si hem obert algun script amb anterioritat).
        :return:
        """
        self.file = filedialog.askopenfilename(initialdir=self.directori, title="Obrir fitxer",
                                               filetypes=[("Fitxers d'Scripts Bash", "*.sh")])
        if self.file:  # Si no escollim cap fitxer, llavors no entrem al if
            try:
                self.file_name = os.path.basename(self.file)  # Obtenim el nom del fitxer
                self.e1.delete(0, END)  # esborrem el contingut de entry
                self.e1.insert(0, self.file_name)  # I li assigned el nom del fitxer
                f = open(self.file, 'r')  # Obrir fitxer, en mode lectura
                content = f.read()  # Llegim tot el fitxer i l'emmagatzemem
                self.st.delete(1.0, END)  # Fem un clean del text
                self.st.insert(END, content)  # inserim el contingut del fitxer
                f.close()  # Tanquem el fitxer
            except Exception:
                messagebox.showerror(title="Error I/O",
                                     message="Error E/S")  # Si captem una excepció E/S, mostrem el missatge

    def save_script(self):
        """
        Funció Guardar Script
        S'encarrega d'agafar el contingut del ScrolledText i passar-lo al fitxer que ja ha sigut obert
        Per a executar-se un fitxer ha hagut de ser obert prèviament.
        :return:
        """
        if self.file != "":  # Si el flag no es troba actiu...
            try:
                f = open(self.file, 'w+')  # Obrim el fitxer en mode d'escriptura +, farà clean abans
                text = self.st.get(1.0, END)  # Obtenim el text del text box
                f.write(text)  # Guardem el text al fitxer
                f.close()  # Tanquem fitxer
            except Exception:
                messagebox.showerror(title="Error I/O",
                                     message="Error E/S")  # Si captem una excepció E/S, mostrem el missatge
        else:  # ...Mostrem missatge d'error
            # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
            messagebox.showerror(title="Error I/O",
                                 message="Per a guardar cal carregar un fitxer abans")

    def save_new_script(self):
        """
        Genera un nou script amb el nom indicat a l'Entry e1 en el directori que indica label l1. Cal fer dues
        excepcions si no hi ha valors o bé el string de nom de fitxer és incorrecte.
        :return:
        """
        try:
            f = filedialog.asksaveasfile(initialdir=self.directori, title="Guardar com", defaultextension='.sh')
            if f:
                text = self.st.get(1.0, END)
                f.write(text)
                f.close()
        except Exception:
            # Si captem una excepció E/S, mostrem el missatge
            messagebox.showerror(title="Error I/O", message="Error E/S")

    def see_stderr(self):
        """
        Crea una subfinestra per a visualitzar si existeix la sortida de la darrera execució de l’script.
        :return:
        """
        r = MyDialog(self.main_window, self.stderr_txt)
        self.main_window.wait_window(r.top)

    def see_stdout(self):
        """
        Crea una subfinestra per a visualitzar si existeix la sortida de la darrera execució de l’script.
        :return:
        """
        d = MyDialog(self.main_window, self.stdout_txt)
        self.main_window.wait_window(d.top)

    def run_now(self):
        """
        Executa l’script escollit amb els arguments i redireccions indicades de manera immediata.
        :return:
        """
        location = "/tmp/tmp.sh"  # Assignem la ubicació del fitxer temporal script
        arguments = location + " " + self.e2.get()  # Obtenim els arguments (executar script i passar arguments)
        com = self.st.get(1.0, END)  # Obtenim el text del fitxer
        f = open(location, 'w+')  # Obrim el fitxer en mode d'escriptura +, farà un clean abans d'escriure
        f.write(com)  # Escrivim el script
        f.close()  # Tanquem el fitxer
        os.system("chmod +x /tmp/tmp.sh")  # Donem permisos d'execució
        rc = subprocess.Popen(  # Cridem al modul subprocess
            arguments,  # Li passem les comandes (execució + parameters)
            shell=True,  # Pel tipus de crida aquest ha de ser true
            stdout=PIPE,  # Per a poder obtenir stdout
            stderr=PIPE)  # Per a poder obtenir stderr
        self.stdout_txt, self.stderr_txt = rc.communicate()  # Obtenim les sortides

        # Checkboxes
        if self.std1.get():  # Si l'usuari ha marcat el checkbox del stdout...
            if self.file_name != "":  # Si s'ha obert un fitxer
                f = open(self.file_name + ".out", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
                f.write(self.stdout_txt.decode("utf-8"))  # Hi escrivim la sortida
                f.close()  # Tanquem
            else:  # i si no li donem un altre nom
                f = open("script.out", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
                f.write(self.stdout_txt.decode("utf-8"))  # Hi escrivim la sortida
                f.close()  # Tanquem
        if self.std2.get():  # Si l'usuari ha marcat el checkbox del stderr...
            if self.file_name != "":  # Si s'ha obert un fitxer
                f = open(self.file_name + ".err", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
                f.write(self.stderr_txt.decode("utf-8"))  # Hi escrivim la sortida
                f.close()  # Tanquem
            else:  # i si no li donem un altre nom
                f = open("script.err", 'w+')  # Obrim el fitxer en mode w+, per a fer el clean.
                f.write(self.stderr_txt.decode("utf-8"))  # Hi escrivim la sortida
                f.close()  # Tanquem

    def run_late(self):
        """
        Programa l’execució de l’script mitjançant la comanda «at» a una
        hora i minut determinats. Caldrà buscar informació sobre la comanda
        Obtenim el temps en el format HH:MM -> e4:e3
        :return:
        """
        try:
            segons = int(self.e4.get())
            if segons > 0:
                location = "/tmp/" + str(random.randrange(10000)) + "Late.sh"
                # Obtenim els arguments (executar script i passar arguments)
                arguments = "sleep " + str(segons) + " && " + location + " " + self.e2.get()
                com = self.st.get(1.0, END)  # Obtenim el text del fitxer
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

    def run_at(self):
        """
        Corre l'script en un moment determinat amb el format de la comanda at.
        :return:
        """
        try:
            err = None
            commands = self.e7.get()
            if not commands:
                # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
                messagebox.showerror(title="Error en les comandes.",
                                     message="Introduïu una comanda AT Vàlida. Tingueu en compte que l'String \"At \" "
                                             "ja s'afegeix automàticament.")
            else:
                if self.directori == "":
                    location = os.path.dirname(os.path.abspath(
                        inspect.getfile(
                            inspect.currentframe()))) + "/"  # Assignem la ubicació del fitxer temporal script
                else:
                    location = self.directori + "/"
                fitxer = location + str(random.randrange(10000)) + "At.sh"
                # Obtenim els arguments (executar script i passar arguments)
                arguments = "at " + commands + " -f " + "\"" + fitxer + "\"" + self.e2.get() + ""
                com = self.st.get(1.0, END)  # Obtenim el text del fitxer
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

    def run_with_period(self):
        """
        En la programació de l’execució de l’script de manera periòdica. Permetre
        tota la potència de descripcions del temps de la comanda «crontab». Caldrà modificar
        els camps que indiquen el temps per a tenir com a mínim cinc camps strings per a
        indicar el temps en què s’ha d’executar l’script. (format * * * * *).
        :return:
        """
        com = self.st.get(1.0, END)  # Obtenim el text del fitxer
        if self.directori == "":
            location = os.path.dirname(os.path.abspath(
                inspect.getfile(inspect.currentframe()))) + "/"  # Assignem la ubicació del fitxer temporal script
        else:
            location = self.directori
        fitxer = location + str(random.randrange(10000)) + "Period.sh"
        # Obtenir informació
        correcte = 1  # Flag per entrar a la funció (comprova que tot estigui bé)
        ds = self.e5.get()  # Obtenim el camp dS
        if not ds:
            correcte = 0  # Si està buit, posem un 0 per a indicar que està malament
        mes = self.e6.get()  # Així successivament
        if not mes:
            correcte = 0
        dm = self.e8.get()
        if not dm:
            correcte = 0
        hh = self.e9.get()
        if not hh:
            correcte = 0
        mm = self.e10.get()
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
                                             "mitjanit.diu fa referència al dia del mes, per exemple es pot "
                                             "especificar "
                                             "15 si es vol executar cada dia 15 dow significa el dia de la setmana, "
                                             "pot ser numèric (0 a 7, on 0 i 7 són diumenge) o les 3 primeres lletres "
                                             "del dia en anglès: mon, tue, wed, thu, fri, sat, sun.")
        else:
            # Si captem una excepció (que el fitxer no existeixi) mostrem el missatge
            messagebox.showerror(title="Falten dades", message="Emplena tots els camps de l'esquerra")

    def close_window(self):
        self.main_window.quit()


EditorScripts()

from argparse import FileType
from cProfile import label
from cgitb import text
from codecs import BufferedIncrementalDecoder
from curses import window
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo
from turtle import title, update, width
from tkinter import filedialog
from setuptools import Command

class SDP:
    
    def __init__(self):
        
        # criacao da janela de simulacao de dispersao de poluente #
        self.window = Tk()
        self.window.title("Simulacao de Dispersao de Poluente")
        self.window.minsize(width=600, height=600)
        self.window.resizable(0,0)
        self.main_menu = tkinter.Menu(self.window)
        
        # criacao das opcoes na barra de menu #
        self.arquivo_menu = tkinter.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Menu", menu=self.arquivo_menu)
        self.arquivo_menu.add_command(label="Carregar", command=self.carregar)
        self.arquivo_menu.add_command(label="Salvar", command=self.salvar)
        self.arquivo_menu.add_command(label="Sair", command=self.window.quit)
        
        # criacao das opcoes na barra de simulacao #
        self.simulacao_menu = tkinter.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Simulacao", menu=self.simulacao_menu)
        self.simulacao_menu.add_command(label="Iniciar Simulacao", command=self.simulacao_completa)
        self.simulacao_menu.add_command(label="Finalizar Simulacao", command=self.simulacao_incompleta)
        self.window.config(menu=self.main_menu)
        
        # Design do Aplicativo #
        self.bar_menu = Frame(self.window)
        self.bar_menu.pack(pady=10, padx=20)
        
        self.bar_menu2 = Frame(self.window)
        self.bar_menu2.pack(pady=10)
        
        self.bar_menu3 = Frame(self.window)
        self.bar_menu3.pack(padx=10, pady=10)
        
        # Design bar menu #
        self.text1 = Label(self.bar_menu, text="Malha da Ilha:", font="arial 13 bold", fg="white")
        self.text1.pack(side="left")
        self.text1 = tkinter.Entry(self.bar_menu, font="arial 13 bold", width=15)
        self.text1.pack(side="left",padx=1, pady=1)
        
        self.text2 = Label(self.bar_menu, text="  Intesidade da Fonte:", font="arial 13 bold",  fg="white")
        self.text2.pack(side="left")
        intesidade_fonte= tkinter.Label(self.bar_menu, text="  Intensidade da fonte: ")
        self.fonte_size = tkinter.Spinbox(self.bar_menu, from_=1, to=100, width=4)
        self.fonte_size.pack(side="left")
        
        self.text3 = Label(self.bar_menu, text="  Coordenadas da fonte (x,y):", font="arial 13 bold", fg="white")
        self.text3.pack(side="left")
        self.text3 = tkinter.Entry(self.bar_menu, font="arial 13 bold", width=5)
        self.text3.pack(side="left")
        
        # Design bar menu 2 #
        self.text4 = Label(self.bar_menu2, text="  Gravar Resultado por:", font="arial 13 bold", fg="white")
        self.text4.pack(side="left")
        save_result = tkinter.Label(self.bar_menu2, text="  Gravar Resultado por:")
        self.size = tkinter.Spinbox(self.bar_menu2, values=("dia", "semana", "mes"), width=7)
        self.size.pack(side="left")
        
        self.text5 = Label(self.bar_menu2, text="  Limite maximo de iteracoes:", font="arial 13 bold", fg="white")
        self.text5.pack(side="left")
        max_interaction = tkinter.Label(self.bar_menu2, text="  Limite maximo de iteracoes:")
        self.max_size = tkinter.Spinbox(self.bar_menu2, from_=1, to=100, width=4)
        self.max_size.pack(side="left")
        
        # Design bar menu 3 #
        self.area = Label(self.bar_menu3, text="Mapa de Dispersao", font="arial 13 bold", fg="white")
        self.area.pack()
        self.area = Canvas(self.bar_menu3,bg= "white", width=360,height=360)
        self.area.pack()
        
        # Botoes de Simulacao #
        self.iniciar = Button(self.window, text="  Iniciar Simulacao  ", font="arial 13 bold", fg="black", width=17, command=self.simulacao_completa)
        self.iniciar.pack()
        
        self.finalizar = Button(self.window, text="  Finalizar Simulacao  ",  font="arial 13 bold", fg="black", width=17, command=self.simulacao_incompleta)
        self.finalizar.pack()
        
        self.carregar = Button(self.window, text="  Carregar  ", font="arial 13 bold", fg="black", width=17, command=self.carregar)
        self.carregar.pack()

        # Design do Progresso #
        self.area = Label(self.window, text="  Progresso:  ", font="arial 13 bold", fg="white")
        self.area.pack(side="left", pady=20)
        self.progresso = ttk.Progressbar(self.window, orient='horizontal', mode='determinate', length=100)
        self.progresso.pack(side="left")
        
        self.window.mainloop()
    
    # Def para rodar a simulacao e abrir uma janela no final da simulacao #   
    def simulacao_completa(self):
        window = Toplevel()
        window.title("  Simulacao Completa  ") 
        window.resizable(0,0)
        window.geometry("300x200+300+200")
        text = Label(window, text="  Simulacao completa  ",  font="arial 13 bold", pady=30)
        text.pack()
        
        button_exit = Button(window, text="  OK  ",  font="arial 13 bold", command=window.destroy)
        button_exit.pack()
    
    # Def para interromper a simulacao e abrir uma janela quando #    
    def simulacao_incompleta(self):
        window = Toplevel()
        window.title("  ERROR  ") 
        window.resizable(0,0)
        window.geometry("300x200+300+200")
        text = Label(window, text="  Simulacao Interrompida  ", font="arial 13 bold", pady=30)
        text.pack()
        
        button_exit = Button(window, text="  OK  ",  font="arial 13 bold", command=window.destroy)
        button_exit.pack()
    
    # Def para carregar o txt para rodar as simulacoes #    
    def carregar(self):
        filetypes =(('Arquivos de Texto', '*.txt'), ('Todos Arquivos', '*.*'))
        filename = filedialog.askopenfilename()
        window = Toplevel()
        window.title("  Carregamento  ") 
        window.resizable(0,0)
        window.geometry("300x200+300+200")
        text = Label(window, text="  Carregamento Concluido  ", font="arial 13 bold", pady=30)
        text.pack()
        button_exit = Button(window, text="  OK  ",  font="arial 13 bold", command=window.destroy)
        button_exit.pack()
        
    # Def para salvar o txt com as simulacoes #
    def salvar(self):
        files = (('Arquivos de Texto', '*.txt'), ('Todos Arquivos', '*.*'))
        file = filedialog.asksaveasfile(filetypes= files, defaultextension= files)
        window = Toplevel()
        window.title("  Salvar  ") 
        window.resizable(0,0)
        window.geometry("300x200+300+200")
        text = Label(window, text="  Salvamento Concluido  ", font="arial 13 bold", pady=30)
        text.pack()
        button_exit = Button(window, text="  OK  ",  font="arial 13 bold", command=window.destroy)
        button_exit.pack()
         
SDP()
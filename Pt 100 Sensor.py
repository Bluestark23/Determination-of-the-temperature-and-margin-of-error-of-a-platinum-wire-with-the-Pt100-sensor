# -*- coding: utf-8 -*-
"""
Created on Thu Sep 07 16:44:49 2021

@author: Tadeo Daniel
"""
import cv2
import numpy as np

from tkinter import Tk,Text,Label,ttk,filedialog,StringVar,Menu,Toplevel,messagebox 
from PIL import Image,ImageTk
import imutils
import shutil
import ntpath
from scipy.interpolate import lagrange
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

class Interfaz:
    def __init__(self,ventana1):
        ancho_ventana = 500
        alto_ventana = 300
        ventana1.configure(bg='blue')
        x_ventana = ventana1.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = ventana1.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        ventana1.geometry(posicion)

        ventana1.resizable(0,0)
        self.ventana1=ventana1 
        self.ventana1.title("Tarea")
        self.la1=Label(ventana1,text="Num. de *C a buscado:")
        self.la1.place(x=25,y=45)               
        self.entrada=ttk.Entry(ventana1)
        self.entrada.place(x=160,y=45)
        
        self.la2=Label(ventana1,text="R:")
        self.la2.place(x=25,y=70)
        self.resultado=ttk.Entry(ventana1,textvariable=Resultados)
        self.resultado.place(x=160,y=70)
        
        self.btn=ttk.Button(ventana1,text="Guardar",width=45,command=self.Pt100)
        self.btn.place(x=25,y=100)


        self.Eror1=Label(ventana1,text="Porcentaje de error:")
        self.Eror1.place(x=25,y=130)
        self.Eror=Label(ventana1)
        self.Eror.place(x=160,y=130)
        self.btn1=ttk.Button(ventana1,text="Calcular error",width=45,command=self.error)
        self.btn1.place(x=25,y=155)

        self.Nota=Label(ventana1,text="Nota:Es obligatoria valores a Num de *C y *C de la tabla a calcular antes de calcular.")
        self.Nota.place(x=25,y=20)
       
        self.la3=Label(ventana1,text="¿Valor *C de la tabla?:")
        self.la3.place(x=25,y=190)
        self.grafica1=ttk.Entry(ventana1)
        self.grafica1.place(x=160,y=190)
        self.la4=Label(ventana1,text="Ohms de la tabla:")
        self.la4.place(x=25,y=210)
        self.resultado2=ttk.Entry(ventana1,textvariable=Resultados2)
        self.resultado2.place(x=160,y=210)
        self.btn=ttk.Button(ventana1,text="Graficar",width=45,command=self.tabla)
        self.btn.place(x=25,y=240)
        
        
  
    def Pt100(self):
        #formula Rt=100(1+3.9*10**-3*90)##la formula segun para el platino es 3.9*10 pero
        #para estar sincronizados con la trabala debe ser 3.856
        T=int(self.entrada.get())    
        Rt=float(100*(1+3.85*10**-3*T))
        Resultados.set(Rt)  
        T2=int(self.grafica1.get())    
        Rt2=float(100*(1+3.85*10**-3*T2))
        Resultados2.set(Rt2)  
        
    def error(self):
        #formula para la taza de error

        A=int(self.entrada.get()) 
        B=int(self.grafica1.get())
        r=A-B   
        E=(r/A)*100
        self.Eror.configure(text=E)
    
    def tabla(self):
 
        A=int(self.entrada.get())
        B=int(self.grafica1.get())
        i=0
        x=[]
        w=0
        y=[]
        xy=[]       
        x2=[]     
        
        Tr=float(100*(1+3.85*10**-3*B))
        
        
        
        for i in range(B):
                    x.append(i+1) 
                    
                    r=float(100*(1+3.85*10**-3*x[i]))
                    y.append(r)                           
                    ##minimos cuadrados         
                    sumax = sum(x)
                    sumay = sum(y)
                    xy=np.multiply(x,y)   
                    x2=np.power(x,2)
                    sumax2=sum(x2)
                    sumaxy=sum(xy)
                    print(x[i],y[i],"hola","taco","sumax",sumax,"sumay",sumay,"xy",sumaxy,"x2",sumax2)
                  
                    ##calculo de la pendiente
                    Tam=(sumax)*(sumay)/max(x)
                    Po=sumaxy-Tam
                    To=sumax2-(sumax**2)/max(x)
                    Pendiente=Po/To
                    print("Pendiente M:",Pendiente)
                    
                    #calculo de la media de los valores de x y la media de lox valores de y 
                    Lo=sumay/x[i]-Pendiente*sumax/x[i]  #max(x) y x[i] muestran el dato mas alto
                    print("Intercepcion B:",Lo)
                    #calcular la intercepcion en y
                    
                    #Ecuacion mx+b
                    maximoy=Pendiente*A+Lo
                    print("Eje y: ",maximoy)
                    print("++++++++++++++++++++++++++++") 
                    
                   
                    
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.plot(5,90)
        ax.set_title("Grafica",fontsize=15)
        ax.set_xlabel("*C",fontsize=12)
        ax.set_ylabel("Ohm",fontsize=12)
        ax.plot(x,y,marker="o",color="blue")
        ax.plot([min(x),A],[min(y),maximoy],color="red",linestyle="solid",marker="<")##tiene un bug el cual no grafica bien los datos cuando

        ax.legend(('Valor que estoy buscando(rojo)','Valor maximo de la tabla(azul)'),prop = {'size':10}, loc = 'upper right')
        plt.show()
         
ventana_principal=Tk()##instancia la ventana principal,solo puede haber 1
 

Resultados=StringVar()        
Resultados2=StringVar()
Reconocimiento= Interfaz(ventana_principal)###mandamos los datos a la clase interfaz
ventana_principal.mainloop()#para los eventos
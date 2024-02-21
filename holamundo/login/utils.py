from .models import  Casos, Clientes
import pandas as pd


def extraer_clientes():
   

   tabla= pd.read_excel('C:/Users/alvar\Documents/GitHub/Proyecto/Consultorio_Efren/Consultorio_Efren/holamundo/media/documentos/Clientes.xlsx')

   for indice,linea in tabla.iterrows():
     objeto_cliente, created = Clientes.objects.update_or_create(nombrec=linea['Cliente'])
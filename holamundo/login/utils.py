from .models import  *
import pandas as pd


def extraer_clientes():
   

   tabla= pd.read_excel('C:/Users/alvar\Documents/GitHub/Proyecto/Consultorio_Efren/Consultorio_Efren/holamundo/media/documentos/Clientes.xlsx')

   for indice,linea in tabla.iterrows():
     objeto_cliente, created = Clientes.objects.update_or_create(nombrec=linea['Cliente'])

def es_abogado(user):
    if hasattr(user, 'abogado'):
       return  True
    else:
       return False

def es_cliente(user):
    if hasattr(user, 'cliente'):
       return  True
    else:
       return False

       
    
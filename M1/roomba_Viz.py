'''
    Visualización Roomba
    Autores: 
        Jorge Rojas Rivas A01745334, 
        Omar Rodrigo Talavera A01752221
    Este código grafica un comportamiento simple de una aspiradora
    automática que prioriza moverse a celdas sucias.
    Noviembre, 2022
'''

from roomba_model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

'''
La función es un diccionario que permite a los agentes 
ser representados graficamente.
'''
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "purple",
                 "r": 0.5}

    if agent.object == "roomba":
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
    elif agent.object == "dirty":
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
    elif agent.object == "clean":
        portrayal["Layer"] = 0
        portrayal["r"] = 0.1

    return portrayal

ancho = 28
alto = 28
grid = CanvasGrid(agent_portrayal, ancho, alto, 375, 375)
server = ModularServer(RoombaModel,
                       [grid],
                       "Roomba Model",
                       {"N": 4, "P": 70, "width":ancho, "height":alto})
server.port = 8521
server.launch()
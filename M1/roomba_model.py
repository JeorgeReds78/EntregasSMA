"""
    Modelación Roomba
    Autores: 
        Jorge Rojas Rivas A01745334, 
        Omar Rodrigo Talavera A01752221
    Este código modela un comportamiento simple de una aspiradora
    automática que prioriza moverse a celdas sucias.
    Noviembre, 2022
"""

import mesa
import numpy as np

'''
Representa un agente aspiradora.
'''
class RoombaAgent(mesa.Agent):
    '''
    Inicializa el agente obteniendo una identificación única y el modelo 
    del que es llamado. Su estado le confiere su forma gráfica.
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.object = "roomba"
        self.new_position = None
        
    '''
    El metodo que permite que el agente se mueva hacia un espacio 
    aleaotrio o hacia la mugre. Solo se llama a sí mismo.
    '''        
    def step(self):
        '''
        Las coordenadas de su alrededor.
        '''
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        
        '''
        Toma los vecinos que esten alrededor del agente.
        '''
        self.possible_dirt = self.model.grid.get_neighbors(self.pos,
            moore=True,
            include_center=False)
             
        '''
        Formula que recaba la mugre alrededor, revisa si son agentes mugre para recabarlos.
        Inicializa un arreglo vacío para uso futuro.
        '''
        self.dirt = []
        for i in self.possible_dirt:
            if (isinstance(i, RoombaDirt) and i.object == "dirty"):
                self.dirt.append(i.pos)
                
    '''
    El metodo no permite a los agentes actuar hasta que todos los
    existentes esten listos.
    '''
    def advance(self): 
        '''
        Si hay algo en la lista dirt, se va a la tierra, 
        si no eligen un lugar al azar.
        '''          
        if (self.dirt):
            self.new_position = self.random.choice(self.dirt)
            self.model.grid.move_agent(self, self.new_position)
        else:
            self.new_position = self.random.choice(self.neighborhood)            
            self.model.grid.move_agent(self, self.new_position)

'''
Representa un agente de mugre.
'''
class RoombaDirt(mesa.Agent):
    '''
    Inicializa el agente obteniendo una identificación única y el modelo 
    del que es llamado. Su estado le confiere su forma gráfica.
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.object = "dirty"
        self.next_state = "dirty"                             
    
    '''
    Revisa si el agente mugre será limpiado al buscar a un agente aspiradora
    en su posición personal. Solo se llama a sí mismo. 
    '''
    def step(self):
        self.cleaniness = self.model.grid.get_cell_list_contents([self.pos])
        for i in self.cleaniness:
            if isinstance(i, RoombaAgent):
                self.next_state = "clean"           

    '''
    El metodo no permite a los agentes actuar hasta que todos los
    existentes esten listos. Solo se llama a sí mismo.
    '''
    def advance(self):
        self.object = self.next_state
    
    
'''
Representa el modelo de los agentes.
'''       
class RoombaModel(mesa.Model):
    '''
    Inicializa el modelo obteniendo el número de aspiradoras a generar,
    el porcentaje de la cuadricula a ensuciar, así como las dimensiones
    de la misma.
    '''
    def __init__(self, N, P, width, height):
        self.num_agents = N
        self.probability = P
        '''
        MultiGrid permite a los agentes compartir un mismo espacio.
        '''
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.running = True        
        
        '''
        Crea un nuevo agente roomba tantas veces como haya sido dictado.
        '''
        for i in range(self.num_agents):
            a = RoombaAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))
            
        '''
        Genera la mugre con base en la probabilidad dictada evitando el
        espacio inicial de los agentes aspiradora ya que resultaría
        redundante.
        '''    
        for (content, x, y) in self.grid.coord_iter():
            rn = np.random.randint(0, 99)
            if (x == 1 and y == 1):
                print("")
            elif (rn < self.probability):
                b = RoombaDirt((x, y), self)
                self.grid.place_agent(b, (x, y))
                self.schedule.add(b)
                
    '''
    Declara el siguiente paso que todos toman.
    '''
    def step(self):
        self.schedule.step()
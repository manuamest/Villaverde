
from dialogue_strategy import Dialogue_Strategy

class DialogoPolloEstrategia(Dialogue_Strategy):

    def __init__(self, draw, escene, animales):
        self.animals = animales
        self.draw = draw
        self.escene = escene
        
        self.animals = animales if animales is not None else []

    def set_animals(self, animals):
        self.animals = animals

    def obtener_dialogo(self, contexto,escene,draw):

        if contexto.get_contador_llave() == 3:
                return self.draw.dialogos_llave_magistral
        if contexto.obtener_opcion_escogida_pollo():
            if contexto.obtener_opcion_seleccionada() == 1:
                return self.draw.dialogos_pollo_4
            elif contexto.obtener_opcion_seleccionada() == 0:
                return self.draw.dialogos_pollo_2 if contexto.get_jordan_dadas() else self.draw.dialogos_pollo_3
        else:
            return self.draw.dialogos_pollo
    def manejar_opciones(self, contexto,draw):
        return ["Dar Jordan a la gallina Daniel", "Tendras que esperar por tus Jordan"]
    
    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje,contexto,escene,draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if contexto.get_contador_llave() == 3 and fin_dialogo:
            contexto.set_final_dialogo(True)
        elif contexto.obtener_opcion_escogida_pollo() and (contexto.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo:
            contexto.set_final_dialogo(True)
        elif not contexto.obtener_opcion_escogida_pollo() and fin_dialogo:
            contexto.manejar_opciones_personaje(keys, inventory, inicio_texto_x, inicio_texto_y, personaje)
    
    def ejecutar_accion(self, inventory, contexto,personaje,draw):
        if not contexto.get_jordan_dadas():
            if contexto.opcion_seleccionada == 0:
                    contexto.set_opcion_seleccionada(0)
                    contexto.set_opcion_escogida_pollo(True)
                    if inventory.get_jordan():
                        contexto.set_jordan_dadas(True)
                        inventory.eliminar_jordan()
                        self.animals[1].target_positions = [(self.animals[1].pos[0]+ 5, self.animals[1].pos[1] + 5), (self.animals[1].pos[0] - 5, self.animals[1].pos[1] - 5)]
                        self.animals[1].make_prime()
                        contexto.set_incr_llave(1)
                        if contexto.get_contador_llave() == 3:
                            inventory.añadir_llave()
                    else:
                        contexto.set_jordan_dadas(False)
            elif contexto.opcion_seleccionada == 1:
                contexto.set_opcion_seleccionada(1)
                contexto.set_opcion_escogida_pollo(True)
                contexto.set_jordan_dadas(False)
    

    def reset_dialogo(self,keys, dialogos_personaje,timers,personaje_actual,contexto,escene,draw):
        contexto.set_opcion_dialogo(True)
        contexto.set_indice_personaje(personaje_actual, 0)
        contexto.set_opcion_seleccionada(0)
        if contexto.obtener_opcion_escogida_pollo():
            if contexto.obtener_final_dialogo():   
                if contexto.obtener_opcion_seleccionada() == 0:
                
                    if contexto.get_contador_llave() == 3:

                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_bufandas_dadas(True)
                        contexto.set_opcion_escogida_oveja(True)
                        contexto.set_indice_personaje(personaje_actual, 0) 
                        personaje_actual = None
                    elif contexto.get_jordan_dadas():
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_jordan_dadas(True)
                        contexto.set_opcion_escogida_pollo(True)
                        contexto.set_indice_personaje(personaje_actual, 0) 
                        personaje_actual = None
                    else:
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_jordan_dadas(False)
                        contexto.set_opcion_escogida_pollo(False)
                        contexto.set_indice_personaje(personaje_actual, 2) 
                        personaje_actual = None


                elif contexto.obtener_opcion_seleccionada() == 1:
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_jordan_dadas(False)
                        contexto.set_opcion_escogida_pollo(False)
                        contexto.set_indice_personaje(personaje_actual, 2) 
                        personaje_actual = None
        
        else:
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_jordan_dadas(False)
                        contexto.set_opcion_escogida_pollo(False)
                        contexto.set_indice_personaje(personaje_actual, 2) 
                        personaje_actual = None
        
        

class DialogoVacaEstrategia(Dialogue_Strategy):
    def __init__(self, draw, escene, animales):
        self.animals = animales
        self.draw = draw
        self.escene = escene
        
        self.animals = animales if animales is not None else []

    def set_animals(self, animals):
        self.animals = animals

    def obtener_dialogo(self, contexto,escene,draw):
        if contexto.obtener_opcion_escogida_vaca():
            if contexto.get_contador_llave() == 3:
                return self.draw.dialogos_llave_magistral
            elif contexto.obtener_opcion_seleccionada() == 1:
                return self.draw.dialogos_vaca_4
            elif contexto.obtener_opcion_seleccionada() == 0:
                return self.draw.dialogos_vaca_2 if contexto.get_gafas_dadas() else self.draw.dialogos_vaca_3
        else:
            return contexto.draw.dialogos_vaca

    def manejar_opciones(self, contexto,draw):
        return ["Dar gafas Swarovski para que vaya con estilo", "Lo siento Vaca Klara, aun no las he conseguido"]
    
    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje,contexto,escene,draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if contexto.get_contador_llave() == 3 and fin_dialogo:
            contexto.set_final_dialogo(True)

        elif contexto.obtener_opcion_escogida_vaca() and (contexto.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo:
            contexto.set_final_dialogo(True)
        elif not contexto.obtener_opcion_escogida_vaca() and fin_dialogo:
            contexto.manejar_opciones_personaje(keys, inventory, inicio_texto_x, inicio_texto_y, personaje)
    
    def ejecutar_accion(self, inventory, contexto,personaje,draw):
        if not contexto.get_gafas_dadas():
            if contexto.opcion_seleccionada == 0:
                contexto.set_opcion_seleccionada(0)
                contexto.set_opcion_escogida_vaca(True)
                if inventory.get_gafas():
                    contexto.set_gafas_dadas(True)
                    inventory.eliminar_gafas()
                    self.animals[2].make_prime()
                    contexto.set_incr_llave(1)
                    if contexto.get_contador_llave() == 3:
                        inventory.añadir_llave()
                else:
                        contexto.set_gafas_dadas(False)
            elif contexto.opcion_seleccionada == 1:
                contexto.set_opcion_seleccionada(1)
                contexto.set_opcion_escogida_vaca(True)
                contexto.set_gafas_dadas(False)
    

    def reset_dialogo(self,keys, dialogos_personaje,timers,personaje_actual,contexto,escene,draw):
            contexto.set_opcion_dialogo(True)
            contexto.set_indice_personaje(personaje_actual, 0)
            contexto.set_opcion_seleccionada(0)
            if contexto.obtener_opcion_escogida_vaca():
                if contexto.obtener_final_dialogo():   
                    if contexto.obtener_opcion_seleccionada() == 0:


                        if contexto.get_contador_llave() == 3:
                            contexto.set_opcion_dialogo(False)
                            contexto.set_final_dialogo(False)
                            contexto.set_gafas_dadas(True)
                            contexto.set_opcion_escogida_vaca(True)
                            contexto.set_indice_personaje(personaje_actual, 0) 
                            personaje_actual = None


                        elif contexto.get_gafas_dadas():
                            contexto.set_opcion_dialogo(False)
                            contexto.set_final_dialogo(False)
                            contexto.set_gafas_dadas(True)
                            contexto.set_opcion_escogida_vaca(True)
                            contexto.set_indice_personaje(personaje_actual, 0) 
                            personaje_actual = None
                        else:
                            contexto.set_opcion_dialogo(False)
                            contexto.set_final_dialogo(False)
                            contexto.set_gafas_dadas(False)
                            contexto.set_opcion_escogida_vaca(False)
                            contexto.set_indice_personaje(personaje_actual, 2) 
                            personaje_actual = None


                    elif contexto.obtener_opcion_seleccionada() == 1:
                            contexto.set_opcion_dialogo(False)
                            contexto.set_final_dialogo(False)
                            contexto.set_gafas_dadas(False)
                            contexto.set_opcion_escogida_vaca(False)
                            contexto.set_indice_personaje(personaje_actual, 2) 
                            personaje_actual = None


class DialogoOvejaEstrategia(Dialogue_Strategy):

    def __init__(self, draw, escene, animales):
        self.animals = animales
        self.draw = draw
        self.escene = escene
        
        self.animals = animales if animales is not None else []

    def set_animals(self, animals):
        self.animals = animals
    def obtener_dialogo(self, contexto,escene,draw):
        if contexto.obtener_opcion_escogida_oveja():
            if contexto.get_contador_llave() == 3:
                return self.draw.dialogos_llave_magistral
            elif contexto.obtener_opcion_seleccionada() == 1:
                return self.draw.dialogos_oveja_4
            elif contexto.obtener_opcion_seleccionada() == 0:
                return self.draw.dialogos_oveja_2 if contexto.get_bufandas_dadas() else self.draw.dialogos_oveja_3
        else:
            return contexto.draw.dialogos_oveja
    
    def manejar_opciones(self, contexto,draw):
        return ["Dar bufanda Ovejana a Oscar", "Oscar, aun no te puedo dar tu bufanda"]
    
    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje,contexto,escene,draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if contexto.get_contador_llave() == 3 and fin_dialogo:
            contexto.set_final_dialogo(True)

        elif contexto.obtener_opcion_escogida_oveja() and (contexto.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo:
            contexto.set_final_dialogo(True)
        elif not contexto.obtener_opcion_escogida_oveja() and fin_dialogo:
            contexto.manejar_opciones_personaje(keys, inventory, inicio_texto_x, inicio_texto_y, personaje)
    
    def ejecutar_accion(self, inventory, contexto,personaje,draw):
        if not contexto.get_bufandas_dadas():       
            if contexto.opcion_seleccionada == 0:
                contexto.set_opcion_seleccionada(0)
                contexto.set_opcion_escogida_oveja(True)
                if inventory.get_bufandas():
                    contexto.set_bufandas_dadas(True)
                    inventory.eliminar_bufandas()
                    self.animals[0].make_prime()
                    contexto.set_incr_llave(1) 
                    if contexto.get_contador_llave() == 3:
                        inventory.añadir_llave()
                else:
                    contexto.set_bufandas_dadas(False)
            elif contexto.opcion_seleccionada == 1:
                contexto.set_opcion_seleccionada(1)
                contexto.set_opcion_escogida_oveja(True)
                contexto.set_bufandas_dadas(False)


    def reset_dialogo(self,keys, dialogos_personaje,timers,personaje_actual,contexto,escene,draw):
        contexto.set_opcion_dialogo(True)
        contexto.set_indice_personaje(personaje_actual, 0)
        contexto.set_opcion_seleccionada(0)
        if contexto.obtener_opcion_escogida_oveja():
            if contexto.obtener_final_dialogo():   
                if contexto.obtener_opcion_seleccionada() == 0:

                    if contexto.get_contador_llave() == 3:

                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_bufandas_dadas(True)
                        contexto.set_opcion_escogida_oveja(True)
                        contexto.set_indice_personaje(personaje_actual, 0) 
                        personaje_actual = None

                    elif contexto.get_bufandas_dadas():
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_bufandas_dadas(True)
                        contexto.set_opcion_escogida_oveja(True)
                        contexto.set_indice_personaje(personaje_actual, 0) 
                        personaje_actual = None
                        
                    else:
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_bufandas_dadas(False)
                        contexto.set_opcion_escogida_oveja(False)
                        contexto.set_indice_personaje(personaje_actual, 2) 
                        personaje_actual = None


                elif contexto.obtener_opcion_seleccionada() == 1:
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_bufandas_dadas(False)
                        contexto.set_opcion_escogida_oveja(False)
                        contexto.set_indice_personaje(personaje_actual, 2) 
                        personaje_actual = None
        

        else:

                    contexto.set_opcion_dialogo(False)
                    contexto.set_final_dialogo(False)
                    contexto.set_bufandas_dadas(False)
                    contexto.set_opcion_escogida_oveja(False)
                    contexto.set_indice_personaje(personaje_actual, 2) 
                    personaje_actual = None

class DialogoCabraEstrategia(Dialogue_Strategy):
    def obtener_dialogo(self, contexto,escene,draw):
        return self.draw.dialogos_cabra    

    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje,contexto,escene,draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if fin_dialogo:
            contexto.set_final_dialogo(True)
            contexto.set_ultimo_dialogo_cabra(True)
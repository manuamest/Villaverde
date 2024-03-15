
class Dialogue_Strategy:
    
    def __init__(self, draw,escene):
        self.draw = draw
        self.escene = escene

    def obtener_dialogo(self, contexto,escene,draw):
        pass
    
    def manejar_opciones(self, contexto,draw):
        pass
    
    def ejecutar_accion(self, inventory, contexto,personaje,draw):
        pass
    
    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje,contexto,escene,draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if fin_dialogo and personaje in ["butanero","mercader","modista","pollo","oveja","vaca"]:
            contexto.manejar_opciones_personaje(keys, inventory, inicio_texto_x, inicio_texto_y, personaje)

    def reset_dialogo(self,keys, dialogos_personaje,timers,personaje_actual,contexto,escene,draw):
        contexto.set_opcion_dialogo(False)
        contexto.set_final_dialogo(False)
        contexto.set_confirmacion_abierta(False)
        contexto.set_opcion_escogida(False)
        contexto.set_indice_personaje(personaje_actual, 0)
        personaje_actual = None
        
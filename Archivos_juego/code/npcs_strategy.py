from dialogue_strategy import Dialogue_Strategy


# Estrategia Don Diego
class DialogoDonDiegoEstrategia(Dialogue_Strategy):

    def obtener_dialogo(self, contexto,escene,draw):
        if escene == "Nivel1":
            return self.draw.dialogos_dondiego
        else:
            return self.draw.dialogos_dondiego_2      


# Estrategia Obrero
class DialogoObreroEstrategia(Dialogue_Strategy):
    
    def obtener_dialogo(self, contexto, escene, draw):
        if contexto.obtener_opcion_escogida_obrero():
            if contexto.obtener_opcion_seleccionada() == 0:
                if contexto.obtener_dinero_dado() and contexto.obtener_madera_dada():
                    return self.draw.dialogos_obrero_2
                elif contexto.obtener_madera_dada() and not contexto.obtener_dinero_dado():
                    return self.draw.dialogos_obrero_5
                
                elif not contexto.obtener_madera_dada() and contexto.obtener_dinero_dado():
                    return self.draw.dialogos_obrero_6
                elif not contexto.obtener_madera_dada():
                    return self.draw.dialogos_obrero_3
            elif contexto.obtener_opcion_seleccionada() == 1:
                    return self.draw.dialogos_obrero_4
        
        else:
            return self.draw.dialogos_obrero
        
    def manejar_opciones(self, contexto,draw):
        return ["Dar dinero y madera a Jordi", "Aun no te lo puedo dar"]
    
    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje, contexto, escene, draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if contexto.obtener_opcion_escogida_obrero() and (contexto.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo:
            contexto.set_final_dialogo(True)
        elif not contexto.obtener_opcion_escogida_obrero() and fin_dialogo:
            contexto.manejar_opciones_personaje(keys, inventory, inicio_texto_x, inicio_texto_y, personaje)
    
    def ejecutar_accion(self, inventory, contexto,personaje,draw):
        if not contexto.obtener_dinero_dado() and not contexto.obtener_madera_dada():
            if contexto.opcion_seleccionada == 0:
                tiene_dinero = inventory.get_dinero() == 100
                tiene_madera = inventory.get_madera() >= 30
              
                if tiene_dinero and not tiene_madera:
                    contexto.set_dinero_dado(True)
                    contexto.set_madera_dada(False)
                    contexto.set_opcion_seleccionada(0) 
                    contexto.set_opcion_escogida_obrero(True)

                elif not tiene_dinero and tiene_madera:
                    contexto.set_madera_dada(True)
                    contexto.set_dinero_dado(False)
                    contexto.set_opcion_seleccionada(0) 
                    contexto.set_opcion_escogida_obrero(True)

                elif tiene_dinero and tiene_madera:
                    contexto.set_dinero_dado(True)
                    contexto.set_madera_dada(True)
                    contexto.set_opcion_seleccionada(0) 
                    inventory.eliminar_dinero(100)
                    inventory.eliminar_madera(30)
                    contexto.set_opcion_escogida_obrero(True)
                    contexto.set_objetos_a_jordi(True)
                
                else:
                    contexto.set_dinero_dado(False)
                    contexto.set_madera_dada(False)
                    contexto.set_opcion_seleccionada(0)
                    contexto.set_opcion_escogida_obrero(True)

            elif contexto.opcion_seleccionada == 1:
                contexto.set_dinero_dado(False)
                contexto.set_madera_dada(False)
                contexto.set_opcion_seleccionada(1) 
                contexto.set_opcion_escogida_obrero(True)

    def reset_dialogo(self,keys, dialogos_personaje, timers, personaje_actual, contexto, escene, draw):
        contexto.set_opcion_dialogo(True)
        contexto.set_indice_personaje(personaje_actual, 0)
   
        if contexto.obtener_opcion_escogida_obrero():
            if contexto.obtener_final_dialogo():   
                if contexto.obtener_opcion_seleccionada() == 0:
                    if contexto.obtener_dinero_dado() and contexto.obtener_madera_dada():
                        contexto.set_dinero_dado(True)
                        contexto.set_madera_dada(True)
                        contexto.set_indice_personaje(personaje_actual, 0)
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_opcion_escogida_obrero(True)
                        contexto.set_opcion_seleccionada(0)
                        personaje_actual = None
                    else:
                        contexto.set_dinero_dado(False)
                        contexto.set_madera_dada(False)
                        contexto.set_indice_personaje(personaje_actual, 3)
                        contexto.set_opcion_dialogo(False)
                        contexto.set_final_dialogo(False)
                        contexto.set_opcion_escogida_obrero(False)
                        contexto.set_opcion_seleccionada(0)
                        personaje_actual = None
                else:
                    contexto.set_dinero_dado(False)
                    contexto.set_madera_dada(False)
                    contexto.set_indice_personaje(personaje_actual, 3)
                    contexto.set_opcion_dialogo(False)
                    contexto.set_final_dialogo(False)
                    contexto.set_opcion_escogida_obrero(False)
                    contexto.set_opcion_seleccionada(0)
                    personaje_actual = None

# Estrategia Mercader
class DialogoMercaderEstrategia(Dialogue_Strategy):
    
    def obtener_dialogo(self, contexto, escene, draw):
        if escene== "Nivel2":
            if contexto.obtener_opcion_escogida():
                if contexto.obtener_opcion_seleccionada() == 1:
                    return self.draw.dialogos_mercader_6
                elif contexto.obtener_opcion_seleccionada() == 0:
                    return self.draw.dialogos_mercader_4 if contexto.obtener_material_dado() else self.draw.dialogos_mercader_5
            elif contexto.obtener_confirmacion_abierta():
                if draw.obtener_cantidad_seleccionada() == 0:
                    return self.draw.dialogos_mercader_3
                else:
                    pago = contexto.calcular_pago("mercader", draw.item_seleccionado, draw.cantidad_seleccionada)
                    return ["Seguro que quieres vender {} unidades de {}? Te ofrecere por ello {} unidades de dinero. Hay trato?\u00A0".format(draw.cantidad_seleccionada, draw.item_seleccionado[0].lower() + draw.item_seleccionado[1:] if draw.item_seleccionado else '', pago)]
            else:
                return self.draw.dialogos_mercader
        elif escene == "Nivel3":
            return self.draw.dialogos_mercader_7
        
    def manejar_opciones(self, contexto,draw):
        return ["Si, quiero venderlo", "No, no me interesa"]
    
    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje, contexto, escene, draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if escene == "Nivel2":
            if contexto.obtener_dialogo() and not contexto.obtener_final_dialogo():  
                # Solo dibuja el inventario mientras el menú esté abierto y el diálogo no haya terminado
                inventory.dibujar_inventario((draw.pantalla_ancho // 2 + 1200 // 2 - 400),(draw.pantalla_alto // 2 - 400 // 2 - 155),True)
            if contexto.obtener_opcion_escogida() and (contexto.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo and contexto.confirmacion_abierta:
                contexto.set_final_dialogo(True)
            elif draw.obtener_cantidad_seleccionada() == 0 and contexto.obtener_confirmacion_abierta() and not contexto.obtener_opcion_escogida():
                draw.dibujar_menu(personaje, inventory, keys)
            
            elif contexto.obtener_opcion_seleccionada() == 1 and contexto.obtener_opcion_escogida():
                draw.dibujar_menu(personaje, inventory, keys)
            
            elif fin_dialogo and not contexto.confirmacion_abierta:
                draw.dibujar_menu(personaje, inventory, keys)
        
            elif not contexto.obtener_opcion_escogida() and fin_dialogo and contexto.confirmacion_abierta:
                contexto.manejar_opciones_personaje(keys, inventory, inicio_texto_x, inicio_texto_y, personaje)
           
    def ejecutar_accion(self, inventory, contexto, personaje, draw):
        contexto.set_opcion_escogida(True)
        pago = contexto.calcular_pago(personaje, draw.item_seleccionado, draw.cantidad_seleccionada)

        material_suficiente = False
        if draw.item_seleccionado == "Madera":
            cantidad_disponible = inventory.get_madera()
            material_suficiente = draw.cantidad_seleccionada <= cantidad_disponible
        elif draw.item_seleccionado == "Trigo":
            cantidad_disponible = inventory.get_trigo()
            material_suficiente = draw.cantidad_seleccionada <= cantidad_disponible

        if contexto.opcion_seleccionada == 0 and material_suficiente:
            contexto.set_opcion_seleccionada(0)
            contexto.set_material_dado(True)
            if draw.item_seleccionado == "Madera":
                inventory.eliminar_madera(draw.cantidad_seleccionada)
                draw.set_opcion_menu(0)
            elif draw.item_seleccionado == "Trigo":
                inventory.eliminar_trigo(draw.cantidad_seleccionada)
                draw.set_opcion_menu(0)
            inventory.añadir_dinero_mercader(pago)
        else:
            contexto.set_opcion_seleccionada(0 if contexto.opcion_seleccionada == 0 else 1)
            contexto.set_material_dado(False)

    def reset_dialogo(self,keys, dialogos_personaje,timers,personaje_actual,contexto,escene,draw):
        if escene == "Nivel2":
            if not contexto.obtener_opcion_escogida():
               contexto.set_opcion_seleccionada(0)
            if contexto.obtener_confirmacion_abierta():
                contexto.set_opcion_dialogo(True)
                contexto.set_indice_personaje("mercader", 0)
                if contexto.obtener_opcion_escogida() and (contexto.obtener_opcion_seleccionada() == 0 or contexto.obtener_opcion_seleccionada() == 1):
                    contexto.set_opcion_dialogo(True)
                    if contexto.obtener_opcion_escogida():
                        if contexto.obtener_final_dialogo():
                            contexto.set_opcion_dialogo(False)
                            contexto.set_final_dialogo(False)
                            contexto.set_confirmacion_abierta(False)
                            contexto.set_opcion_escogida(False)
                            contexto.set_indice_personaje("mercader", 2) 
                            contexto.cantidades = {"Madera": 0, "Trigo": 0, "Jordan": 0, "Bufanda y boina": 0, "Gafas y cadena": 0}
        else:
            contexto.set_opcion_dialogo(False)
            contexto.set_final_dialogo(False)
            contexto.set_confirmacion_abierta(False)
            contexto.set_opcion_escogida(False)
            contexto.set_indice_personaje(personaje_actual, 0)
            personaje_actual = None

# Estrategia Modista
class DialogoModistaEstrategia(Dialogue_Strategy):

    def obtener_dialogo(self, contexto, escene, draw):
        if contexto.todo_vendido == 1: 
            return self.draw.dialogos_modista_8
        elif contexto.obtener_opcion_escogida():
            if contexto.obtener_opcion_seleccionada() == 1:
                return self.draw.dialogos_modista_6
            elif contexto.obtener_opcion_seleccionada() == 0:
                return self.draw.dialogos_modista_4 if contexto.obtener_material_dado() else self.draw.dialogos_modista_5
        elif contexto.obtener_confirmacion_abierta():
            if draw.obtener_cantidad_seleccionada() == 0:
                return self.draw.dialogos_modista_3
            elif draw.obtener_cantidad_seleccionada() == 1 and ((draw.obtener_item_seleccionado() == "Jordan" and contexto.jordan_compradas) 
             or (draw.obtener_item_seleccionado() == "Bufanda y boina" and contexto.bufandas_compradas) 
             or (draw.obtener_item_seleccionado() == "Gafas y cadena" and contexto.gafas_compradas)):
                return self.draw.dialogos_modista_7

            else:
                pago = contexto.calcular_pago("modista", draw.item_seleccionado, draw.cantidad_seleccionada)
                return ["Seguro que quieres comprar {} unidad de {}? Te cobrare por ello {} unidades de dinero. Es una buena oferta, verdad?\u00A0".format(draw.cantidad_seleccionada, draw.item_seleccionado[0].lower() + draw.item_seleccionado[1:] if draw.item_seleccionado else '', pago)]
        else:
            return self.draw.dialogos_modista
    
    def manejar_opciones(self, contexto,draw):
        return ["Si, quiero comprarlo", "Tengo que ahorrar mas, estoy pobre"]
    
    def manejar_interacciones(self, keys, inventory, inicio_texto_x, inicio_texto_y, longitud_actual, personaje, contexto, escene, draw):
        dialogos_personaje = contexto.obtener_dialogo_personaje(personaje)
        indice_dialogo = contexto.obtener_indice_personaje(personaje)
        fin_dialogo = longitud_actual >= len(dialogos_personaje[indice_dialogo]) and indice_dialogo == len(dialogos_personaje) - 1

        if contexto.obtener_dialogo() and not contexto.obtener_final_dialogo() and not (contexto.jordan_compradas and  contexto.bufandas_compradas and contexto.gafas_compradas):  
            inventory.dibujar_inventario((draw.pantalla_ancho // 2 + 1200 // 2 - 400),(draw.pantalla_alto // 2 - 400 // 2 - 155),True)
        
        if (contexto.jordan_compradas and  contexto.bufandas_compradas and contexto.gafas_compradas) and fin_dialogo:
            contexto.set_final_dialogo(True)

        if contexto.obtener_opcion_escogida() and (contexto.obtener_opcion_seleccionada() in [0, 1]) and fin_dialogo and contexto.confirmacion_abierta and not (contexto.jordan_compradas 
         and contexto.bufandas_compradas and contexto.gafas_compradas) :
            contexto.set_final_dialogo(True)

        elif draw.obtener_cantidad_seleccionada() == 0 and contexto.obtener_confirmacion_abierta() and not contexto.obtener_opcion_escogida():
            draw.dibujar_menu(personaje, inventory, keys)
        elif draw.obtener_cantidad_seleccionada() == 1 and contexto.obtener_confirmacion_abierta() and not contexto.obtener_opcion_escogida() and ((draw.obtener_item_seleccionado() == "Jordan" 
         and contexto.jordan_compradas) or (draw.obtener_item_seleccionado() == "Bufanda y boina" and contexto.bufandas_compradas) 
         or (draw.obtener_item_seleccionado() == "Gafas y cadena" and contexto.gafas_compradas)):
            draw.dibujar_menu(personaje, inventory, keys)

        elif contexto.obtener_opcion_seleccionada() == 1 and contexto.obtener_opcion_escogida():
            draw.dibujar_menu(personaje, inventory, keys)
        elif fin_dialogo and not contexto.confirmacion_abierta and not (contexto.jordan_compradas and  contexto.bufandas_compradas and contexto.gafas_compradas):
            draw.dibujar_menu(personaje, inventory, keys)
        elif not contexto.obtener_opcion_escogida() and fin_dialogo and contexto.confirmacion_abierta:
            contexto.manejar_opciones_personaje(keys, inventory, inicio_texto_x, inicio_texto_y, personaje)
    
    def ejecutar_accion(self, inventory, contexto, personaje, draw):
        contexto.set_opcion_escogida(True)
        pago = contexto.calcular_pago(personaje, draw.item_seleccionado, draw.cantidad_seleccionada)
        puede_comprar = pago <= inventory.get_dinero()

        if contexto.opcion_seleccionada == 0:
            if puede_comprar:
                contexto.set_opcion_seleccionada(0)
                contexto.set_material_dado(True)
                inventory.eliminar_dinero_modista(pago)
                if draw.item_seleccionado == "Jordan":
                    inventory.añadir_jordan()
                    contexto.jordan_compradas = True
                    draw.set_opcion_menu(0)
                elif draw.item_seleccionado == "Bufanda y boina":
                    inventory.añadir_bufandas()
                    contexto.bufandas_compradas = True
                    draw.set_opcion_menu(0)
                elif draw.item_seleccionado == "Gafas y cadena":
                    inventory.añadir_gafas()
                    contexto.gafas_compradas = True
                    draw.set_opcion_menu(0)
            else:
                contexto.set_opcion_seleccionada(0)
                contexto.set_material_dado(False)
        else:
            contexto.set_opcion_seleccionada(1)
            contexto.set_material_dado(False)


    def reset_dialogo(self,keys, dialogos_personaje, timers, personaje_actual, contexto, escene, draw):
        contexto.set_opcion_dialogo(True)
        contexto.set_indice_personaje(personaje_actual, 0)
        
        if not contexto.obtener_opcion_escogida():
            contexto.set_opcion_seleccionada(0)
            
        if contexto.jordan_compradas and  contexto.bufandas_compradas and contexto.gafas_compradas and contexto.todo_vendido == 1:
            contexto.set_opcion_dialogo(True)
            if contexto.obtener_final_dialogo():
                contexto.set_opcion_dialogo(False)
                contexto.set_final_dialogo(False)
                contexto.set_confirmacion_abierta(False)
                contexto.set_opcion_escogida(False)
                contexto.cantidades = {"Madera": 0, "Trigo": 0,"Jordan": 0, "Bufanda y boina": 0,"Gafas y cadena":0}
                contexto.set_indice_personaje(personaje_actual, 0) 
                personaje_actual = None

        if contexto.obtener_opcion_escogida() and (contexto.obtener_opcion_seleccionada() == 0 or contexto.obtener_opcion_seleccionada() == 1):
            if contexto.jordan_compradas and  contexto.bufandas_compradas and contexto.gafas_compradas and not contexto.obtener_final_dialogo():
                contexto.todo_vendido = 1
             
            contexto.set_opcion_dialogo(True)
            if  contexto.obtener_opcion_escogida():
                if contexto.obtener_final_dialogo():
                    contexto.set_opcion_dialogo(False)
                    contexto.set_final_dialogo(False)
                    contexto.set_confirmacion_abierta(False)
                    contexto.set_opcion_escogida(False)
                    contexto.cantidades = {"Madera": 0, "Trigo": 0,"Jordan": 0, "Bufanda y boina": 0,"Gafas y cadena":0}
                    contexto.set_indice_personaje(personaje_actual, 1) 
                    personaje_actual = None

# Estrategia Hermanos
class DialogoHermanosEstrategia(Dialogue_Strategy):
    def obtener_dialogo(self, contexto, escene, draw):
        return self.draw.dialogos_hermanos

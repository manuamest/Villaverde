import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Draw:
    def __init__(self,screen):
      
      self.pantalla = screen
      self.fuente = pygame.font.Font("./code/fonts/Stardew_Valley.ttf", 28)
      self.MARRON = (128, 58, 58)
      self.caracter_especial_dibujado = False
      self.marcador= '\u00A0' 
      self.definir_dialogos()
   
    def definir_dialogos(self):
        self.dialogos_dondiego  = ["Que va a ser de mi?, mi granja esta destrozada y Fer ha desaparecido...", "Por favor, Wuan, coge la bolsa que tengo en casa con todos mis ahorros y habla con Jordi el obrero, el quizas nos pueda ayudar.", "Todo esta en tus manos..."]
        self.dialogos_dondiego_2 = ["Ugh...ugh...necesito una monst...er.", "Querido Wuan, salva la granja...esta todo en tus manos.", "Eres el unico capaz de hacer que me vaya de esta vida en paz...cumple solo este favor..."]
        self.dialogos_butanero = ["Hola! Soy Jordi el butanero.", "Necesito que me des 5 unidades de dinero y 3 de madera, venga damelo que hay prisa!"]
        self.dialogos_butanero_2 = ["Genial! Ya era hora de que por fin me trajeras el dinero y la madera, sigue asi Wuan."]
        self.dialogos_butanero_3 = ["Estas sordo primo? Que te he dicho que me des el dinero y la madera, ya veo que no tienes suficientes unidades de ambos, traeme lo que te he pedido."]
        self.dialogos_butanero_4 = ["Me vas a tener esperando un tiempecito parece eh, avisame cuando los consigas"]
        self.dialogos_butanero_5 = ["Solo tienes madera, traeme el dinero tambien anda"]
        self.dialogos_butanero_6 = ["Solo tienes dinero, traeme la madera tambien anda"]
        self.dialogos_butanero_7 = ["No tienes suficientes unidades de dinero y madera, vuelve cuando tengas la cantidad que te pedi"]
        self.dialogos_mercader = ["Bienvenido a la tienda de Xoel el mercader, donde tu madera y trigo compra sin perder. Trae tus bienes, los frutos de tu labor, Xoel paga bien, con justicia y honor.", "Dicen que soy agarrado, de mi eso murmuran, por no soltar el dinero, criticas me aseguran. Mas si supieran la verdad, detras del velo y la penumbra, necesito cada centavo, para vivir sin ninguna duda.", "Dime Wuan, como te puedo estafar hoy?"]
        self.dialogos_mercader_3 = ["No puedes seleccionar 0 unidades."]
        self.dialogos_modista_3 = ["No puedes seleccionar 0 unidades querido Wuan...se paciente."]
        self.dialogos_mercader_4 = ["Es un placer hacer negocios contigo, vuelve cuando quieras!"]
        self.dialogos_mercader_5 = ["No tienes suficientes unidades del material, vuelve cuando tengas algo que ofrecerme."]
        self.dialogos_modista_4 = ["Es un placer hacer negocios contigo, vuelve cuando quieras!"]
        self.dialogos_modista_5 = ["No tienes suficiente dinero, vuelve cuando consigas mas dinero con Xoel el mercader."]
        self.dialogos_mercader_6 = ["Avisame si cambias de opinion!"]
        self.dialogos_mercader_7 = ["Parece que todo se termina aqui...me has descubierto, no eres tan despistado como pensaba","Malditos animales, se han revelado todos, pense que podria quedarme con la granja..."]
        self.dialogos_modista_7 = ["Lo siento Wuan, no nos quedan existencias de ese articulo...era una edicion limitada."]
        self.dialogos_modista_8 = ["Madre mia Wuan, has agotado las existencias de todos mis articulos, tendre que cerrar durante un tiempo para poder reponer la mercancia!"]
        self.dialogos_modista_6 = ["Juntos reconstruiremos la granja! Vuelve pronto, seguro que ves algo que te pueda servir."]
        self.dialogos_modista = ["Bienvenido a la tienda de Eva la modista...Wuan, que articulo de lujo necesitas?", "Nos han llegado las ultimas novedades como las bufandas de Ovejana, a las ovejas misteriosamente les atrae este accesorio..."]
        self.dialogos_pollo = ["Cococo! Escucha bien, te lo voy a decir, mi amor por las Jordans es algo que no puede huir, si quieres que camine junto a ti, en este lugar, necesitas comprender que es lo que quiero calzar.", "Con mis Jordan en mis patas, contigo voy a marchar.", "Dime Wuan, me has traido mi complemento favorito? Tengo muchas ganas de lucirlas por el corral."]
        self.dialogos_pollo_2 = ["Con Jordan en las garras, sere el gallo de las carreras, Gallina Daniel, ¡brillando como estrellas en las praderas! En la granja, sere el mas veloz de todas las bestias granjeras!,Y junto a Wuan, la granja salvare, en cada paso que de!"]
        self.dialogos_pollo_3 = ["Aun no tienes mis preciadas Jordan...ya se que estan caras pero sin mi no podras conseguirlo, tu veras Wuan, o Jordans o no hay trato."]
        self.dialogos_pollo_4 = ["Que paciencia hay que tener contigo Wuan, bueno, confio en que al menos las que me traeras seran una edicion limitada."]
        
        self.dialogos_oveja = ["Baa-baa! Yo soy Oscar, lanuda y noble oveja, para salvar tu granja, una peticion te dejo. Una bufanda de Ovejana, con nudos de esperanza, traeme esa prenda, y juntos tendremos bonanza. Con la bufanda al cuello, sere tu fiel aliado,te ayudare en tu granja, hasta que todo haya acabado.", "Asi que amigo del campo, ya sabes mi condicion,una bufanda para mi, y yo te doy mi devocion. Juntos enfrentaremos, el frio y la adversidad,y con bufanda en mano, la granja vamos a salvar.", "Me has traido mi preciada bufanda de Ovejana?"]
        self.dialogos_oveja_2 = ["Que bien me va a sentar esta bufanda!"]
        self.dialogos_oveja_3 = ["Corre Wuan, aunque sea una oveja me estoy muriendo de frio, necesito una bufanda al cuello para poder servirte como aliado."]
        self.dialogos_oveja_4 = ["Vaya...bueno no te preocupes Wuan, confiamos todo el pueblo de Villaverde en ti, seguro que seras capaz de conseguir cada uno de los retos, aqui te esperare."]
        self.dialogos_vaca = ["Moo-moo! Presta atencion, aqui te voy a contar, mis gustos son exclusivos! Si quieres que camine a tu lado, que te siga sin fallar, necesitas comprender lo que me hace deslumbrar.", "Mi estilo ha de resplandecer, con unas gafas Swarovski, me vas a enloquecer! Asi que si quieres mi amistad, si quieres mi devocion, trae esas gafas!", "Dime cielo, tienes unas gafas rechulonas por ahi que poder darme?"]
        self.dialogos_vaca_2 = ["Gracias cielo, ahora junto a ti desfilare, con estas gafas y nuestro esfuerzo salvaremos la granja. Puedes contar conmigo, Clara, como tu fiel aliada."]
        self.dialogos_vaca_3 = ["Aun no tienes las gafas cielo...vuelve cuando tengas algo mas de disposicion."]
        self.dialogos_vaca_4 = ["De acuerdo, cuando las traigas sere la vaca mas guapa y te podre ayudar."]
        self.dialogos_hermanos = ["Hermano Pablo, has visto a Wuan con determinacion, buscando soluciones para salvar nuestra situacion?", "Si, Manuel, lo he visto, con su mente inquieta y su corazon valiente, buscando formas de reconstruir nuestra granja y ser eficiente.", "Debemos unirnos a su noble labor, juntos, enfrentaremos cualquier dolor.", "Pero, Manuel, escucha lo que te digo, a veces, actuar solo es el mejor abrigo.", "Entiendo, Pablo, pero quiero colaborar, juntos, mas podemos lograr.", "Tu entusiasmo es loable, Manuel, no lo niego, pero confiemos en Wuan, el es nuestro fuego.", "Wuan, cuando salves la granja con ingenio y destreza, Don Diego dejara de ser un cascarrabias, vaya rareza!"]
        self.dialogos_llave_magistral = ["Nos has reclutado a todos, por eso hemos decidido darte la Llave Magistral, ponla a buen recaudo, la necesitaras."]
        self.dialogos_cabra = ["MEEEEEEE!!!"]

        dialogos = [
            self.dialogos_dondiego,self.dialogos_dondiego_2, self.dialogos_butanero, self.dialogos_butanero_2, self.dialogos_mercader,
            self.dialogos_mercader_3, self.dialogos_mercader_4, self.dialogos_mercader_5, self.dialogos_mercader_6,self.dialogos_mercader_7,
            self.dialogos_modista_3, self.dialogos_modista_4, self.dialogos_modista_5, self.dialogos_modista_6,
            self.dialogos_modista, self.dialogos_pollo, self.dialogos_pollo_2, self.dialogos_pollo_3,
            self.dialogos_pollo_4, self.dialogos_vaca, self.dialogos_oveja, self.dialogos_oveja_2,
            self.dialogos_oveja_3, self.dialogos_oveja_4, self.dialogos_hermanos, self.dialogos_vaca_2,
            self.dialogos_vaca_3, self.dialogos_vaca_4, self.dialogos_llave_magistral, self.dialogos_modista_7,
            self.dialogos_modista_8, self.dialogos_butanero_3, self.dialogos_butanero_4, self.dialogos_butanero_5,
            self.dialogos_butanero_6, self.dialogos_butanero_7,self.dialogos_cabra
        ]

        for lista_dialogos in dialogos:
                for i in range(len(lista_dialogos)):
                    lista_dialogos[i] = lista_dialogos[i] + self.marcador


    def dibujar_frases(self, texto_mostrado, inicio_texto_x, inicio_texto_y, max_ancho_linea=450, color_texto=None):

        palabras = texto_mostrado.split(' ')
        linea_actual = ""
        y_offset = 0
        self.caracter_especial_dibujado = False

        for palabra in palabras:
            prueba_linea = f"{linea_actual} {palabra}" if linea_actual else palabra
            prueba_superficie = self.fuente.render(prueba_linea, True, color_texto if color_texto else self.MARRON)
            prueba_ancho = prueba_superficie.get_width()

            if prueba_ancho <= max_ancho_linea:
                linea_actual = prueba_linea
            else:
                self.pantalla.blit(self.fuente.render(linea_actual, True, color_texto if color_texto else self.MARRON),
                                (inicio_texto_x, inicio_texto_y + y_offset))
                y_offset += 30
                linea_actual = palabra

        if linea_actual:
            self.pantalla.blit(self.fuente.render(linea_actual, True, color_texto if color_texto else self.MARRON),
                            (inicio_texto_x, inicio_texto_y + y_offset))
            if self.marcador in linea_actual:
              self.caracter_especial_dibujado = True


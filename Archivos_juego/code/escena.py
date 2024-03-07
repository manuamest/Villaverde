class Escena:
    def __init__(self, director):
        self.director = director
    
    def update(self, *args):
        # Enemigos, animales, sprites dinamicos
        raise NotImplemented("Tiene que implementar el metodo update.")
    
    def eventos(self, *args):
        # Mover jugador
        raise NotImplemented("Tiene que implementar el metodo eventos.")
    
    def dibujar(self, pantalla):
        # Camara
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
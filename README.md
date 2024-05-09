# Descripción del Videojuego
La ambientación de este juego se sitúa en un entorno rural destrozado, donde los jugadores tienen la oportunidad de sumergirse en la vida en una granja y su reconstrucción. El juego ofrece la posibilidad de realizar actividades agrícolas, que incluyen el cultivo de cultivos, la gestión de animales y la compra-venta de productos. Los jugadores pueden disfrutar de la gestión de su granja, experimentando con diferentes estrategias para alcanzar unos objetivos prefijados. El juego tiene un estilo pixel art muy colorido.

![Menu principal](https://github.com/manuamest/Villaverde/blob/main/menu.png)

# Mecánicas Implementadas
## Sistema de Tala
El jugador puede talar usando la tecla 'Espacio', tras haber seleccionado como herramienta la azada con la tecla 'Q'. Para talar un árbol es necesario golpearlo desde las distintas posiciones posibles hasta que este caiga.

## Sistema de Cultivo
Para cultivar, el jugador debe situarse en la zona cultivable indicada en el Nivel 2 y realizar todas las acciones situado justo encima de la porción de tierra en la que desea plantar. Primero se puede arar la tierra usando 'Espacio', tras haber seleccionado como herramienta la azada con la 'Q'. Posteriormente se puede usar la bolsa de semillas de trigo para plantar presionando 'F'. Finalmente, se puede regar usando 'Espacio', tras haber seleccionado como herramienta la regadera con la 'Q'.

## Sistema de Compra-Venta
Una vez el jugador alcanza el Nivel 2, desbloqueará las tiendas de Eva la modista y Xoel el mercader. El jugador puede hablar con Xoel el mercader para vender sus productos, tanto madera como trigo. Para ello, debe seleccionar mediante el uso de las flechas del teclado la cantidad que desea vender de un producto en concreto y confirmar con 'X'. El jugador también puede hablar con Eva la modista para comprar los distintos artículos necesarios para que los animales sean felices y regresen a la granja. Para ello, debe seleccionar mediante el uso de las flechas del teclado el artículo que desea comprar y confirmar con 'X'.

## Otras Interacciones
### Interacción con Carteles
Se puede interactuar con carteles si estás situado cerca de ellos presionando la tecla 'E'.

### Interacción con la Puerta de la Mazmorra
Cuando llegas al Nivel 3, debes usar la llave obtenida en el Nivel 2 para acceder a la mazmorra final.

## Puzle
Como reto final, el jugador debería resolver un puzle empleando el ratón para mover las piezas. Una vez ha conseguido ordenar las piezas el puzle se establecerá como completado y se abrirá la puerta, permitiendo al jugador acceder a la sala final y así poder rescatar a la cabra Fer.

# Instalación y Ejecución
Descarga el repositorio del juego.
Instala Python si aún no lo tienes instalado.
Instala las dependencias del juego
```
git clone git@github.com:manuamest/Villaverde.git
cd Villaverde
pip install -r requirements.txt
```
Ejecuta el juego ejecutando el archivo principal del juego con Python desde la ruta Archivos_juego: 
```
cd Archivos_juego
python code/main.py.
```

Para más detalles consultar el archivo [Memoria_CIIE](Memoria_CIIE.pdf)
¡Disfruta del juego y diviértete reconstruyendo la granja!

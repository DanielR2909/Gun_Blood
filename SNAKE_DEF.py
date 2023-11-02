import pygame
# Vector2 es como un arreglo para manejar mejor las posiciones y los comandos
from pygame.math import Vector2
import random

# Inicialización de Pygame
pygame.init()

#Marcador
score = 0
high_score = 0

# Dimensiones de la ventana
ANCHO = 720
ALTO = 480

# Cargar las imágenes de la serpiente, la manzana y la cabeza de la serpiente
SNAKE_BODY = pygame.transform.scale(pygame.image.load("snakebody.png"), (20, 20))
APPLE = pygame.transform.scale(pygame.image.load("manzana.png"), (20, 20))
SNAKE_HEAD = []
for x in range(1, 5):
    SNAKE_HEAD.append(pygame.transform.scale(pygame.image.load(f"SnakeHead{x}.png"), (20, 20)))

# Configuración de la ventana
WIN = pygame.display.set_mode((ANCHO, ALTO))
SCORE_TEXT = pygame.font.SysFont("Russo One", 15)

# Clase Snake (Serpiente)
class Snake:
    def __init__(self):
        self.body = [Vector2(20, 100), Vector2(20, 120), Vector2(20, 140)]  # Cuerpo inicial de la serpiente
        self.direction = Vector2(10, 0)  # Dirección inicial (arriba)
        self.add = False  # Indicador para agregar un segmento

    def draw(self):
        # Dibuja la serpiente en la ventana
        for bloque in self.body:
            WIN.blit(SNAKE_BODY, (bloque.x, bloque.y))

        # Dibuja la cabeza de la serpiente según su dirección
        if self.direction == Vector2(0, -20):
            WIN.blit(SNAKE_HEAD[0], (self.body[0].x, self.body[0].y))
        elif self.direction == Vector2(0, 20):
            WIN.blit(SNAKE_HEAD[2], (self.body[0].x, self.body[0].y))
        elif self.direction == Vector2(20, 0):
            WIN.blit(SNAKE_HEAD[1], (self.body[0].x, self.body[0].y))
        elif self.direction == Vector2(-20, 0):
            WIN.blit(SNAKE_HEAD[3], (self.body[0].x, self.body[0].y))

    def move(self):
        # Mueve la serpiente
        if self.add:
            body_copy = self.body
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.add = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def move_up(self):
        # Cambia la dirección de la serpiente hacia arriba
        self.direction = Vector2(0, -10)

    def move_down(self):
        # Cambia la dirección de la serpiente hacia abajo
        self.direction = Vector2(0, 10)

    def move_right(self):
        # Cambia la dirección de la serpiente hacia la derecha
        self.direction = Vector2(10, 0)

    def move_left(self):
        # Cambia la dirección de la serpiente hacia la izquierda
        self.direction = Vector2(-10, 0)

    def die(self):
        # Verifica si la serpiente ha chocado con los bordes de la ventana o consigo misma
        if self.body[0].x >= ANCHO + 20 or self.body[0].y >= ALTO + 20 or self.body[0].x <= -20 or self.body[0].y <= -20:
            return True
        for i in self.body[1:]:
            if self.body[0] == i:
                return True
        return False

# Clase Apple (Manzana)
class Apple:
    def __init__(self):
        self.generate()

    def draw(self):
        # Dibuja la manzana en la ventana
        WIN.blit(APPLE, (self.pos.x, self.pos.y))

    def generate(self):
        # Genera una nueva posición para la manzana
        self.x = random.randrange(0, ANCHO / 20)
        self.y = random.randrange(0, ALTO / 20)
        self.pos = Vector2(self.x * 20, self.y * 20)

    def check_collision(self, snake):
        # Verifica si la serpiente ha colisionado con la manzana
        if snake.body[0] == self.pos:
            self.generate()
            snake.add = True
            return True
        for bloque in snake.body[1:]:
            if self.pos == bloque:
                self.generate()
        return False


# Bucle principal
#ejecutando = True
#while ejecutando:
#    for evento in pygame.event.get():
#        if evento.type == pygame.QUIT:
#            ejecutando = False

    # Limpiar la pantalla
#    WIN.fill((255, 255, 255))

    # Dibujar el texto
#    texto = pygame.font.SysFont(f"Score: {score}     High Score: {high_score}", True, 0, 0, 0)
#    WIN.blit(texto, (50, 80))

# Función principal del juego
def main():
    snake = Snake()
    apple = Apple()
    score = 0
    fps = pygame.time.Clock()
    
#    ejecutando = True

    while True:
        fps.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
#                ejecutando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction.y != 20:
                    snake.move_up()
                if event.key == pygame.K_DOWN and snake.direction.y != -20:
                    snake.move_down()
                if event.key == pygame.K_RIGHT and snake.direction.x != -20:
                    snake.move_right()
                if event.key == pygame.K_LEFT and snake.direction.x != 20:
                    snake.move_left()
                    
    

        WIN.fill((51, 0, 102))  # Llena la ventana con un color de fondo
        snake.draw()  # Dibuja la serpiente
        apple.draw()  # Dibuja la manzana
        snake.move()  # Mueve la serpiente
        if apple.check_collision(snake):
            score += 1  # Aumenta la puntuación cuando la serpiente come la manzana
        if snake.die():
            mensaje = pygame.font.SysFont('GAME OVER!', True, (255, 255, 255))
            WIN.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2 - mensaje.get_height() // 2))
            print('!Game Over¡')
            
            pygame.display.flip()
            pygame.time.wait(8000)
            pygame.quit()
            
            quit() # Sale del juego si la serpiente colisiona con los bordes o consigo misma
            
            
            
        text = SCORE_TEXT.render(f"Score: {score}", 1, (255, 255, 255))
        WIN.blit(text, (ANCHO - text.get_width() - 20, 20))  # Muestra la puntuación en la ventana
        pygame.display.update()  # Actualiza la ventana

main()
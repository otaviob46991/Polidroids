from pygame.math import Vector2 # Importa o módulo math do pygame
from pygame.transform import rotozoom # Importa o método rotozoom do módulo transform do pygame
from utils import get_random_velocity, load_sprite, wrap_position # Importa os métodos do módulo utils

UP = Vector2(0, -1) # Define a direção para cima

class GameObject: # Classe base para todos os objetos do jogo
    def __init__(self, position, sprite, velocity): # Método construtor
        self.position = Vector2(position) # Define a posição do objeto
        self.sprite = sprite # Define a imagem do objeto
        self.radius = sprite.get_width() / 2 # Define o raio do objeto
        self.velocity = Vector2(velocity) # Define a velocidade do objeto

    def draw(self, surface): # Método desenha o objeto na tela
        blit_position = self.position - Vector2(self.radius) # Define a posição do objeto
        surface.blit(self.sprite, blit_position) # Desenha o objeto na tela
 
    def move(self, surface): # Método move o objeto
        self.position = wrap_position(self.position + self.velocity, surface) # Calcula a nova posição do objeto

    def collides_with(self, other_obj): # Método verifica se o objeto colidiu com outro objeto
        distance = self.position.distance_to(other_obj.position) # Calcula a distância entre os objetos
        return distance < self.radius + other_obj.radius # Retorna se a distância é menor que a soma dos raios
    
class Spaceship(GameObject): # Classe para a nave
    MANEUVERABILITY = 3 # Define a manobrabilidade da nave
    ACCELERATION = 0.25 # Define a aceleração da nave
    BULLET_SPEED = 3 # Define a velocidade do tiro
    
    def __init__(self, position, create_bullet_callback): # Método construtor
        self.create_bullet_callback = create_bullet_callback # Define o método para criar um tiro
        self.direction = Vector2(UP) # Define a direção da nave
        super().__init__(position, load_sprite("spaceship", 0.4), Vector2(0)) # Chama o construtor da classe pai
        
    def rotate(self, clockwise=True): # Método rotaciona a nave
        sign = 1 if clockwise else -1 # Define o sinal da rotação
        angle = self.MANEUVERABILITY * sign # Calcula o ângulo da rotação
        self.direction.rotate_ip(angle) # Rotaciona a direção da nave
        
    def accelerate(self): # Método acelera a nave
        self.velocity += self.direction * self.ACCELERATION # Atualiza a velocidade da nave
        
    def draw(self, surface): # Método desenha a nave na tela
        angle = self.direction.angle_to(UP) # Calcula o ângulo da direção da nave
        rotated_surface = rotozoom(self.sprite, angle, 1.0) # Rotaciona a imagem da nave
        rotated_surface_size = Vector2(rotated_surface.get_size()) # Calcula o tamanho da imagem rotacionada
        blit_position = self.position - rotated_surface_size * 0.5 # Define a posição da imagem rotacionada
        surface.blit(rotated_surface, blit_position) # Desenha a imagem rotacionada na tela
        
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED # Calcula a velocidade do tiro
        bullet = Bullet(self.position, bullet_velocity) # Cria um tiro
        self.create_bullet_callback(bullet) # Chama o método para criar um tiro
        
class Asteroids(GameObject): # Classe para os asteroides
    def __init__(self, position, create_asteroid_callback, size=4): # Método construtor
        self.create_asteroid_callback = create_asteroid_callback  # Recursão para a quebra de asteroid
        self.size = size  # "Tamanho"

        size_scale = {
            4:1,
            3:0.75,
            2:0.5,
            1:0.25
        }  # Escala em relação ao tamanho
        scale = size_scale[self.size]
        
        sprite_size = {
            4:"hexagoid",
            3:"pentagoid",
            2:"quadroid",
            1:"trianguloid"
        }  # Formato em relação ao tamanho
        sprite_img = sprite_size[size]

        sprite = rotozoom(load_sprite(sprite_img, 0.5), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3)) # Chama o construtor da classe pai
    
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroids(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)
        
class Bullet(GameObject): # Classe para os tiros
    def __init__(self, position, velocity): # Método construtor
        super().__init__(position, load_sprite("bullet_1", 0.1), velocity) # Chama o construtor da classe pai
        
    def move(self, surface): # Método move o tiro
        self.position = self.position + self.velocity # Calcula a nova posição do tiro
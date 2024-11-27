import pgzrun  # Importa o framework PgZero
import os  # Para definir a posição da janela no sistema operacional
from pygame import Rect  # Importa a classe Rect da biblioteca Pygame
import random  # Importa a biblioteca random para movimentação aleatória

# Centraliza a janela no centro do monitor
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Cria o ator e define sua posição
player_000 = Actor('player_000')
player_000.pos = 500, 410  # Define a posição do ator

# Define a largura e a altura da janela
WIDTH = 1000
HEIGHT = 562

# Define uma variável chao_y com a altura do chão
chao_y = HEIGHT - 130  # A altura do chão a 130 pixels do fundo

# Define as plataformas com suas posições e tamanhos
plataformas = [
    Rect(200, chao_y - 100, 600, 30),  # Plataforma 
    Rect(0, chao_y - 200, 220, 30),    # Plataforma 
    Rect(780, chao_y - 200, 220, 30),  # Plataforma 
    Rect(200, chao_y - 300, 600, 30)    # Plataforma 
]

# Variáveis de controle de pulo
jumping = False  # Indica se o jogador está pulando
velocity_y = 0  # Velocidade vertical do jogador
gravity = 1  # Força da gravidade
jump_height = 15  # Altura do pulo

def draw():
    screen.clear()  # Limpa a tela a cada quadro
    screen.blit("background", (0, 0))  # Exibe a imagem de fundo
    screen.blit("chao", (0, chao_y))  # Exibe a imagem do chão na posição (0, chao_y)

    # Desenha as plataformas
    for plataforma in plataformas:
        screen.draw.filled_rect(plataforma, "green")  # Preenche a plataforma de verde
    
    player_000.draw()  # Desenha o jogador

def update():
    global jumping, velocity_y

    # Movimentação das plataformas
    for plataforma in plataformas:
        # Move a plataforma para a esquerda de forma aleatória
        plataforma.x -= random.randint(1, 3)  # Move entre 1 e 3 pixels para a esquerda

        # Se a plataforma sair da tela, reposiciona-a para a direita
        if plataforma.x < -plataforma.width:
            plataforma.x = WIDTH + random.randint(0, 300)  # Reposiciona aleatoriamente para a direita

    # Movimentação do jogador
    if keyboard.right:  # Se a tecla direita estiver pressionada
        player_000.x += 5  # Move o jogador para a direita

    if keyboard.left:  # Se a tecla esquerda estiver pressionada
        player_000.x -= 5  # Move o jogador para a esquerda

    # Restringe o movimento do jogador para que ele permaneça na tela
    player_000.x = max(0, min(player_000.x, WIDTH - player_000.width))  # Mantém o jogador dentro da largura da tela

    # Lógica de pulo
    if not jumping and keyboard.space:  # Se não está pulando e a tecla de espaço é pressionada
        # Verifica se o jogador está em cima de alguma plataforma
        for plataforma in plataformas:
            if player_000.colliderect(plataforma):  # Verifica colisão com a plataforma
                jumping = True  # Inicia o pulo
                velocity_y = -jump_height  # Define a velocidade vertical negativa para o pulo
                break  # Sai do loop após o primeiro pulo

    if jumping:  # Se está pulando
        player_000.y += velocity_y  # Move o jogador verticalmente

        # Aplica a gravidade
        velocity_y += gravity  

        # Verifica se o jogador atingiu o chão ou uma plataforma
        if player_000.y >= chao_y - player_000.height:  # Se atingir o chão
            player_000.y = chao_y - player_000.height  # Coloca o jogador no chão
            jumping = False  # O jogador não está mais pulando
            velocity_y = 0  # Reseta a velocidade vertical
        else:
            # Verifica se o jogador colidiu com alguma plataforma
            for plataforma in plataformas:
                if player_000.colliderect(plataforma):
                    player_000.y = plataforma.top - player_000.height  # Coloca o jogador em cima da plataforma
                    jumping = False  # O jogador não está mais pulando
                    velocity_y = 0  # Reseta a velocidade vertical
                    break  # Sai do loop após a primeira colisão

pgzrun.go()  # Inicia o jogo    

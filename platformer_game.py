import os
import pgzrun
import pygame
import random

# Função para carregar as imagens do herói
def load_hero_images():
    images = []
    hero_path = os.path.join('images', 'hero', 'walk')

    if not os.path.exists(hero_path):
        print(f"Pasta não encontrada: {hero_path}")
        return images

    for filename in sorted(os.listdir(hero_path)):
        if filename.endswith('.png'):
            img_path = os.path.join(hero_path, filename)
            images.append(pygame.image.load(img_path).convert_alpha())
            print(f"Imagem carregada: {img_path}")

    return images

# Função para carregar as imagens de ataque
def load_attack_images():
    images = []
    attack_path = os.path.join('images', 'hero', 'attack_1')

    if not os.path.exists(attack_path):
        print(f"Pasta não encontrada: {attack_path}")
        return images

    for filename in sorted(os.listdir(attack_path)):
        if filename.endswith('.png'):
            img_path = os.path.join(attack_path, filename)
            images.append(pygame.image.load(img_path).convert_alpha())
            print(f"Imagem de ataque carregada: {img_path}")

    return images

# Função para carregar as imagens do inimigo
def load_enemy_images():
    images = []
    enemy_path = os.path.join('images', 'enemy', 'walk')

    if not os.path.exists(enemy_path):
        print(f"Pasta não encontrada: {enemy_path}")
        return images

    for filename in sorted(os.listdir(enemy_path)):
        if filename.endswith('.png'):
            img_path = os.path.join(enemy_path, filename)
            images.append(pygame.image.load(img_path).convert_alpha())
            print(f"Imagem de inimigo carregada: {img_path}")

    return images

# Inicializa variáveis
hero_images = load_hero_images()  # Carrega as imagens de caminhada
attack_images = load_attack_images()  # Carrega as imagens de ataque
enemy_images = load_enemy_images()  # Carrega as imagens do inimigo

# Verifica se as imagens foram carregadas corretamente
if not hero_images:
    print("Nenhuma imagem de herói foi carregada. Verifique o diretório e os arquivos.")
if not enemy_images:
    print("Nenhuma imagem de inimigo foi carregada. Verifique o diretório e os arquivos.")

# Variáveis do menu
game_started = False
sound_enabled = True  # Controle de som

# Posições e estados iniciais
hero_pos = [100, 450]  # Posição inicial do herói
hero_frame = 0  # Índice do frame atual
hero_speed = 5  # Velocidade do herói
is_attacking = False  # Estado de ataque
attack_frame = 0  # Índice do frame de ataque
attack_speed = 10  # Define a quantidade de frames entre cada atualização de ataque
attack_counter = 0  # Contador para controlar a atualização do ataque

# Posições e movimentos do inimigo
enemy_pos = [random.randint(0, 800 - 50), random.randint(0, 600 - 50)]  # Posição inicial aleatória do inimigo
enemy_frame = 0  # Índice do frame atual do inimigo
enemy_speed = 2  # Velocidade do inimigo
enemy_direction = [random.choice([-1, 1]), random.choice([-1, 1])]  # Direção aleatória do movimento do inimigo
enemy_frame_counter = 0  # Contador para animar o inimigo

# Função para gerar uma nova posição para o inimigo
def respawn_enemy():
    return [random.randint(0, 800 - 50), random.randint(0, 600 - 50)]  # Considera o tamanho do inimigo

# Função de atualização do jogo
def update():
    global hero_frame, hero_pos, is_attacking, attack_frame, attack_counter
    global enemy_pos, enemy_frame, enemy_direction, enemy_frame_counter, sound_enabled

    if game_started:
        # Movimentação do herói
        if not is_attacking:
            if keyboard.left:
                hero_pos[0] -= hero_speed  # Move para a esquerda
                hero_frame = (hero_frame + 1) % len(hero_images)
            elif keyboard.right:
                hero_pos[0] += hero_speed  # Move para a direita
                hero_frame = (hero_frame + 1) % len(hero_images)
            if keyboard.up:
                hero_pos[1] -= hero_speed  # Move para cima
                hero_frame = (hero_frame + 1) % len(hero_images)
            elif keyboard.down:
                hero_pos[1] += hero_speed  # Move para baixo
                hero_frame = (hero_frame + 1) % len(hero_images)

            # Limita a movimentação do herói aos limites da tela
            hero_pos[0] = max(0, min(hero_pos[0], 800 - hero_images[0].get_width()))
            hero_pos[1] = max(0, min(hero_pos[1], 600 - hero_images[0].get_height()))

            # Verifica se a tecla de ataque é pressionada
            if keyboard.space:  # Aqui, o ataque é ativado com a tecla de espaço
                is_attacking = True  # Ativa o estado de ataque
                attack_frame = 0  # Reinicia o frame de ataque
                attack_counter = 0  # Reinicia o contador
                play_attack_sound()  # Reproduz som de ataque

        # Atualiza a animação de ataque
        if is_attacking:
            attack_counter += 1  # Incrementa o contador
            if attack_counter >= attack_speed:  # Se atingiu a velocidade desejada
                attack_frame += 1  # Avança para o próximo frame de ataque
                attack_counter = 0  # Reinicia o contador
            if attack_frame >= len(attack_images):  # Se a animação de ataque terminar
                is_attacking = False  # Retorna ao estado normal

        # Movimentação do inimigo
        enemy_pos[0] += enemy_speed * enemy_direction[0]  # Move o inimigo na direção x
        enemy_pos[1] += enemy_speed * enemy_direction[1]  # Move o inimigo na direção y

        # Verifica se o inimigo atingiu a borda da tela e inverte a direção
        if enemy_pos[0] <= 0 or enemy_pos[0] >= 800 - enemy_images[0].get_width():
            enemy_direction[0] *= -1  # Inverte a direção horizontal
        if enemy_pos[1] <= 0 or enemy_pos[1] >= 600 - enemy_images[0].get_height():
            enemy_direction[1] *= -1  # Inverte a direção vertical

        # Atualiza a animação do inimigo
        enemy_frame_counter += 1
        if enemy_frame_counter >= 5:  # Ajuste o valor para mudar a velocidade da animação
            enemy_frame = (enemy_frame + 1) % len(enemy_images)
            enemy_frame_counter = 0  # Reinicia o contador de frames do inimigo

        # Verifica colisão entre o herói e o inimigo
        if is_attacking and (hero_pos[0] < enemy_pos[0] + enemy_images[0].get_width() and
                             hero_pos[0] + hero_images[0].get_width() > enemy_pos[0] and
                             hero_pos[1] < enemy_pos[1] + enemy_images[0].get_height() and
                             hero_pos[1] + hero_images[0].get_height() > enemy_pos[1]):
            enemy_pos[:] = respawn_enemy()  # Respawn do inimigo

# Função para reproduzir som de ataque
def play_attack_sound():
    if sound_enabled:
        attack_sound = pygame.mixer.Sound("sounds/attack.wav")  # Ajuste o caminho para o seu arquivo de som
        attack_sound.play()

# Função de desenho do jogo
def draw():
    screen.clear()  # Limpa a tela
    if not game_started:  # Se o jogo ainda não começou, desenha o menu
        draw_menu()
    else:  # Se o jogo começou, desenha o jogo
        screen.blit('background', (0, 0))  # Desenha o fundo
        if is_attacking and attack_images:  # Verifica se está atacando
            screen.blit(attack_images[attack_frame], hero_pos)  # Desenha o herói com a animação de ataque na posição atual
        elif hero_images:  # Se não está atacando, desenha o herói
            screen.blit(hero_images[hero_frame], hero_pos)

        # Desenha o inimigo
        if enemy_images:
            screen.blit(enemy_images[enemy_frame], enemy_pos)  # Desenha o inimigo na posição atual

# Função para desenhar o menu
def draw_menu():
    screen.clear()
    screen.draw.text("Pressione 'Enter' para iniciar o jogo", center=(400, 300), fontsize=40, color="white")
    screen.draw.text("Pressione 'M' para alternar som", center=(400, 350), fontsize=30, color="white")

# Função que gerencia eventos do teclado
def on_key_down(key):
    global game_started, sound_enabled
    if key == keys.RETURN:  # Inicia o jogo
        game_started = True
    elif key == keys.M:  # Alterna o som
        sound_enabled = not sound_enabled  # Alterna o estado do som
        print("Som habilitado" if sound_enabled else "Som desabilitado")

# Inicializa o jogo
pgzrun.go()

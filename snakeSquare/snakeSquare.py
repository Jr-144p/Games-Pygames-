import pygame
import time
import random
import sys

# Inicializa o pygame
pygame.init()

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 200, 0)
vermelho = (200, 0, 0)
azul = (0, 0, 200)  # Cor para as bordas
cinza = (100, 100, 100)  # Cor para o texto da pontuação

# Dimensões da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake Game 🐍")

# Espessura da borda
espessura_borda = 5
# Área jogável
area_jogavel_x = espessura_borda
area_jogavel_y = espessura_borda
area_jogavel_largura = largura - 2 * espessura_borda
area_jogavel_altura = altura - 2 * espessura_borda
# Clock para controlar FPS
clock = pygame.time.Clock()

# Tamanho do bloco da cobra
tamanho_bloco = 20

# Fonte
fonte = pygame.font.SysFont("arial", 25)
fonte_pontuacao = pygame.font.SysFont("arial", 20)

def mensagem(msg, cor):
    texto = fonte.render(msg, True, cor)
    tela.blit(texto, [largura / 6, altura / 3])

def mostrar_pontuacao(pontos):
    texto = fonte_pontuacao.render(f"Pontuação: {pontos}", True, vermelho)
    tela.blit(texto, [10, 10])

def desenhar_bordas():
    # Borda superior
    pygame.draw.rect(tela, preto, [0, 0, largura, espessura_borda])
    # Borda inferior
    pygame.draw.rect(tela, preto, [0, altura - espessura_borda, largura, espessura_borda])
    # Borda esquerda
    pygame.draw.rect(tela, preto, [0, 0, espessura_borda, altura])
    # Borda direita
    pygame.draw.rect(tela, preto, [largura - espessura_borda, 0, espessura_borda, altura])

def menu_fim_jogo(pontuacao):
    game_close = True
    while game_close:
        tela.fill(preto)
        # Primeira mensagem
        texto1 = fonte.render(f"Você perdeu! Pontuação: {pontuacao}", True, vermelho)
        tela.blit(texto1, [largura / 6, altura / 3])
        
        # Segunda mensagem (posicionada abaixo da primeira)
        texto2 = fonte.render("Pressione C para jogar de novo ou Q para sair", True, vermelho)
        tela.blit(texto2, [largura / 6, altura / 3 + 40])  # +40 para posicionar abaixo
        
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_c:
                    jogo()  # Reinicia o jogo

def jogo():
    game_over = False
    game_close = False

    # Posição inicial da cobra (ajustada para a área jogável)
    x = largura / 2
    y = altura / 2
    dx = 0
    dy = 0

    # Variáveis para controlar a direção atual
    direcao_atual = ""
    # Corpo da cobra
    cobra = []
    comprimento = 1

    # Pontuação inicial
    pontuacao = 0
    # Velocidade inicial
    velocidade = 10

    # Comida inicial (ajustada para a área jogável)
    comida_x = round(random.randrange(area_jogavel_x, area_jogavel_x + area_jogavel_largura - tamanho_bloco) / 20.0) * 20.0
    comida_y = round(random.randrange(area_jogavel_y, area_jogavel_y + area_jogavel_altura - tamanho_bloco) / 20.0) * 20.0

    while not game_over:

        while game_close:
            menu_fim_jogo(pontuacao)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and direcao_atual != "DIREITA":
                    dx = -tamanho_bloco
                    dy = 0
                    direcao_atual = "ESQUERDA"
                elif evento.key == pygame.K_RIGHT and direcao_atual != "ESQUERDA":
                    dx = tamanho_bloco
                    dy = 0
                    direcao_atual = "DIREITA"
                elif evento.key == pygame.K_UP and direcao_atual != "BAIXO":
                    dy = -tamanho_bloco
                    dx = 0
                    direcao_atual = "CIMA"
                elif evento.key == pygame.K_DOWN and direcao_atual != "CIMA":
                    dy = tamanho_bloco
                    dx = 0
                    direcao_atual = "BAIXO"

        # Atualiza posição da cobra
        x += dx
        y += dy

        # Verifica se bateu na borda (ajustado para as novas bordas)
        if x < area_jogavel_x or x >= area_jogavel_x + area_jogavel_largura or y < area_jogavel_y or y >= area_jogavel_y + area_jogavel_altura:
            game_close = True

        tela.fill(branco)
        # Desenha as bordas
        desenhar_bordas()
        pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        cabeca = [x, y]
        cobra.append(cabeca)

        if len(cobra) > comprimento:
            del cobra[0]

        # Se bateu em si mesma
        for parte in cobra[:-1]:
            if parte == cabeca:
                game_close = True

        # Desenha a cobra
        for bloco in cobra:
            pygame.draw.rect(tela, preto, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

        # Mostra a pontuação
        mostrar_pontuacao(pontuacao)
        pygame.display.update()

        # Se comeu a comida
        if x == comida_x and y == comida_y:
            # Nova posição da comida (ajustada para a área jogável)
            comida_x = round(random.randrange(area_jogavel_x, area_jogavel_x + area_jogavel_largura - tamanho_bloco) / 20.0) * 20.0
            comida_y = round(random.randrange(area_jogavel_y, area_jogavel_y + area_jogavel_altura - tamanho_bloco) / 20.0) * 20.0
            comprimento += 1
            pontuacao += 10  # Aumenta a pontuação em 10 pontos a cada comida
            velocidade += 1  #  aumenta a velocidade a cada comida

        clock.tick(velocidade)

    pygame.quit()
    quit()

jogo()

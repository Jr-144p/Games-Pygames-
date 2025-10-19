import pygame
import random

# Inicializa o pygame
pygame.init()

# Dimensões da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong 🏓")

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
azul = (0, 0, 255)

# Raquetes
raquete_largura = 15
raquete_altura = 125

# Bola
bola_raio = 10

# Velocidade
velocidade_raquete = 7
velocidade_inicial = 5   # velocidade inicial
velocidade_bola = velocidade_inicial
velocidade_max = velocidade_inicial * 1.8  # limite: +80%

# Fonte
fonte = pygame.font.SysFont("arial", 36)


def jogo():
    global velocidade_bola

    # Posições iniciais
    raquete1_y = altura // 2 - raquete_altura // 2
    raquete2_y = altura // 2 - raquete_altura // 2
    bola_x = largura // 2
    bola_y = altura // 2

    # Direção inicial da bola
    bola_dx = random.choice([-velocidade_bola, velocidade_bola])
    bola_dy = random.choice([-velocidade_bola, velocidade_bola])

    # Placar
    pontos1 = 0
    pontos2 = 0

    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Controles das raquetes
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and raquete1_y > 0:
            raquete1_y -= velocidade_raquete
        if teclas[pygame.K_s] and raquete1_y < altura - raquete_altura:
            raquete1_y += velocidade_raquete
        if teclas[pygame.K_UP] and raquete2_y > 0:
            raquete2_y -= velocidade_raquete
        if teclas[pygame.K_DOWN] and raquete2_y < altura - raquete_altura:
            raquete2_y += velocidade_raquete

        # Movimento da bola
        bola_x += bola_dx
        bola_y += bola_dy

        # Colisão com o topo e base
        if bola_y - bola_raio <= 0 or bola_y + bola_raio >= altura:
            bola_dy *= -1

        # Colisão com raquetes
        if (bola_x - bola_raio <= raquete_largura and
                raquete1_y < bola_y < raquete1_y + raquete_altura):
            bola_dx *= -1

        if (bola_x + bola_raio >= largura - raquete_largura and
                raquete2_y < bola_y < raquete2_y + raquete_altura):
            bola_dx *= -1

        # Pontuação
        if bola_x < 0:  # ponto do jogador 2
            pontos2 += 1
            if velocidade_bola < velocidade_max:  # só acelera até +80%
                velocidade_bola = min(velocidade_bola * 1.1, velocidade_max)
            bola_x = largura // 2
            bola_y = altura // 2
            bola_dx = random.choice([-velocidade_bola, velocidade_bola])
            bola_dy = random.choice([-velocidade_bola, velocidade_bola])

        if bola_x > largura:  # ponto do jogador 1
            pontos1 += 1
            if velocidade_bola < velocidade_max:  # só acelera até +80%
                velocidade_bola = min(velocidade_bola * 1.1, velocidade_max)
            bola_x = largura // 2
            bola_y = altura // 2
            bola_dx = random.choice([-velocidade_bola, velocidade_bola])
            bola_dy = random.choice([-velocidade_bola, velocidade_bola])

        # Desenho da tela
        tela.fill(preto)

        pygame.draw.rect(tela, branco, (0, raquete1_y,
                         raquete_largura, raquete_altura))
        pygame.draw.rect(tela, vermelho, (0, raquete1_y,
                         raquete_largura, raquete_altura))
        pygame.draw.rect(tela, azul, (largura - raquete_largura,
                         raquete2_y, raquete_largura, raquete_altura))
        pygame.draw.circle(tela, branco, (bola_x, bola_y), bola_raio)
        pygame.draw.aaline(tela, branco, (largura // 2, 0),
                           (largura // 2, altura))

        # Placar
        texto = fonte.render(f"{pontos1}   {pontos2}", True, branco)
        tela.blit(texto, (largura // 2 - texto.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


jogo()

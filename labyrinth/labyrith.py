import pygame
import sys

# Inicializa o pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Tamanho da tela e dos blocos
largura, altura = 600, 600
tamanho_bloco = 40
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Labirinto 🧩")

# Fonte
fonte = pygame.font.SysFont("arial", 35)

# Labirinto representado por matriz (1 = parede, 0 = caminho, 2 = saída)
labirinto = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,0,1,0,1,1],
    [1,0,1,0,0,0,0,0,0,1,0,1,0,0,1],
    [1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,1,0,1,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Posição inicial do jogador
jogador_x, jogador_y = 1, 1

def desenhar_labirinto():
    for y, linha in enumerate(labirinto):
        for x, bloco in enumerate(linha):
            if bloco == 1:
                pygame.draw.rect(tela, PRETO, (x*tamanho_bloco, y*tamanho_bloco, tamanho_bloco, tamanho_bloco))
            elif bloco == 2:
                pygame.draw.rect(tela, VERDE, (x*tamanho_bloco, y*tamanho_bloco, tamanho_bloco, tamanho_bloco))

def mensagem(texto):
    txt = fonte.render(texto, True, VERMELHO)
    tela.blit(txt, (largura//2 - txt.get_width()//2, altura//2 - txt.get_height()//2))
    pygame.display.update()
    pygame.time.wait(3000)

def jogo():
    global jogador_x, jogador_y
    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                novo_x, novo_y = jogador_x, jogador_y
                if evento.key == pygame.K_LEFT:
                    novo_x -= 1
                elif evento.key == pygame.K_RIGHT:
                    novo_x += 1
                elif evento.key == pygame.K_UP:
                    novo_y -= 1
                elif evento.key == pygame.K_DOWN:
                    novo_y += 1

                # Verifica se a nova posição não é parede
                if labirinto[novo_y][novo_x] != 1:
                    jogador_x, jogador_y = novo_x, novo_y

        # Verifica vitória
        if labirinto[jogador_y][jogador_x] == 2:
            tela.fill(BRANCO)
            mensagem("🎉 Você venceu!")
            rodando = False

        # Desenha
        tela.fill(BRANCO)
        desenhar_labirinto()
        pygame.draw.rect(tela, VERMELHO, (jogador_x*tamanho_bloco, jogador_y*tamanho_bloco, tamanho_bloco, tamanho_bloco))
        pygame.display.update()
        clock.tick(10)


jogo()

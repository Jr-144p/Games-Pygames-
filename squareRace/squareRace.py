import pygame
import random
import sys

# Inicialização
pygame.init()

# Configurações da tela
largura = 600
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Corrida de Quadrados 🏎️")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
VERDE = (0, 200, 0)
CINZA_PISTA = (70, 70, 70) # Um cinza um pouco mais escuro para a pista

# Fonte
fonte = pygame.font.SysFont("Arial", 30)

# Relógio
clock = pygame.time.Clock()
FPS = 60

carro01_img = pygame.image.load("carro001.png")
carro01_img = pygame.transform.scale(carro01_img, (70, 150))
largura_carro = 60
altura_carro = 150
pos_x = largura // 2 - largura_carro // 2
pos_y = altura - altura_carro - 10
velocidade_lateral = 7

# Obstáculos
carro02_img = pygame.image.load("carro002.png")
carro02_img = pygame.transform.scale(carro02_img, (70, 150))
largura_obst = 60
altura_obst = 150
obstaculos = []
velocidade_obst = 10
frequencia_obst = 35 # Aumentar o fluxo de obstáculos (diminuir o número de frames)

# Pista
largura_pista = largura - 150 # <<-- ALTERAÇÃO AQUI: Pista mais estreita
margem_pista = (largura - largura_pista) // 2
largura_linha_central = 5
altura_linha_central = 40
espacamento_linha_central = 30

# Pontuação
pontos = 0

# Tela inicial
def tela_inicial():
    tela.fill(VERDE) # Fundo verde para a tela inicial
    # Desenha a pista no centro da tela inicial
    pygame.draw.rect(tela, CINZA_PISTA, (margem_pista, 0, largura_pista, altura))
    texto = fonte.render("Pressione ESPAÇO para começar", True, BRANCO)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - 20))
    pygame.display.update()

# Tela de Game Over
def tela_game_over(pontos):
    tela.fill(VERDE) # Fundo verde para a tela de game over
    # Desenha a pista no centro da tela de game over
    pygame.draw.rect(tela, CINZA_PISTA, (margem_pista, 0, largura_pista, altura))
    texto1 = fonte.render("Game Over!", True, VERMELHO)
    texto2 = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    texto3 = fonte.render("Pressione ESPAÇO para jogar novamente", True, BRANCO)
    tela.blit(texto1, (largura // 2 - texto1.get_width() // 2, altura // 2 - 60))
    tela.blit(texto2, (largura // 2 - texto2.get_width() // 2, altura // 2 - 20))
    tela.blit(texto3, (largura // 2 - texto3.get_width() // 2, altura // 2 + 20))
    pygame.display.update()

# Função principal
def jogo():
    global pos_x, pos_y, obstaculos, velocidade_obst, pontos

    rodando = True
    jogo_iniciado = False

    while rodando:
        # Inicialização do jogo
        pos_x = largura // 2 - largura_carro // 2
        obstaculos = []
        velocidade_obst = 4  # Velocidade inicial menor
        pontos = 0
        frame_count = 0
        ultimo_obst_y = -altura_obst  # Para controlar sobreposição vertical

        while True:
            tela.fill(VERDE) # Fundo verde para as laterais (gramado)
            # Desenha a pista
            pygame.draw.rect(tela, CINZA_PISTA, (margem_pista, 0, largura_pista, altura))

            frame_count += 1

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        if not jogo_iniciado:
                            jogo_iniciado = True

            if not jogo_iniciado:
                tela_inicial()
                continue

            # Movimentação do jogador
            keys = pygame.key.get_pressed()
            # O jogador agora está restrito à largura da pista
            if keys[pygame.K_LEFT] and pos_x > margem_pista:
                pos_x -= velocidade_lateral
            if keys[pygame.K_RIGHT] and pos_x < largura - largura_carro - margem_pista:
                pos_x += velocidade_lateral

            # Desenhar linhas centrais em movimento suave
            offset_linha = (frame_count * velocidade_obst) % (altura_linha_central + espacamento_linha_central)
            for i in range(-altura_linha_central, altura, altura_linha_central + espacamento_linha_central):
                y_linha = i + offset_linha
                pygame.draw.rect(tela, BRANCO, (largura // 2 - largura_linha_central // 2, y_linha, largura_linha_central, altura_linha_central))

            # Criar obstáculos apenas se o último estiver suficientemente distante
            if len(obstaculos) == 0 or (obstaculos[-1][1] > altura_obst + 120):
                obst_x = random.randint(margem_pista, largura - largura_obst - margem_pista)
                obstaculos.append([obst_x, -altura_obst])

            # Atualizar obstáculos
            for obst in obstaculos:
                obst[1] += velocidade_obst

            # Remover obstáculos que saíram da tela e marcar ponto
            obstaculos_restantes = []
            for obst in obstaculos:
                if obst[1] < altura:
                    obstaculos_restantes.append(obst)
                else:
                    pontos += 1  # Marca ponto ao passar por obstáculo
            obstaculos = obstaculos_restantes

            # Aumentar velocidade gradativamente de forma suave
            velocidade_obst = 4 + pontos * 0.10  # Começa em 4, aumenta suavemente
            velocidade_obst = min(velocidade_obst, 18)  # Limite máximo para não ficar impossível

            # Desenhar jogador (sprite)
            tela.blit(carro01_img, (pos_x, pos_y))
            hitbox_jogador = pygame.Rect(pos_x, pos_y, largura_carro, altura_carro)

            # Desenhar obstáculos (sprite)
            hitboxes_obst = []
            for obst in obstaculos:
                tela.blit(carro02_img, (obst[0], obst[1]))
                hitboxes_obst.append(pygame.Rect(obst[0], obst[1], largura_obst, altura_obst))

            # Mostrar pontuação
            texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)
            tela.blit(texto, (10, 10))

            # Dica de controles nos primeiros segundos
            if pontos < 5:
                dica = fonte.render("Use ← e → para mover", True, BRANCO)
                tela.blit(dica, (largura // 2 - dica.get_width() // 2, altura - 50))

            # Verificar colisão usando hitbox igual ao sprite
            colisao = False
            for hitbox_obst in hitboxes_obst:
                if hitbox_jogador.colliderect(hitbox_obst):
                    colisao = True
                    break

            if colisao:
                tela_game_over(pontos)
                esperando = True
                while esperando:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                            esperando = False
                            jogo_iniciado = False
                break

            pygame.display.update()
            clock.tick(FPS)

# Iniciar jogo
jogo()

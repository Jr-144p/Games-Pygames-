import turtle
import random
import time

# Configuração da tela
wn = turtle.Screen()
wn.title("Jogo Pega-Pega 🐢")
wn.bgcolor("lightblue")
wn.setup(width=600, height=600)

# Variáveis globais
score = 0
game_time = 20  # duração do jogo em segundos
turtles = []
colors = ["red", "green", "blue", "orange", "purple", "black"]

# Texto do placar
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.goto(0, 260)
score_writer.write(f"Pontuação: {score}", align="center", font=("Arial", 18, "bold"))

# Texto de tempo
time_writer = turtle.Turtle()
time_writer.hideturtle()
time_writer.penup()
time_writer.goto(0, 230)
time_writer.write(f"Tempo: {game_time}", align="center", font=("Arial", 16, "normal"))

# Função para atualizar placar
def update_score():
    score_writer.clear()
    score_writer.write(f"Pontuação: {score}", align="center", font=("Arial", 18, "bold"))

# Função para atualizar tempo
def update_time(t):
    time_writer.clear()
    time_writer.write(f"Tempo: {t}", align="center", font=("Arial", 16, "normal"))

# Função chamada ao clicar na tartaruga
def catch_turtle(x, y, t):
    global score
    score += 1
    update_score()
    move_turtle(t)

# Criar tartarugas clicáveis
def create_turtles(num):
    for i in range(num):
        t = turtle.Turtle()
        t.shape("turtle")
        t.color(random.choice(colors))
        t.penup()
        t.speed(0)
        move_turtle(t)
        t.onclick(lambda x, y, t=t: catch_turtle(x, y, t))
        turtles.append(t)

# Mover tartaruga para posição aleatória
def move_turtle(t):
    x = random.randint(-250, 250)
    y = random.randint(-200, 200)
    t.goto(x, y)

# Contagem regressiva
def countdown(t):
    if t > 0:
        update_time(t)
        wn.ontimer(lambda: countdown(t - 1), 1000)
    else:
        update_time(0)
        game_over()

# Fim do jogo
def game_over():
    for t in turtles:
        t.hideturtle()
    wn.clear()
    wn.bgcolor("lightcoral")
    go = turtle.Turtle()
    go.hideturtle()
    go.write(f"⏰ Fim de Jogo!\nPontuação Final: {score}", align="center", font=("Arial", 22, "bold"))

# Iniciar jogo
create_turtles(5)  # quantidade de tartarugas
countdown(game_time)

wn.mainloop()

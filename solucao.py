#Bibliotecas
import pygame
#Inicializar o Pygame
pygame.init()

# Constante de Largura e Altura
LARGURA, ALTURA = 700, 500

# Setup de Janela do Jogo
JANELA = pygame.display.set_mode((LARGURA, ALTURA))

# Constante de FPS (Para todos os computadores)
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Dimensões da Barra do Jogo
BARRA_LARGURA, BARRA_ALTURA = 20, 100

# Titulo da Janela
pygame.display.set_caption("Pong")

class Barra:
    COR = BRANCO # Constante para cor Branca

    def __init__(self, x, y, largura, altura): #Construtor
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
    
    def desenhar(self, janela): # Desenhar um retangulo
        pygame.draw.rect(janela, self.COR, (self.x, self.y, self.largura, self.altura))

def desenhar(janela, barras):
    janela.fill(PRETO) # Preencher a tela com a cor Preto

    for barra in barras:
        barra.desenhar(janela)

    pygame.display.update() #Atualizar

def main():
    exe = True #Executar
    clock = pygame.time.Clock() #FPS do Jogo

    barra_esquerda = Barra(10, ALTURA // 2 - BARRA_ALTURA // 2, 
                                    BARRA_LARGURA, BARRA_ALTURA) # Centrar a barra na janela do jogo
    barra_direita = Barra(LARGURA - 10 - BARRA_LARGURA, ALTURA // 2 - BARRA_ALTURA // 2, 
    BARRA_LARGURA, BARRA_ALTURA)

    while exe: # Executar as funções enquanto o jogo está aberto
        clock.tick(FPS)
        desenhar(JANELA, [barra_esquerda, barra_direita])
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Se o botão de sair, for pressionado
                exe = False # A execução acaba
                break
    pygame.quit() # O jogo irá fechar


if __name__ == '__main__':
    main()
                

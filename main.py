#Bibliotecas
import pygame

#Inicializar o Pygame
pygame.init()

# Constante de Largura e Altura da janela
LARGURA, ALTURA = 700, 500

# Setup de Janela do Jogo
JANELA = pygame.display.set_mode((LARGURA, ALTURA))

# Constante de FPS (Para todos as máquinas)
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Dimensões da raquete do Jogo
RAQUETE_LARGURA, RAQUETE_ALTURA = 20, 100

# Raio da bola
BOLA_RAIO = 7

# Fonte da Pontuação
PONTUACAO_FONTE = pygame.font.SysFont("ComicSans", 50)

# Pontuação final para ganhar o jogo
PONTUACAO_FINAL = 10

# Titulo da Janela
pygame.display.set_caption("Jogo para estudo - Pong")

class Bola:
    MAX_VELOCIDADE = 5
    COR = BRANCO
    def __init__(self, x, y, raio): # Construtor
        self.x = self.x_original = x
        self.y = self.y_original = y
        self.raio = raio
        self.x_velocidade = self.MAX_VELOCIDADE
        self.y_velocidade = 0
    
    def desenhar(self, janela): # Desenhar a bola
        pygame.draw.circle(janela, self.COR, (self.x, self.y), self.raio)

    def mover(self): # Mover a bola
        self.x += self.x_velocidade
        self.y += self.y_velocidade

    def resetar(self): # Resetar a bola/inverter a direção
        self.x = self.x_original
        self.y = self.y_original
        self.y_velocidade = 0
        self.x_velocidade *= -1


class Raquete:
    COR = BRANCO # Constante para cor Branca da raquete
    VELOCIDADE = 4 # Constante para velocidade da raquete

    def __init__(self, x, y, largura, altura): #Construtor da raquete (posição/tamanho)
        self.x = self.x_original = x
        self.y = self.y_original = y
        self.largura = largura
        self.altura = altura
    
    def desenhar(self, janela): # Desenhar a raquete
        pygame.draw.rect(janela, self.COR, (self.x, self.y, self.largura, self.altura))

    def mover(self, cima=True): # Mover as raquetes
        if cima: # Se quiser mover pra cima
            self.y -= self.VELOCIDADE #Subtraia sua coord Y com a velocidade
        else:
            self.y += self.VELOCIDADE #Some sua coord Y com a velocidade

    def resetar(self): # Resetar as raquetes para a posição original
        self.x = self.x_original
        self.y = self.y_original



def desenhar(janela, raquetes, bola, pontuacao_esquerda, pontuacao_direita):
    janela.fill(PRETO) # Preencher a tela com a cor Preto

    # Render da fonte da pontuação
    texto_pontuacao_esquerda = PONTUACAO_FONTE.render(f"{pontuacao_esquerda}", 1, BRANCO)
    texto_pontuacao_direita = PONTUACAO_FONTE.render(f"{pontuacao_direita}", 1, BRANCO)

    # Centralizar as duas pontuações 3/4 da tela
    janela.blit(texto_pontuacao_esquerda, (LARGURA // 4 - texto_pontuacao_esquerda.get_width() // 2, 20))
    janela.blit(texto_pontuacao_direita, (LARGURA * (3/4) - texto_pontuacao_direita.get_width() // 2, 20))

    # Desenhar as duas raquetes
    for raquete in raquetes:
        raquete.desenhar(janela)

    # Desenhar a rede/mesa do jogo
    for i in range(10, ALTURA, ALTURA // 20):
        if i % 2 == 1: # Espaçamento entre os retangulos
            continue
        pygame.draw.rect(janela, BRANCO, (LARGURA // 2 - 5, i, 10, ALTURA // 20))
    
    # Desenhar a bola no jogo
    bola.desenhar(janela) 
    # Atualizar partes da tela para exibições
    pygame.display.update() #Atualizar

def colisao(bola, raquete_esquerda, raquete_direita):
    # Se a bola colidir embaixo
    if bola.y + bola.raio >= ALTURA:  # Centro da bola + raio da bola >= altura da janela
        bola.y_velocidade *= -1 # Inverte a direção da bola
     # Se a bola colidir em cima
    elif bola.y - bola.raio <= 0:
        bola.y_velocidade *= -1 # Inverte a direção da bola
    
    # Se a bola colidir com a raquete esquerda
    if bola.x_velocidade < 0:
        if bola.y >= raquete_esquerda.y and bola.y <= raquete_esquerda.y + raquete_esquerda.altura: # Verificar se a bola colidiu com a altura da raquete
            if bola.x - bola.raio <= raquete_esquerda.x + raquete_esquerda.largura: # Verificar se a bola colidiu com o canto direito (da raquete esquerda)
                bola.x_velocidade *= -1 # Inverte a direção da bola

                # Formula para o efeito de quicar a bola
                meio_y = raquete_esquerda.y + raquete_esquerda.altura / 2
                diferenca_y = meio_y - bola.y
                fator_reducao = (raquete_esquerda.altura / 2) / bola.MAX_VELOCIDADE
                y_velocidade = diferenca_y / fator_reducao
                bola.y_velocidade = -1 * y_velocidade

    # Se a bola colidir com a raquete direita
    else:
        if bola.y >= raquete_direita.y and bola.y <= raquete_direita.y + raquete_direita.altura:
            if bola.x + bola.raio >= raquete_direita.x: # Verificar se a bola colidiu com o canto esquerdo (da raquete direita)
                bola.x_velocidade *= -1 # Inverte a direção da bola

                # Formula para o efeito de quicar a bola
                meio_y = raquete_direita.y + raquete_direita.altura / 2
                diferenca_y = meio_y - bola.y
                fator_reducao = (raquete_direita.altura / 2) / bola.MAX_VELOCIDADE
                y_velocidade = diferenca_y / fator_reducao
                bola.y_velocidade = -1 * y_velocidade

def raquete_movimento(teclas, raquete_esquerda, raquete_direita):
    # Manusear os movimentos da raquete esquerda com as teclas W/S E controlar para que não saia fora da tela
    if teclas[pygame.K_w] and raquete_esquerda.y - raquete_esquerda.VELOCIDADE >= 0:
        raquete_esquerda.mover(cima=True)
    if teclas[pygame.K_s] and raquete_esquerda.y + raquete_esquerda.VELOCIDADE + raquete_esquerda.altura <= ALTURA:
        raquete_esquerda.mover(cima=False)
        
    # Manusear os movimentos da raquete direita com as teclas ↑/↓ E controlar para que não saia fora da tela
    if teclas[pygame.K_UP] and raquete_direita.y - raquete_direita.VELOCIDADE >= 0:
        raquete_direita.mover(cima=True)
    if teclas[pygame.K_DOWN] and raquete_direita.y + raquete_direita.VELOCIDADE + raquete_direita.altura <= ALTURA:
        raquete_direita.mover(cima=False)

#Chamar todas as funções para a execução do jogo
def main():
    exe = True #Executar
    clock = pygame.time.Clock() #FPS do Jogo
    # Centralizar a raquete na janela do jogo
    raquete_esquerda = Raquete(10, ALTURA // 2 - RAQUETE_ALTURA // 2, RAQUETE_LARGURA, RAQUETE_ALTURA) 
    raquete_direita = Raquete(LARGURA - 10 - RAQUETE_LARGURA, ALTURA // 2 - RAQUETE_ALTURA // 2, RAQUETE_LARGURA, RAQUETE_ALTURA)
    bola = Bola(LARGURA // 2, ALTURA // 2, BOLA_RAIO)
    # Pontuação inicial
    pontuacao_esquerda = 0
    pontuacao_direita = 0

    while exe: # Executar as funções enquanto o jogo está aberto
        clock.tick(FPS) # Atualizar o FPS do jogo
        desenhar(JANELA, [raquete_esquerda, raquete_direita], bola, pontuacao_esquerda, pontuacao_direita) # Executar a função desenhar as raquetes e a bola

        # Gerenciar o evento de sair do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Se o botão de sair, for pressionado
                exe = False # A execução acaba
                break

        # Obter o estado de todos os botões do teclado      
        teclas = pygame.key.get_pressed()
        # Chamar a função para movimentar as raquetes
        raquete_movimento(teclas, raquete_esquerda, raquete_direita)
        # Executar a movimentação da bola
        bola.mover()
        # Manusear a colisão no jogo
        colisao(bola, raquete_esquerda, raquete_direita)

        # Checando se o jogador pontuou (a bola passou da raquete)
        if bola.x < 0:
            pontuacao_direita += 1
            bola.resetar()
        elif bola.x > LARGURA:
            pontuacao_esquerda +=1
            bola.resetar()
        
        # Manusear se o jogador ganhou o jogo
        vitoria = False
        if pontuacao_esquerda >= PONTUACAO_FINAL:
            vitoria = True
            texto_vitoria = 'Jogador Esquerdo Ganhou!'
        elif pontuacao_direita >= PONTUACAO_FINAL:
            vitoria = True
            texto_vitoria = 'Jogador Direito Ganhou!'
        # Se ocorrer vitoria, resetar as raquetes e a bola
        if vitoria:
            texto = PONTUACAO_FONTE.render(texto_vitoria, 1, BRANCO) # Formatação da fonte de vitoria
            JANELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2)) # Centralizar a pontuação na tela 
            pygame.display.update() # Atualizar o jogo
            pygame.time.delay(5000) # 5 segundos de delay
            # Resetar o jogo
            bola.resetar()
            raquete_esquerda.resetar()
            raquete_direita.resetar()
            pontuacao_esquerda = 0
            pontuacao_direita = 0

    pygame.quit() # O jogo irá fechar se exe = False

# Chamar a função main e rodar o jogo
if __name__ == '__main__':
    main()
                

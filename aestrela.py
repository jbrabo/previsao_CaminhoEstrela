#O ALGORITIMO A* cálcula a nota de cada célula até o ponto final, 
#Levando em consideração o f_score = g_score+h_score 
#Onde g_score é a quantidade de passos para chegar a célula, e 
#h_score é a distancia entre a célula e o ponto final

from pyamaze import maze, agent
from queue import PriorityQueue 

destino = (1,1)

def h_score(celula,destino):
    linhac = celula[0]
    colunac = celula[1]
    linhad = destino[0]
    colunad = destino[1]
    return abs(colunac-colunad)+abs(linhac-linhad)

def aestrela(labirinto_set):
    # iniciando o tabuleiro com todo mundo com f_score infinito
    f_score = {celula:float("inf") for celula in labirinto_set.grid}
    #iniciando a variável g_score como vazia, será preenchida 
    #a medida que os passos são dados
    g_score = {}

    #Calcular o valor da célula inicial 
    #capturando total de linhas e colunas existente no labirinto,
    #e registrando a célula NxN como o ponto inicial
    celula_inicial = (labirinto_set.rows, labirinto_set.cols)
    
    g_score [celula_inicial]= 0
    f_score [celula_inicial] = g_score[celula_inicial]+h_score(celula_inicial,destino)

    fila = PriorityQueue()
    item = (f_score[celula_inicial], h_score(celula_inicial,destino), celula_inicial)
    fila.put(item)

    caminho = {}
    #enquanto minha fila não estiver vazia
    #vou realizar os cálculos até chegar ao destino final
    
    while not fila.empty():
        celula = fila.get()[2]
        
        #se a célula retirada da fila for o destino final pode encerrar
        if celula == destino:
            break

        #Calcular o f_score dos caminhos possíveis
        for direcao in "NSEW":
            if labirinto_set.maze_map[celula][direcao] == 1:
                
                #Nossa célula foi retirada de uma lista de itens qual é uma tupla
                #a posição 0 é linhas e 1 é colunas
                linha_celula = celula[0]
                coluna_celula = celula[1]

                #De acordo com a variação que desejamos andar vamos movimentar
                #um paço naquela direção
                if direcao == "N":
                    proxima_celula = (linha_celula-1, coluna_celula)
                
                elif direcao == "S":
                    proxima_celula = (linha_celula+1, coluna_celula)
                
                elif direcao == "W":
                    proxima_celula = (linha_celula, coluna_celula-1)
                
                elif direcao == "E":
                    proxima_celula = (linha_celula, coluna_celula+1)
        
            #encontrado a próxima celula, 
            #precisamos calcular os novos scores
                novo_gscore = g_score[celula]+1
                novo_fscore = novo_gscore + h_score(proxima_celula,destino)

            #Se os score forem menores, logo teremos que
            #substituir os scores antigos
                if novo_fscore < f_score[proxima_celula]:
                    
                    f_score[proxima_celula] = novo_fscore
                    g_score[proxima_celula] = novo_gscore
                    item = (novo_fscore,h_score(proxima_celula,destino),proxima_celula)
                    fila.put(item)
                    caminho[proxima_celula] = celula
    
    #caminho foi passado sempre da célula que estou indo 
    # para célula que vim
    caminho_final = {}
    celula_analisada = destino

    #Dessa forma consigo percorrer o dicionário e inverter seus valores
    while celula_analisada != celula_inicial:
        caminho_final[caminho[celula_analisada]] = celula_analisada
        celula_analisada = caminho[celula_analisada]

    return caminho_final


#Criando labirinto com a biblioteca Pyamaze

labirinto = maze()
labirinto.CreateMaze()

#criando o agente que irá percorrer o labirinto
agente = agent(labirinto, filled=True, footprints=True)

#traçando o caminho através da função que calcula os scores
caminho = aestrela(labirinto)

#traçando visual, que nosso agente percorreu através dos cálculos do score
labirinto.tracePath({agente: caminho}, delay=50)
labirinto.run()
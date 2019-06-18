import numpy as np
import imageio
import matplotlib.pyplot as plt
import sys

"""Funcao que retorna o valor otimo para o Thresholding"""
def calculate_optimal_T(img, T0, M, N, debug=False):
    optimal_T = T0          #Inicializa o Thresholding otimo
    prev_T = T0*2           #Inicializa o Thresholding anterior com um numero maior do que o inicial
    if debug == True:
        print("Inicial: " + str(T0))
    while True:
        G1 = img[np.where(img > optimal_T)]
        G2 = img[np.where(img <= optimal_T)]
        prev_T    = optimal_T
        optimal_T = (np.average(G1) + np.average(G2))/2.0
        if (abs(optimal_T-prev_T) <= 0.5):
            if debug == True:
                print("T-Otimo: " + str(optimal_T))
            break
        if debug == True:
            print("Converg: " + str(optimal_T))
    return optimal_T

"""Funcao Limiarization"""
def limiarization(img, M, N):
    T0 = 127
    img_thresh = np.zeros([M,N], dtype=int)                 #Inicializa uma matriz para a imagem de saida
    optimal_T = calculate_optimal_T(img, T0, M, N, True)    #Obtem o Thresholding otimo
    img_thresh[np.where(img > optimal_T)] = 1
    return img_thresh

"""Retorna a imagem erodita"""
def erosion(img, M, N): 
    n = m = 3        #
    a = int((n-1)/2) #Calculo da vizinhanca a ser explorada
    b = int((m-1)/2) #Calculo da vizinhanca a ser explorada
    g = np.array(img, copy=True) #Imagem com valores originais nas bordas
    for x in range(a, M-a):
        for y in range(b, N-b):
            sub_img = img[ x-a : x+a+1 , y-b:y+b+1 ]
            if np.sum(sub_img) != 0:   #Se o somatorio for diferente de zero, quer dizer que ha pelo menos um branco
                g[x,y] = 1                 #Entao adiciona o branco
    return g
    
"""Retorna a imagem dilatada"""
def dilation(img, M, N): 
    n = m = 3        #
    a = int((n-1)/2) #Calculo da vizinhanca a ser explorada
    b = int((m-1)/2) #Calculo da vizinhanca a ser explorada
    g = np.array(img, copy=True) #Imagem com valores originais nas bordas
    for x in range(a, M-a):
        for y in range(b, N-b):
            sub_img = img[ x-a : x+a+1 , y-b:y+b+1 ]
            if np.sum(sub_img) != (n*m):    #Se o somatorio for diferente do tamanho do filtro, quer dizer que ha pelo menos um preto
                g[x,y] = 0                      #Entao adiciona o preto
    return g
    
"""Retorna o Fechamento: Suaviza o contorno pelo exterior"""
def closing(img, M, N):
    img = dilation(img, M, N)
    img = erosion(img, M, N)
    return img
    
"""Retorna a Abertura: Suaviza o contorno pelo interior"""
def opening(img, M, N):
    img = erosion(img, M, N)
    img = dilation(img, M, N)
    return img

"""Normaliza entradas entre 0 e 1, depois converte entre 0 e 255"""
def normalize_values(img):
    imax = np.max(img)
    imin = np.min(img)
    img_norm = (img-imin)/(imax-imin)
    img_norm = (img_norm * 255).astype(np.uint8)
    return img_norm

"""Mostra as 3 imagens, uma ao lado da outra"""
def show_image(img, img_out):
    plt.figure(figsize=(10,12))
    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    plt.title("Original")
    plt.subplot(122)
    plt.title("Output")
    plt.imshow(img_out, cmap='gray')
    plt.show()

"""Retorna as dimensoes da imagem"""
def size_image(img):
    return img.shape

"""Carrega a imagem de entrada"""
def load_image(nome):
    img = imageio.imread(nome)
    return img

"""Verifica o numero de argumentos passados"""
def verify_arguments():
    if len(sys.argv) < 2:
        print("Digite " + str(sys.argv[0]) + " <img>\n")
        exit(-1)
    return True

"""Funcao principal"""
def main():
    if(verify_arguments()):
        filename = sys.argv[1]
        img = load_image(filename)
        M,N = size_image(img)
        img_out = np.zeros([M,N], dtype=float) #Inicializa uma matriz para a imagem de saida
        
        """Point Operations"""
        img_out = limiarization(img, M, N)
        img_out = opening(img_out, M, N)
        img_out = normalize_values(img_out)
        show_image(img, img_out)
        
"""Funcao Principal"""
main()

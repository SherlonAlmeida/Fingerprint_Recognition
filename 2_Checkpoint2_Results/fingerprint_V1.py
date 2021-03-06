###### Useful Libraries ####################################
import numpy as np                                         #
import imageio, sys, math                                  #
import matplotlib.pyplot as plt                            #
from scipy.fftpack import fftn, ifftn, fftshift, ifftshift #
from scipy import ndimage                                  #
from matplotlib.colors import LogNorm                      #
from skimage.morphology import skeletonize                 #
from skimage.util import invert                            #
############################################################


"""Gera o filtro de Gabor para os parametros passados"""
def genGabor(sz, omega, theta, func=np.cos, K=np.pi):
    radius = (int(sz[0]/2.0), int(sz[1]/2.0))
    if sz[0]%2==0 and sz[1]%2==0: #(PAR, PAR)
        [x, y] = np.meshgrid(range(-radius[0], radius[0]), range(-radius[1], radius[1]))
    if sz[0]%2==1 and sz[1]%2==1: #(IMPAR, IMPAR)
        [x, y] = np.meshgrid(range(-radius[0], radius[0]+1), range(-radius[1], radius[1]+1))
    if sz[0]%2==0 and sz[1]%2==1: #(PAR, IMPAR)
        [x, y] = np.meshgrid(range(-radius[0], radius[0]), range(-radius[1], radius[1]+1))
    if sz[0]%2==1 and sz[1]%2==0: #(IMPAR, PAR)
        [x, y] = np.meshgrid(range(-radius[0], radius[0]+1), range(-radius[1], radius[1]))
    x1 = x * np.cos(theta) + y * np.sin(theta)
    y1 = -x * np.sin(theta) + y * np.cos(theta)
    gauss = omega**2 / (4*np.pi * K**2) * np.exp(- omega**2 / (8*K**2) * ( 4 * x1**2 + y1**2))
    #show_image(gauss, gauss)
    sinusoid = func(omega * x1) * np.exp(K**2 / 2)
    #show_image(sinusoid, sinusoid)
    gabor = gauss * sinusoid
    return gabor

"""Realiza a convolucao com os filtros de Gabor gerados"""
def gabor_filter_frequency_domain(f, M, N, plot=False):
    n_rotation = 8
    n_scale = 8
    theta = np.linspace(0.0, np.pi, n_rotation)
    omega = np.geomspace(0.1, 0.9, n_scale)
    params = [(t,o) for o in omega for t in theta]
    filterBank = []
    fftFilterBank = []
    gaborParams = []
    gaborFeaturesBank = []
    for (theta, omega) in params:
        gaborParam = {'omega':omega, 'theta':theta, 'sz':(N, M)}
        gabor = genGabor(func=np.cos, **gaborParam)
        filterBank.append(gabor)
        fftFilterBank.append(fftn(gabor))
        gaborParams.append(gaborParam)

    #Imprime os filtros de Gabor Gerados no Dominio Espacial
    if plot == True:
        plt.figure()
        plt.suptitle("Filtros de Gabor no Dominio Espacial", fontsize=16)
        n = len(filterBank)
        for i in range(n):
            plt.subplot(n_scale,n_rotation,i+1)
            plt.axis('off')
            plt.imshow(filterBank[i], cmap='gray')
    
    #Imprime os filtros de Gabor Gerados e convertidos para o Dominio de Frequencia
    if plot == True:
        plt.figure()
        plt.suptitle("Filtros de Gabor no Dominio de Frequencia", fontsize=16)
        n = len(fftFilterBank)
        for i in range(n):
            im_fft = fftshift(fftFilterBank[i])
            plt.subplot(n_scale,n_rotation,i+1)
            plt.axis('off')
            plt.imshow(np.log(np.abs(im_fft)+1), cmap='gray')
    
    n = len(fftFilterBank)
    out = np.zeros([M,N]).astype(np.float64)
    for i in range(n):
        G = fftFilterBank[i]
        F = fftn(f)
        C = np.multiply(F, G)
        f_rest = np.real(fftshift(ifftn(C)))
        #De repente converter f_rest para o range -1 a 1 e aplicar a funcao x^3 ou sigmoide (Talvez apareca apenas os valores das transicoes detectados)
        out += f_rest
        gaborFeaturesBank.append(f_rest)
        #show_image(f_rest, out)
    
    #Imprime a imagem de entrada filtrada com os filtros de Gabor Gerados
    if plot == True:
        plt.figure()
        plt.suptitle("Mapa de Features da Filtragem de Gabor", fontsize=16)
        n = len(gaborFeaturesBank)
        for i in range(n):
            im_gabor = gaborFeaturesBank[i]
            plt.subplot(n_scale,n_rotation,i+1)
            plt.axis('off')
            plt.imshow(im_gabor, cmap='gray')    
    
    out = normalize_values(out)
    return out

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
    optimal_T = calculate_optimal_T(img, T0, M, N, False)   #Obtem o Thresholding otimo
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

"""Retorna um valor a partir de uma funcao Sigmoide"""
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

"""Gaussian Filter Operation"""
def gaussian_filter(k=3, sigma=1.0):
    arx = np.arange((-k//2) + 1.0, (k//2) + 1.0)
    x, y = np.meshgrid(arx, arx)
    filt = np.exp(-(1/2)*(np.square(x) + np.square(y))/np.square(sigma))
    F = filt/np.sum(filt)
    return F

"""Dado um filtro, eh realizado o padding centralizando o filtro em uma imagem de tamanho dado"""
"""Parametros da funcao: paddind(Imagem, Filtro, Linhas da Imagem, Colunas da Imagem, Linhas do Filtro, Colunas do Filtro)"""
def padding(img, filt, M, N, m, n):
    pad_p = np.zeros([M,N]).astype(np.float64)
    init_x = (M//2)-m
    init_y = (N//2)-n
    filt_i = 0
    for img_i in range(init_x, init_x+m):
        filt_j = 0
        for img_j in range(init_y, init_y+n):
            #print(img_i, img_j, filt_i, filt_j)
            pad_p[img_i,img_j] = filt[filt_i,filt_j]
            filt_j += 1
        filt_i += 1
    return pad_p

"""Constrained Least Squares Filtering Operation"""
"""Obs.: Era pra usar o conjugado transposto, mas como os filtros utilizados no trabalho sao simetricos nao precisa"""
def constrained_least_squares_filtering(g, M, N, k=5, sigma=1.25, gamma=0.02):
    p = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])                         #Laplacian Operator
    m,n = size_image(p)                                                 #Tamanho do Filtro Laplaciano
    P = fftn(padding(g, p, M, N, m, n))                                 #Laplacian Fourier
    G = fftn(g)                                                         #Degraded Image Fourier
    h = gaussian_filter(k, sigma)                                       #Degradation Operator
    H = fftn(padding(g, h, M, N, k, k))                                 #Degradation Fourier
    C = np.multiply(np.divide(np.conj(H), (np.square(np.absolute(H)) + (gamma * np.square(np.absolute(P))))), G)
    f_rest = np.real(fftshift(ifftn(C)))
    return f_rest

"""Calcula o erro"""
def rms_error(img, out):
    M,N = img.shape
    error = ((1/(M*N))*np.sum((img-out)**2))**(1/2)
    return error

"""Normaliza entradas entre 0 e 1, depois converte entre 0 e 255"""
def normalize_values(img):
    imax = np.max(img)
    imin = np.min(img)
    img_norm = (img-imin)/(imax-imin)
    img_norm = (img_norm * 255).astype(np.float64)
    return img_norm

"""Mostra as 3 imagens, uma ao lado da outra"""
def show_image(img, img_out):
    plt.figure(figsize=(10,12))
    plt.suptitle("Resultado Obtido", fontsize=16)
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
        
        #Realizar um laco para processar todas as imagens da pasta Treinamento e depois validar com as imagens da pasta Teste
        img_out = gabor_filter_frequency_domain(img, M, N)          #Image Enhancement
        img_out = constrained_least_squares_filtering(img_out, M,N) #Image Deblurring
        img_out = limiarization(img_out, M, N)                      #Image Segmentation
        img_out = opening(img_out, M, N)                            #Image Denoising
        img_out = abs(img_out-np.max(img_out))                      #Image Inverse
        img_out = skeletonize(img_out).astype(np.float64)           #Image Skeletonization
        img_out = abs(img_out-np.max(img_out))                      #Image Inverse
        #Gerar Minutae Features                                      #Feature Extraction
        #Realizar Matching                                           #Matching
                
        #img_out = normalize_values(img_out)
        show_image(img, img_out)
        
        
"""Funcao Principal"""
main()

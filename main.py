import cv2
from ultralytics import YOLO
import numpy as np
MAX_DISPLAY_WIDTH = 1280
MAX_DISPLAY_HEIGHT = 720
# Aqui ele vai ler o .pt que o modelo treinou
model = YOLO('yolov8m.pt')

# O "0" geralmente puxa a cam

cap = cv2.VideoCapture("C:\\Users\\bruno\\MapaDeCalor\\YTDown_YouTube_Panoramic-video-of-the-football-pitch_Media_HBTFZwMdcCw_001_1080p.mp4")

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

cv2.namedWindow("Monitoramento de Jogadores (PoC)", cv2.WINDOW_NORMAL)
cv2.namedWindow("Radar 2D (Vista de Cima)", cv2.WINDOW_NORMAL)

#  Configuracao da Homografia (Calibração do Campo)
# 1. Os 4 cantos da área na sua câmera (em pixels)
pontos_camera = np.float32([
    [580, 97], # 1. Topo-Esquerdo
    [1344, 97], # 2. Topo-Direito
    [1896, 415], # 3. Baixo-Direito
    [30, 415]   # 4. Baixo-Esquerdo
])

# 2. O tamanho do nosso "Radar 2D" visto de cima
largura_mapa, altura_mapa = 600, 400
pontos_plano_2d = np.float32([
    [0, 0],                         # 1. Topo-Esquerdo
    [largura_mapa, 0],              # 2. Topo-Direito
    [largura_mapa, altura_mapa],    # 3. Baixo-Direito
    [0, altura_mapa]                # 4. Baixo-Esquerdo
])

# 3. A Matemática: Calcula a Matriz de Homografia
matriz_homografia = cv2.getPerspectiveTransform(pontos_camera, pontos_plano_2d)
# -------------------------------------------------------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Passa o frame pelo YOLO filtrando apenas a classe 0 (pessoas)
    resultados = model(frame, classes=0)

    # Desenha as caixas delimitadoras no frame
    frame_anotado = resultados[0].plot()

    # Cria a imagem preta para o mapa 2D
    mapa_2d = np.zeros((altura_mapa, largura_mapa, 3), dtype=np.uint8)

    # Desenha as linhas verdes do "campo" na câmera principal pra ajudar a visualizar
    cv2.polylines(frame_anotado, [np.int32(pontos_camera)], True, (0, 255, 0), 2)

    # Laço para ler cada pessoa que o YOLO achou na tela
    for box in resultados[0].boxes:
        # Pega as coordenadas da caixa delimitadora
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

        # Calcula o meio da base (onde fica o pé)
        x_pe = int((x1 + x2) / 2)
        y_pe = int(y2)

        # Desenha a bolinha vermelha no pé
        cv2.circle(frame_anotado, (x_pe, y_pe), 5, (0, 0, 255), -1)

        # Prepara o ponto para a matemática do OpenCV
        ponto_pe_array = np.array([[[x_pe, y_pe]]], dtype=np.float32)

        # Aplica a transformação de perspectiva para virar 2D
        ponto_transformado = cv2.perspectiveTransform(ponto_pe_array, matriz_homografia)

        # Coordenadas finais no radar
        x_2d = int(ponto_transformado[0][0][0])
        y_2d = int(ponto_transformado[0][0][1])

        # Se o jogador estiver dentro do campo verde, desenha a bolinha amarela no radar
        if 0 <= x_2d <= largura_mapa and 0 <= y_2d <= altura_mapa:
            cv2.circle(mapa_2d, (x_2d, y_2d), 10, (0, 255, 255), -1)
    # -------------------------------------------------------------------

    height, width = frame_anotado.shape[:2]
    scale = min(MAX_DISPLAY_WIDTH / width, MAX_DISPLAY_HEIGHT / height, 1.0)
    display_size = (int(width * scale), int(height * scale))
    frame_exibicao = cv2.resize(frame_anotado, display_size, interpolation=cv2.INTER_AREA)

    cv2.imshow("Monitoramento de Jogadores (PoC)", frame_exibicao)
    cv2.imshow("Radar 2D (Vista de Cima)", mapa_2d)

    # Pressione "q" para encerrar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
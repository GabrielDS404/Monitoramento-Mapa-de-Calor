import cv2

# Ajuste o tamanho máximo da janela aqui (mantém proporção)
MAX_DISPLAY_WIDTH = 1280
MAX_DISPLAY_HEIGHT = 720

frame = None
frame_original = None
scale_x = 1.0
scale_y = 1.0

def pegar_coordenadas(event, x, y, flags, param):
    # Se o botão esquerdo do mouse for clicado
    if event == cv2.EVENT_LBUTTONDOWN:
        x_original = int(x / scale_x)
        y_original = int(y / scale_y)
        print(f"Ponto clicado: [{x}, {y}] (exibido) -> [{x_original}, {y_original}] (original)")
        # Desenha uma bolinha vermelha só para você ver onde clicou
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Calibracao", frame)

cap = cv2.VideoCapture("C:\\Users\\bruno\\MapaDeCalor\\YTDown_YouTube_Panoramic-video-of-the-football-pitch_Media_HBTFZwMdcCw_001_1080p.mp4") # Mude para 1 ou 2 se a câmera não abrir

cv2.namedWindow("Calibracao", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Calibracao", pegar_coordenadas)

print("Clique nos 4 objetos no chão seguindo esta ordem:")
print("1. Superior Esquerdo | 2. Superior Direito | 3. Inferior Esquerdo | 4. Inferior Direito")
print("Pressione 'q' para sair.")

while True:
    ret, frame_original = cap.read()
    if not ret:
        break

    height, width = frame_original.shape[:2]
    scale = min(MAX_DISPLAY_WIDTH / width, MAX_DISPLAY_HEIGHT / height, 1.0)
    display_size = (int(width * scale), int(height * scale))
    frame = cv2.resize(frame_original, display_size, interpolation=cv2.INTER_AREA)

    scale_x = display_size[0] / width
    scale_y = display_size[1] / height

    cv2.imshow("Calibracao", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
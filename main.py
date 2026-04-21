import cv2
from ultralytics import YOLO

# Aqui ele vai ler o .pt que o modelo treinou
model = YOLO('yolov8n.pt')

# O "0" geralmente puxa a cam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Passa o frame pelo YOLO filtrando apenas a classe 0 (pessoas)
    resultados = model(frame, classes=0)

    # Desenha as caixas delimitadoras no frame
    frame_anotado = resultados[0].plot()

    cv2.imshow("Monitoramento de Jogadores (PoC)", frame_anotado)

    # Pressione "q" para encerrar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
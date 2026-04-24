import cv2

def pegar_coordenadas(event, x, y, flags, param):
    # Se o botão esquerdo do mouse for clicado
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Ponto clicado: [{x}, {y}]")
        # Desenha uma bolinha vermelha só para você ver onde clicou
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Calibracao", frame)

cap = cv2.VideoCapture(0) # Mude para 1 ou 2 se a câmera não abrir

cv2.namedWindow("Calibracao")
cv2.setMouseCallback("Calibracao", pegar_coordenadas)

print("Clique nos 4 objetos no chão seguindo esta ordem:")
print("1. Superior Esquerdo | 2. Superior Direito | 3. Inferior Esquerdo | 4. Inferior Direito")
print("Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret: break

    cv2.imshow("Calibracao", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
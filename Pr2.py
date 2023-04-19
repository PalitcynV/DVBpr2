import cv2

cap = cv2.VideoCapture('cam_video.mp4')

while True:  # смотрим покадрово
    ret, frame = cap.read()
    if not ret:  # если кадр заканчивается, закончим цикл
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # размываем шум

    ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)  # преобразуем в черно-белое изображение

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # контуры

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)  # ищем максимальный контур по площади
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # делаем прямоугольник зеленым (0, 255, 0)

        # text = 'Coordinates: (' + str(x) + '; ' + str(y) + ')'
        # print(text)
        # cv2.line(frame, (0, 20), (100, 20), (250, 0, 0), 2)
        # cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))

        # центр объекта
        x0 = x + w // 2
        y0 = y + h // 2
        # центр кадра
        frame_x0 = frame.shape[1] // 2
        frame_y0 = frame.shape[0] // 2
        # перевернем систему координат по вертикали, чтобы Y был положительным выше OX
        y0 = frame.shape[0] - y0
        # координаты центра объекта относительно центра кадра
        d_x = x0 - frame_x0
        d_y = y0 - frame_y0
        # расстояние
        d = (d_x ** 2 + d_y ** 2) ** 0.5
        text1 = 'Distance coordinates: (' + str(d_x) + '; ' + str(d_y) + ')'
        cv2.putText(frame, text1, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
        text2 = 'Distance = ' + str(d)
        cv2.putText(frame, text2, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
        print(text2)
        cv2.circle(frame, (frame_x0, frame_y0), 5, (0, 255, 0), -1)  # добавим точку в центр кадра

    cv2.imshow('frame', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):  # каждый кадр 100мс ждет нажатия клавиши,  q-завершить
        break

cap.release()
cv2.destroyAllWindows()

import time
import cv2
import pyautogui as pag
import mediapipe as mp
import win32api
import win32con


def left_click(xs, ys):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, xs, ys, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, xs, ys, 0, 0)
    time.sleep(0.2)


def left_double_click(xs, ys):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, xs, ys, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, xs, ys, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, xs, ys, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, xs, ys, 0, 0)
    time.sleep(0.2)


def right_click(xs, ys):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, xs, ys, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, xs, ys, 0, 0)
    time.sleep(0.2)


def move_cursor(x_a, y_a):
    xs = int(width - (x_a * width) / w + 50)
    ys = int((y_a * height) / h + 50)
    win32api.SetCursorPos((xs, ys))


cap = cv2.VideoCapture(0)
width, height = pag.size()
hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2,
                                 min_tracking_confidence=0.5, min_detection_confidence=0.5)
violet = (204, 102, 153)
green = (0, 255, 0)
first = True

while True:
    res, frame = cap.read()
    h, w = frame.shape[:2]
    result = hands.process(frame)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            if first:
                for id, lm in enumerate(hand.landmark):
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (x, y), 3, violet, cv2.FILLED)
                    if id == 8:
                        x_8, y_8 = x, y
                        move_cursor(x_8, y_8)
                    first = False
            else:
                for id, lm in enumerate(hand.landmark):
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (x, y), 3, green, cv2.FILLED)
                    if id == 4:
                        x_4, y_4 = x, y

                    if id == 12 and abs(x - x_4) <= 20 and abs(y - y_4) <= 15:
                        left_double_click(x_8, y_8)
                    if id == 8 and abs(x - x_4) <= 20 and abs(y - y_4) <= 15:
                        left_click(x_8, y_8)
                    if id == 16 and abs(x - x_4) <= 20 and abs(y - y_4) <= 15:
                        right_click(x_8, y_8)

                    first = True

    frame = cv2.flip(frame, 1)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

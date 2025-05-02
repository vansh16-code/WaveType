import cv2
import numpy as np
import webbrowser
import mediapipe as mp
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Define keyboard layout
keyboard_keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"]
]

keyboard_text = ""

# Debounce variables
last_click_time = 0
click_cooldown = 0.5  # Set a cooldown period (in seconds) between key presses

def draw_keyboard(img, key_list):
    button_list = []
    x_start = 50
    y_start = 50
    key_w, key_h = 60, 60
    for i, row in enumerate(key_list):
        for j, key in enumerate(row):
            x = x_start + j * (key_w + 10)
            y = y_start + i * (key_h + 10)
            button_list.append((key, (x, y)))
            cv2.rectangle(img, (x, y), (x + key_w, y + key_h), (255, 0, 255), cv2.FILLED)
            cv2.putText(img, key, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
    # Draw SEARCH and BACK buttons
    y_offset = y_start + len(key_list) * (key_h + 10)
    search_x = 50
    back_x = 250
    cv2.rectangle(img, (search_x, y_offset), (search_x + 150, y_offset + key_h), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, "SEARCH", (search_x + 10, y_offset + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.rectangle(img, (back_x, y_offset), (back_x + 150, y_offset + key_h), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, "BACK", (back_x + 30, y_offset + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    button_list.append(("SEARCH", (search_x, y_offset)))
    button_list.append(("BACK", (back_x, y_offset)))
    return img, button_list

def main():
    global keyboard_text, last_click_time

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        img, button_list = draw_keyboard(img, keyboard_keys)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((cx, cy))
                if lm_list:
                    x1, y1 = lm_list[8]  # Index finger tip
                    x2, y2 = lm_list[12] # Middle finger tip
                    thumb_x, thumb_y = lm_list[4]  # Thumb tip
                    
                    cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

                    # Calculate distance between index and thumb (for click gesture)
                    distance_thumb_index = np.sqrt((x1 - thumb_x) ** 2 + (y1 - thumb_y) ** 2)

                    # Check for "click" gesture (if the thumb and index fingers are close)
                    if distance_thumb_index < 30:  # Adjust this threshold for your needs
                        current_time = time.time()
                        # Only register a click if enough time has passed (debounce)
                        if current_time - last_click_time > click_cooldown:
                            for key, (x, y) in button_list:
                                if x < x1 < x + 60 and y < y1 < y + 60:
                                    cv2.rectangle(img, (x, y), (x + 60, y + 60), (0, 255, 0), cv2.FILLED)
                                    cv2.putText(img, key, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

                                    if key == "SEARCH":
                                        webbrowser.open(f"https://www.google.com/search?q={keyboard_text}")
                                        keyboard_text = ""
                                    elif key == "BACK":
                                        keyboard_text = keyboard_text[:-1]
                                    else:
                                        keyboard_text += key
                                    last_click_time = current_time  # Update the last click time

        # Display typed text
        cv2.rectangle(img, (40, 300), (700, 360), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, keyboard_text, (50, 340), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        cv2.imshow("Virtual Keyboard", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

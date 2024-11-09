import pyautogui
import cv2
import numpy as np
import keyboard
import time

# Capture the screen
def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite('res/table.png', screenshot)
    return screenshot
    

def solve_minesweeper(image, reference_images):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detected_elements = []

    for key, template in reference_images.items():
        res = cv2.matchTemplate(gray, cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            detected_elements.append((key, pt))
  
    print('detect image success')
    # Create a grid to represent the game board
    grid = {}
    for element in detected_elements:
        key, (x, y) = element
        grid[(x, y)] = key

    moves = []
    if detected_elements:
      print(detected_elements[0])
    for (x, y), value in grid.items():
        if value.isdigit():
            num = int(value)
            neighbors = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
            closed_neighbors = [n for n in neighbors if grid.get(n) == 'closed']
            # print(neighbors)
            print('closed neighbour', closed_neighbors)
            if len(closed_neighbors) == num:
                moves.extend(closed_neighbors)

    print('moves detected', moves)

    # if all closed do random click
    # if not moves:
    #   closed_tiles = [pos for pos, val in grid.items() if val == 'closed']
    #   if closed_tiles:
    #       random_closed_tile = closed_tiles[np.random.randint(len(closed_tiles))]
    #       print('random click',random_closed_tile)
    #       moves.append(random_closed_tile)

    return moves


def perform_clicks(moves):
    for move in moves:
        x, y = move
        pyautogui.click(x, y)
        

def main():
    # Load the reference images for numbers and tiles
    reference_images = {
      '1': cv2.imread('res/1.png'),
      '2': cv2.imread('res/2.png'),
      '3': cv2.imread('res/3.png'),
      'closed': cv2.imread('res/close-tile.png'),
    }
    
    while True:
        if keyboard.is_pressed('a'):
            print("Solver started")
            while not keyboard.is_pressed('b'):
                screenshot = capture_screen()
                moves = solve_minesweeper(screenshot, reference_images)
                perform_clicks(moves)
                for _ in range(50):  # Check for 'b' key press every 0.1 seconds for 5 seconds
                    if keyboard.is_pressed('b'):
                        print("Solver stopped")
                        return
                    time.sleep(0.1)
            print("Solver stopped")
            break

if __name__ == "__main__":
    main()
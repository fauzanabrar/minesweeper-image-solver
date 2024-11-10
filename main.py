# Description: This script is a Minesweeper solver that uses OpenCV to detect the game board and the elements on it.

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
    

def detect_elements(screenshot, reference_images):
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    detected_elements = []

    for key, template in reference_images.items():
        res = cv2.matchTemplate(gray, cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        
        template_height, template_width = template.shape[:2]
        detected_mask = np.zeros_like(gray, dtype=np.uint8)

        for pt in zip(*loc[::-1]):
            element_center = (pt[0] + template_width // 2, pt[1] + template_height // 2)
            
            # Check if the center is within an already detected region
            if detected_mask[pt[1]:pt[1] + template_height, pt[0]:pt[0] + template_width].sum() == 0:
                detected_elements.append((key, element_center))
                # Mark this region as detected
                detected_mask[pt[1]:pt[1] + template_height, pt[0]:pt[0] + template_width] = 1

    return detected_elements
    
def positions_are_close(pos1, pos2, tolerance=3):
    return np.allclose(pos1, pos2, atol=tolerance)


def solve_minesweeper(detected_elements, reference_images):
    # Create a grid to represent the game board
    grid = {}
    for element in detected_elements:
        key, (x, y) = element
        grid[(x, y)] = key

    moves = []
    
    # print('Closed tiles:', [pos for pos, val in grid.items() if val == 'closed'])
    # number_tiles = [(pos, val) for pos, val in grid.items() if val.isdigit()]
    # print('Number tiles:', number_tiles)

    for (x, y), value in grid.items():
        bombs = []
        if value.isdigit():
            num = int(value)
            tile_size = reference_images['closed'].shape[1]
            neighbors = [(x + dx * tile_size, y + dy * tile_size) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
            
            closed_neighbors = [n for n in neighbors if any(positions_are_close(n, key) and grid[key] == 'closed' for key in grid)]
            flagged_neighbors = [n for n in neighbors if any(positions_are_close(n, key) and grid[key] == 'flag' for key in grid)]
            # print('closed_neighbors length', len(closed_neighbors), 'flagged_neighbors length', len(flagged_neighbors), 'num', num)

            # detect the bomb
            if len(closed_neighbors) == num:
                for neighbor in closed_neighbors:
                    if neighbor not in bombs:
                        # check if it flagged already
                        if neighbor not in flagged_neighbors:
                            perform_clicks([neighbor], button='right')
                            bombs.append(neighbor)

            if len(flagged_neighbors) == num:
                for neighbor in closed_neighbors:
                    if neighbor not in moves:
                        moves.append(neighbor)
        
        # TODO detect the bomb and flag it
        # TODO click the non flag tile if bomb has been detected

    print('moves', moves)

    # if all closed do random click
    if not moves:
        number_tiles = [pos for pos, val in grid.items() if val.isdigit()]

        if not number_tiles:
            closed_tiles = [pos for pos, val in grid.items() if val == 'closed']
            if closed_tiles:
                random_closed_tile = closed_tiles[np.random.randint(len(closed_tiles))]
                # moves.append(random_closed_tile)
                perform_clicks([random_closed_tile], button='left')
                print('random click at', random_closed_tile)
        

    return moves


def perform_clicks(moves, button='left'):
    for move in moves:
        x, y = move
        pyautogui.click(x, y, button=button)
        

def main():
    # Load the reference images for numbers and tiles
    reference_images = {
      '1': cv2.imread('res/1.png'),
      '2': cv2.imread('res/2.png'),
      '3': cv2.imread('res/3.png'),
      '4': cv2.imread('res/4.png'),
      'closed': cv2.imread('res/close-tile.png'),
      'flag': cv2.imread('res/flag.png')
    }
    
    while True:
        if keyboard.is_pressed('a'):
            print("Solver started")
            while not keyboard.is_pressed('b'):
                screenshot = capture_screen()
                detected_elements = detect_elements(screenshot, reference_images)
                moves = solve_minesweeper(detected_elements, reference_images)
                perform_clicks(moves)
                for _ in range(40):  # Check for 'b' key press every 0.1 seconds for 5 seconds
                    if keyboard.is_pressed('b'):
                        print("Solver stopped")
                        return
                    time.sleep(0.1)
            print("Solver stopped")
            break

if __name__ == "__main__":
    main()
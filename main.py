# Description: This script is a Minesweeper solver that uses OpenCV to detect the game board and the elements on it.

import pyautogui
import cv2
import numpy as np
import keyboard
import time
import threading

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

def filter_moves(moves, min_distance=2):
    filtered_moves = []
    for move in moves:
        if all(np.linalg.norm(np.array(move[:2]) - np.array(existing_move[:2])) >= min_distance for existing_move in filtered_moves):
            filtered_moves.append(move)
    return filtered_moves

def solve_minesweeper(detected_elements, reference_images):
    moves = []
    bombs = [] 

    grid = {}

    for element in detected_elements:
        key, (x, y) = element
        grid[(x, y)] = key


    for (x, y), value in grid.items():
        if value.isdigit():
            num = int(value)
            tile_size = reference_images['closed'].shape[1]
            neighbors = [(x + dx * tile_size, y + dy * tile_size) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
            
            closed_neighbors = [n for n in neighbors if any(positions_are_close(n, key) and grid[key] == 'closed' for key in grid)]
            flagged_neighbors = [n for n in neighbors if any(positions_are_close(n, key) and grid[key] == 'flag' for key in grid)]

            all_neighbors = closed_neighbors + flagged_neighbors

            if len(flagged_neighbors) == num:
                for neighbor in closed_neighbors:
                    if neighbor not in moves:
                        moves.append((neighbor[0], neighbor[1], 'left'))
            # detect the bomb
            elif len(all_neighbors) == num:
                for neighbor in closed_neighbors:
                    if neighbor not in bombs:
                        # check if it flagged already
                        if neighbor not in flagged_neighbors:
                            moves.append((neighbor[0], neighbor[1], 'right'))
                            bombs.append(neighbor)

        
        # TODO fix bomb and flag bug

    print('moves', moves)

    # if all closed do random click
    if not moves:
        closed_tiles = [pos for pos, val in grid.items() if val == 'closed']
        if closed_tiles:
            random_closed_tile = closed_tiles[np.random.randint(len(closed_tiles))]
            moves.append((random_closed_tile[0], random_closed_tile[1], 'left'))
            print('random click at', random_closed_tile)

    return moves


def perform_clicks(moves):
    for move in moves:
        x, y, button = move
        pyautogui.click(x, y, button=button)


solver_running = False
stop_program = False

def key_listener():
    global solver_running, stop_program
    while True:
        if keyboard.is_pressed('a'):
            solver_running = not solver_running
            if solver_running:
                print("Solver started")
            else:
                print("Solver stopped")
            time.sleep(0.2)  # Add a small delay to debounce the key press

        if keyboard.is_pressed('b'):
            solver_running = False
            stop_program = True
            print("Program quitting")
            exit()

        time.sleep(0.05)  # Reduce the sleep duration to make the loop more responsive


def main():
    global solver_running
    threading.Thread(target=key_listener, daemon=True).start()

    # Load the reference images for numbers and tiles
    reference_images = {
        '1': cv2.imread('res/1.png'),
        '2': cv2.imread('res/2.png'),
        '3': cv2.imread('res/3.png'),
        '4': cv2.imread('res/4.png'),
        'closed': cv2.imread('res/close-tile.png'),
        'flag': cv2.imread('res/flag.png')
    }

    while not stop_program:
        if solver_running:
            screenshot = capture_screen()
            detected_elements = detect_elements(screenshot, reference_images)
            moves = solve_minesweeper(detected_elements, reference_images)
            filtered_moves = filter_moves(moves)
            perform_clicks(filtered_moves)

        time.sleep(1)
if __name__ == "__main__":
    main()


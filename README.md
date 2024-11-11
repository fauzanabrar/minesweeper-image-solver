# Minesweeper Image Detection Solver

This program was created to solve Minesweeper using image detection. It captures the screen, detects the Minesweeper board and elements, and performs the necessary moves to solve the game.

## Features

- **Screen Capture**: Captures the screen to detect the Minesweeper board.
- **Image Detection**: Uses OpenCV to detect elements on the board.
- **Automated Moves**: Automatically performs clicks to solve the game.
- **Keyboard Controls**: Start, stop, and quit the solver using keyboard inputs.

## Requirements

- Python 3.6+
- OpenCV
- MSS
- Numpy
- PyAutoGUI
- Keyboard

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fauzanabrar/minesweeper-image-solver.git
    cd minesweeper-image-solver
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure the Minesweeper game is open and visible on your screen.
2. Run the script:
    ```sh
    python main.py
    ```
3. Set the crop size for faster the process, change it on ``main.py``:
    ```python
    original_width = 1920
    original_height = 1080
    cropped_x = 260
    cropped_y = 150
    cropped_width = 545 - cropped_x
    cropped_height = 440 - cropped_y
    ```
3. Use the following keyboard controls:
    - Press `a` to start/stop the solver.
    - Press `b` to quit the program.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

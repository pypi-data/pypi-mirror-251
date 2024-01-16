import pygame
import random
import argparse
import webbrowser

class GameOfLife:
    def __init__(self, width, height, tile_size, fps):
        pygame.init()

        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid_width = width // tile_size
        self.grid_height = height // tile_size
        self.fps = fps

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.background_color = (40, 60, 80)
        self.cell_outline_color = (100, 100, 100)
        self.cell_colors = [(255, 170, 170), (170, 255, 170), (170, 170, 255)]

        self.running = True
        self.playing = False
        self.count = 0
        self.update_freq = 20

        self.positions = set()
        self.positions.add((10, 10))

        # Additional color palette for more organic colors
        self.cell_colors = [(200, 50, 50), (50, 200, 50), (50, 50, 200)]

        # Additional color variations for cell outlines
        self.outline_colors = [(150, 150, 150), (120, 120, 120), (100, 100, 100)]

        # Additional variable for smooth transitions
        self.transition_alpha = 255

    # Gosper glider gun
    def fire_glider_gun(self):
        gun_center = (random.randint(5, self.grid_width - 5), random.randint(5, self.grid_height - 5))

        # Randomize the direction of the glider gun
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        gun_coords = [
            (0, 4), (0, 5), (1, 4), (1, 5),
            (10, 4), (10, 5), (10, 6), (11, 3), (11, 7),
            (12, 2), (12, 8), (13, 2), (13, 8),
            (14, 5),
            (15, 3), (15, 7),
            (16, 4), (16, 5), (16, 6),
            (17, 5),
            (20, 2), (20, 3), (20, 4),
            (21, 2), (21, 3), (21, 4),
            (22, 1), (22, 5),
            (24, 0), (24, 1), (24, 5), (24, 6),
            (34, 2), (34, 3), (35, 2), (35, 3)
        ]

        gun_positions = set()
        for coord in gun_coords:
            x, y = coord
            gun_positions.add((gun_center[0] + x * direction[0], gun_center[1] + y * direction[1]))

        return gun_positions

    def draw_grid(self):
        self.screen.fill(self.background_color)

        for position in self.positions:
            col, row = position
            center = (col * self.tile_size + self.tile_size // 2, row * self.tile_size + self.tile_size // 2)

            # Randomize cell color from a palette of organic colors
            cell_color = (
                random.randint(150, 200),  # Red
                random.randint(200, 255),  # Green
                random.randint(150, 200)  # Blue
            )

            # Randomize radius for an organic look
            radius = self.tile_size // 2 + random.randint(-2, 2)

            # Draw cell as a circle with a slightly randomized radius
            pygame.draw.circle(self.screen, cell_color, center, radius)

            # Add some randomness to the cell shape
            for _ in range(2):
                offset = random.randint(-2, 2)
                pygame.draw.circle(self.screen, self.cell_outline_color,
                                   (center[0] + offset, center[1] + offset),
                                   radius + offset, 1)

        pygame.display.update()

    def adjust_grid(self):
        all_neighbours = set()
        new_positions = set()

        for position in self.positions:
            neighbors = self.get_neighbors(position)
            all_neighbours.update(neighbors)

            neighbors = list(filter(lambda x: x in self.positions, neighbors))

            if len(neighbors) in [2, 3]:
                new_positions.add(position)

        for position in all_neighbours:
            neighbors = self.get_neighbors(position)
            neighbors = list(filter(lambda x: x in self.positions, neighbors))

            if len(neighbors) == 3:
                new_positions.add(position)

        return new_positions

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []

        for dx in [-1, 0, 1]:
            if 0 <= x + dx < self.grid_width:
                for dy in [-1, 0, 1]:
                    if 0 <= y + dy < self.grid_height and not (dx == 0 and dy == 0):
                        neighbors.append((x + dx, y + dy))

        return neighbors

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)

            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def handle_mouse_click(self, event):
        x, y = pygame.mouse.get_pos()
        col = x // self.tile_size
        row = y // self.tile_size
        pos = (col, row)

        if event.button == 1:  # Left click
            if pos in self.positions:
                self.positions.remove(pos)
            else:
                self.positions.add(pos)

        elif event.button == 3:  # Right click
            if pos in self.positions:
                self.positions.remove(pos)

    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.playing = not self.playing

        elif event.key == pygame.K_c:
            self.positions = set()
            self.playing = False
            self.count = 0

        elif event.key == pygame.K_g:
            self.positions = self.generate_cells(random.randrange(4, 10) * self.grid_width)

    def generate_cells(self, num):
        return set([(random.randrange(0, self.grid_height), random.randrange(0, self.grid_width)) for _ in range(num)])

    def run(self):

        while self.running:
            self.clock.tick(self.fps)

            if self.playing:
                self.count += 1

            next_glider_fire = random.randint(0, 20)

            if self.count >= self.update_freq:
                if abs(next_glider_fire - self.count) > 15:
                    self.positions.update(self.fire_glider_gun())
                self.count = 0
                self.positions = self.adjust_grid()

            pygame.display.set_caption("Playing" if self.playing else "Paused")

            self.handle_events()
            self.draw_grid()

            pygame.display.update()

        pygame.quit()

def parse_args():
    parser = argparse.ArgumentParser(description="Conway's Game of Life with Gosper Glider Gun")

    parser.add_argument('--i', action='store_true', help='Open GitHub README in a web browser (Requires internet)')

    return parser.parse_args()

# conway-engine/simulation.py

def main():
    args = parse_args()

    if args.i:
        webbrowser.open('https://github.com/vivekkdagar/conway_engine/blob/main/README.md')
        return
        
    game = GameOfLife(800, 800, 20, 60)
    game.run()

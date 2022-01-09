import pygame
import numpy as np
import time
from data_analyzer import DataAnalyzer

col_about_to_die = (200, 200, 225)
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 30)


class GameOfLife:
    def __init__(self, **kwargs):
        self.dim_x = kwargs["dimension_x"]
        self.dim_y = kwargs["dimension_y"]
        self.cell_sie = kwargs["cell_size"]
        self.cycle_timer = kwargs["cycle_duration"]
        self.is_life_span_qm = kwargs["is_life_span"]
        self.life_span = kwargs["cell_lifetime"]
        self.life_span_type = kwargs["evolution_type"]

        self.game_cells = None
        self.surface = None
        self.cell_size = None
        self.next_iteration = None
        self.previous_game_cells = None
        self.data_stats = {"Generatie": [], "Populatie": []}
        self.generation = 0
        self.population = 0
        self.lifspan_cells = np.zeros((self.dim_y, self.dim_x))

    def init_game(self):
        cells = np.zeros((self.dim_y, self.dim_x))
        pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]);

        self.population = np.count_nonzero(pattern == 1)
        self.generation += 1

        pos = (3, 3)
        cells[pos[0]:pos[0] + pattern.shape[0], pos[1]:pos[1] + pattern.shape[1]] = pattern
        self.game_cells = cells
        self.previous_game_cells = cells

    def update(self):
        nxt = np.zeros((self.game_cells.shape[0], self.game_cells.shape[1]))

        for r, c in np.ndindex(self.game_cells.shape):
            num_alive = np.sum(self.game_cells[r - 1:r + 2, c - 1:c + 2]) - self.game_cells[r, c]

            if self.game_cells[r, c] == 1 and num_alive < 2 or num_alive > 3:
                col = col_about_to_die
            elif (self.game_cells[r, c] == 1 and 2 <= num_alive <= 3) or (self.game_cells[r, c] == 0 and num_alive == 3):
                nxt[r, c] = 1
                col = col_alive

            col = col if self.game_cells[r, c] == 1 else col_background
            pygame.draw.rect(self.surface, col, (c * self.cell_sie, r * self.cell_sie, self.cell_sie - 1, self.cell_sie - 1))

        self.population = np.count_nonzero(nxt == 1)
        self.generation += 1
        self.previous_game_cells = self.game_cells
        self.game_cells = nxt

    def check_life_span(self):
        for (current_row, current_col), (old_row, old_col) in zip(np.ndindex(self.game_cells.shape),
                                                                  np.ndindex(self.previous_game_cells.shape)):
            if self.game_cells[current_row, current_col] == 1 and self.game_cells[old_row, old_col] == 1:
                if self.lifspan_cells[current_row, current_col] > self.life_span:

                    pygame.draw.rect(self.surface, col_about_to_die,
                                     (current_col * self.cell_sie, current_row * self.cell_sie, self.cell_sie - 1,
                                      self.cell_sie - 1))
                    if self.life_span_type == "Kill_and_spawn":
                        self.game_cells[current_row][current_col] = 0
                        self.game_cells[current_row + 1][current_col + 1] = 1
                    elif self.life_span_type == "kill":
                        self.game_cells[current_row][current_col] = 0
                    elif self.life_span_type == "spawn":
                        self.game_cells[current_row + 1][current_col + 1] = 1
                    else:
                        raise RuntimeError("Kill_and_spawn / kill / spawn!")
                else:
                    self.lifspan_cells[current_row, current_col] += 1

    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.dim_x * self.cell_sie, self.dim_y * self.cell_sie))
        pygame.display.set_caption("John Conway's Game of Life")

        self.init_game()

        while True:
            self.update_data_set()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.output_data()
                    return

            self.surface.fill(col_grid)
            if self.is_life_span_qm:
                self.check_life_span()
            self.update()
            pygame.display.update()
            time.sleep(self.cycle_timer)

    def update_data_set(self):
        self.data_stats["Generatie"].append(self.generation)
        self.data_stats["Populatie"].append(self.population)

    def output_data(self, skip_step=0):
        data_writer = DataAnalyzer()
        if skip_step == 0:
            data_writer.write(self.data_stats)
        else:
            temp_data = {"Generatie": self.data_stats["Generatie"][::skip_step],
                         "Populatie": self.data_stats["Populatie"][::skip_step]}
            data_writer.write(temp_data)


if __name__ == "__main__":
    GOLobj = GameOfLife(dimension_x=120, dimension_y=90, cell_size=8, cycle_duration=0.1, is_life_span=True,
                        evolution_type="spawn", cell_lifetime=5)
    GOLobj.run()

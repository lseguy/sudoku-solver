import random
import threading

import dearpygui.dearpygui as dpg
import solver
from grid import Grid


GRID_SIZE = 400
FONT_SIZE = 45
CELL_V_PADDING = 1
CELL_H_PADDING = 11


class Gui:
    def __init__(self, grid=None):
        if grid:
            self._grid = grid
        else:
            self._load_new_random_grid()

        self._draw_list = None
        self._solver_lock = threading.Lock()

    def start_gui(self):
        dpg.create_context()

        with dpg.font_registry():
            dpg.add_font('fonts/Roboto-Regular.ttf', FONT_SIZE, tag='font_grid')

        self._display_grid()
        self._display_controls()
        #dpg.set_primary_window('window_grid', True)

        dpg.create_viewport(title='Sudoku Solver', width=GRID_SIZE+50, height=GRID_SIZE+50)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            self._refresh_grid()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def _load_new_random_grid(self, filename='data/35-numbers.txt'):
        with open(filename) as f:
            line_count = sum(1 for _ in f)
            if line_count < 1:
                raise Exception('The file is empty')

            f.seek(0)
            lines_to_skip = random.randrange(line_count - 1)
            for i in range(lines_to_skip):
                next(f)

            data = f.readline().strip()
            self._grid = Grid.from_data(data)

    def _random_grid_callback(self):
        if not self._solver_lock.locked():
            self._load_new_random_grid()
            self._display_grid()

    def _solve(self):
        if self._solver_lock.acquire(blocking=False):
            solver.solve(self._grid, sleep_time=0.007)
            self._solver_lock.release()
        else:
            print('already running')

    def _solve_callback(self):
        threading.Thread(target=self._solve).start()

    def _refresh_grid(self):
        for row in range(9):
            for col in range(9):
                number = self._grid.get_number(row, col)
                if number:
                    self._display_number(row, col, number)

    def _display_number(self, row, column, value, color=(0, 0, 0)):
        tag = f'number_{row}_{column}'

        # First delete the number if it already exists
        if dpg.does_item_exist(tag):
            dpg.delete_item(tag)

        offset = GRID_SIZE / 9
        x = column * offset + CELL_H_PADDING
        y = row * offset + CELL_V_PADDING

        tag = dpg.draw_text((x, y), value, size=FONT_SIZE, color=color, tag=tag, parent=self._draw_list)
        dpg.bind_item_font(tag, 'font_grid')

    def _display_grid(self):
        if dpg.does_item_exist('window_grid'):
            dpg.delete_item('window_grid')

        with dpg.window(label='Sudoku Grid', tag='window_grid', no_resize=True, autosize=True):
            with dpg.drawlist(width=GRID_SIZE, height=GRID_SIZE) as draw_list:
                self._draw_list = draw_list
                dpg.draw_rectangle((0, 0), (GRID_SIZE, GRID_SIZE), color=(0, 0, 0), fill=(255, 255, 255))

                offset = GRID_SIZE / 9
                for i in range(1, 9):
                    thickness = 3 if i % 3 == 0 else 1

                    dpg.draw_line((i*offset, 0), (i*offset, GRID_SIZE), color=(0, 0, 0), thickness=thickness)
                    dpg.draw_line((0, i*offset), (GRID_SIZE, i*offset), color=(0, 0, 0), thickness=thickness)

                for row in range(9):
                    for col in range(9):
                        number = self._grid.get_number(row, col)
                        if number:
                            self._display_number(row, col, number)

    def _display_controls(self):
        with dpg.window(label='Controls', tag='window_controls', autosize=True):
            dpg.add_button(label='Solve', tag='button_solve', callback=self._solve_callback)
            dpg.add_button(label='Random grid', tag='button_random_grid', callback=self._random_grid_callback)

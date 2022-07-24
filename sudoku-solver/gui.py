import dearpygui.dearpygui as dpg
from grid import Grid


GRID_SIZE = 400
FONT_SIZE = 45
CELL_V_PADDING = 1
CELL_H_PADDING = 11


def start_gui(grid: Grid):
    dpg.create_context()

    with dpg.font_registry():
        dpg.add_font('fonts/Roboto-Regular.ttf', FONT_SIZE, tag='grid_font')

    _display_grid(grid)
    dpg.set_primary_window('primary', True)

    dpg.create_viewport(title='Sudoku Solver', width=GRID_SIZE+50, height=GRID_SIZE+50)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.start_dearpygui()
    dpg.destroy_context()


def _display_grid(grid: Grid):
    with dpg.window(label='Sudoku Grid', tag='primary', no_resize=True, autosize=True):
        with dpg.drawlist(width=GRID_SIZE, height=GRID_SIZE):
            dpg.draw_rectangle((0, 0), (GRID_SIZE, GRID_SIZE), color=(0, 0, 0), fill=(255, 255, 255))

            offset = GRID_SIZE / 9
            for i in range(1, 9):
                thickness = 3 if i % 3 == 0 else 1

                dpg.draw_line((i*offset, 0), (i*offset, GRID_SIZE), color=(0, 0, 0), thickness=thickness)
                dpg.draw_line((0, i*offset), (GRID_SIZE, i*offset), color=(0, 0, 0), thickness=thickness)

            for row in range(9):
                for col in range(9):
                    number = grid.get_number(row, col)
                    if number != 0:
                        x = col * offset + CELL_H_PADDING
                        y = row * offset + CELL_V_PADDING

                        text = dpg.draw_text((x, y), number, size=FONT_SIZE, color=(0, 0, 0))
                        dpg.bind_item_font(text, 'grid_font')

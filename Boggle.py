from BoggleGUI import BoggleGUI
from BoggleModel import BoggleModel
from ex12_utils import load_words_dict
from boggle_board_randomizer import randomize_board, BOARD_SIZE


TIMER = 3 * 60
# TIMER = 3
INIT_BOARD = [[''] * BOARD_SIZE] * BOARD_SIZE


def cell_string_to_tuple(cell_str):
    cell = cell_str.split(',')
    return int(cell[0]), int(cell[1])


class BoggleController:
    def __init__(self, words):
        self._model = BoggleModel(words, INIT_BOARD)
        self._gui = BoggleGUI(self._model, TIMER, INIT_BOARD)

        self._gui.set_enter_command(self.get_enter_action())
        self._gui.set_start_command(self.get_start_action())

    def get_enter_action(self):
        def wrapper():
            self._model.submit_word()
            self._gui.display_chosen_word(self._model.get_cur_word())
            self._gui.display_words(self._model.get_found_words())
            self._gui.display_score(self._model.get_score())
        return wrapper

    def get_start_action(self):
        def wrapper():
            new_board = randomize_board()
            self._model.reset_model(new_board)
            self._gui.reset_gui(new_board)
            self.reset_buttons()
            self._gui.display_words(self._model.get_found_words())
            self._gui.display_score(self._model.get_score())
            if not self._model.get_game_on():
                self._gui.change_to_restart()
                self._model.start_game()
                self._gui.countdown()
        return wrapper

    def create_cell_action(self, button_cell: str):
        def wrapper() -> None:
            if not self._model.get_game_on():
                return
            cell_tpl = cell_string_to_tuple(button_cell)
            cell_valid = self._model.cell_clicked(cell_tpl)
            if not cell_valid:
                # do something.. ?
                return
            self._gui.display_chosen_word(self._model.get_cur_word())
        return wrapper

    def reset_buttons(self):
        for button_cell in self._model.get_all_cells():
            i, j = button_cell
            cell_str = str(i) + "," + str(j)
            action = self.create_cell_action(cell_str)
            self._gui.set_cell_command(cell_str, action)

    def run(self):
        self._gui.run()


def main():
    brd = [['A', 'R', 'A', 'QU'], ['D', 'F', 'Y', 'S'], ['A', 'W', 'N', 'E'],
           ['D', 'R', 'A', 'I']]
    brd2 = randomize_board()
    some_words = load_words_dict("boggle_dict.txt")

    BoggleController(some_words).run()


if __name__ == "__main__":
    main()

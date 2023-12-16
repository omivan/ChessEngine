from PIL import Image
import os


class ChessBoardGenerator:
    def __init__(self, fen_pos=None, board_style='wood4', figures_style='merida'):
        self.figures = None
        self.fen_pos = None
        self.start_pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.set_fen_pos(fen_pos)

        images_dir = 'Images'
        self.board_dir = os.path.join(images_dir, 'board')
        self.board_style = board_style
        self.figures_style = figures_style
        # board_style += '.jpg'
        self.figures_dir = os.path.join(images_dir, 'figures')
        # figures_style = 'merida'
        self.figures_array = 'PNBRQKpnbrqk'
        self.figures_names_in_files = {
            'P': 'wP.png', 'p': 'bP.png',
            'N': 'wN.png', 'n': 'bN.png',
            'B': 'wB.png', 'b': 'bB.png',
            'R': 'wR.png', 'r': 'bR.png',
            'Q': 'wQ.png', 'q': 'bQ.png',
            'K': 'wK.png', 'k': 'bK.png'
        }

    def set_fen_pos(self, fen_pos=None):
        if fen_pos is None:
            fen_pos = self.start_pos
        self.fen_pos = fen_pos
        self.figures = fen_pos.split()[0]

    def get_style_sample(self, figure_style=None, board_style=None, save_to='sample.png', show_im=False):
        self.generate_picture(figure_style, board_style, position=self.start_pos, save_to=save_to, show_im=show_im)

    def get_all_board_styles(self):
        delete_file_extentions = lambda x: ''.join(x.split('.')[:-1])
        return list(map(delete_file_extentions, os.listdir(self.board_dir)))

    def get_this_style(self):
        return {
            'board': self.board_style,
            'figures': self.figures_style
        }

    def set_styles_from_dictionary(self, dic):
        self.set_figures_style(dic['pieces'])
        self.set_board_style(dic['board'])

    def set_figures_style(self, style):
        if style is not None:
            self.figures_style = style

    def set_board_style(self, style):
        if style is not None:
            self.board_style = style

    def get_all_figures_styles(self):
        # ATTENTION!!!!!!    hardcode
        not_styles = ['svg', 'svg_to_png.py']
        # ---------------------------------
        styles = os.listdir(self.figures_dir)
        for i in not_styles:
            styles.remove(i)
        return styles

    def generate_picture(self, figures_style=None, board_style=None, position=None,
                         is_save=True, save_to='chess_position.png', show_im=False):
        if figures_style is None:
            figures_style = self.figures_style
        if board_style is None:
            board_style = self.board_style
        board_style += '.jpg'
        if position is None:
            position = self.figures

        path_to_figure_images = {
            'board': os.path.join(self.board_dir, board_style),
        }
        for i in self.figures_array:
            path_to_figure_images[i] = \
                (os.path.join(self.figures_dir, figures_style, self.figures_names_in_files[i]))

        # Load your chessboard image
        chessboard = Image.open(path_to_figure_images['board']).convert('RGBA')
        chessboard = chessboard.resize((1024, 1024))
        chessboard_size = chessboard.size
        square_size = int(chessboard_size[0] / 8), int(chessboard_size[1] / 8)

        iterator = 0
        for i in position:
            if i in self.figures_array:
                piece = Image.open(path_to_figure_images[i])
                piece = piece.resize(square_size)
                piece.alpha_composite(piece)

                row, column = iterator % 8, iterator // 8
                chessboard.paste(piece, (row * square_size[0], column * square_size[1]), piece)
                iterator += 1
            elif i == '/':
                continue
            else:
                iterator += int(i)

        # Save the resulting image
        if is_save:
            chessboard.save(save_to)
        if show_im:
            chessboard.show()


if __name__ == '__main__':
    start_pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    gener = ChessBoardGenerator(start_pos)
    gener.get_style_sample(figure_style='tatiana', board_style='maple2.orig', show_im=True)
    print(gener.get_all_figures_styles())
    print(gener.get_all_board_styles())

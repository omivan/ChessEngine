import os
from cairosvg import svg2png
import shutil


def main():
    dir_with_svg_dirs = 'svg'
    for i in os.listdir(dir_with_svg_dirs):
        if not os.path.exists(i):
            os.mkdir(i)
        figures_path = os.path.join(dir_with_svg_dirs, i)
        for j in os.listdir(figures_path):
            old_figure_path = os.path.join(figures_path, j)
            if j.endswith('.png'):
                shutil.copy(old_figure_path, os.path.join(i, j))
                continue
            figure_name_png = j.replace('svg', 'png')
            svg2png(url=old_figure_path, write_to=os.path.join(i, figure_name_png))


if __name__ == '__main__':
    main()

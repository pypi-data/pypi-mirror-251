import click
from .functions import EquationAnimation, copy_animation
from manim import config


bg_path = "Users/vaihavblayer/10xphysics/backgrounds/bg_instagram.jpg"

@click.command(
        help="Converts pdf pages into pngs"
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./solution.tex",
        show_default=True,
        help="Input file name"
        )
@click.option(
        '-t',
        '--tikzfile',
        type=click.Path(),
        default="./tikzpicture.tex",
        show_default=True,
        help="Tikzpicture file name"
        )
def main(inputfile, tikzfile):
    EquationAnimation(file_sol=inputfile, file_tikz=inputfile).render()
    copy_animation(config.pixel_height, config.frame_rate)
    
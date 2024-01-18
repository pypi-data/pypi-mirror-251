import click
from .functions import EquationAnimation, copy_animation
from manim import config


bg_path = "/Users/vaibhavblayer/10xphysics/backgrounds/bg_instagram.jpg"

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
@click.option(
        '-b',
        '--background',
        type=click.Path(),
        default=bg_path,
        show_default=True,
        help="Path of the background image"
        )
def main(inputfile, tikzfile, background):
    EquationAnimation(file_sol=inputfile, file_tikz=tikzfile).render()
    copy_animation(config.pixel_height, config.frame_rate, bg_path=background)
    
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
@click.option(
        '-p',
        '--pixel_height',
        type=int,
        default=1600,
        show_default=True,
        help="Pixel height of the video"
        )
@click.option(
        '-w',
        '--pixel_width',
        type=int,
        default=1600,
        show_default=True,
        help="Pixel width of the video"
        )
@click.option(
        '-f',
        '--frame_rate',
        type=int,
        default=120,
        show_default=True,
        help="Frame rate of the video"
        )
def main(inputfile, tikzfile, background, pixel_height, pixel_width, frame_rate):
    equation = EquationAnimation(file_sol=inputfile, file_tikz=tikzfile)
    equation.pw = pixel_width
    equation.ph = pixel_height
    equation.fr = frame_rate
    equation.render()
    copy_animation(config.pixel_height, config.frame_rate, bg_path=background)
    
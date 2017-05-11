"""This script generates a pdf with multiplikation."""

import argparse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth 
import sys

__version__ = "0.1.0"

""" Changelog.
version  changes
0.1.0    created script
"""

verbosity_level = 0 # pylint: disable=C0103


def check_arg(arguments=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--version', action='store_true')
    parser.add_argument('output_file', nargs='*', default=None)
    parser.set_defaults(version=False)

    return parser.parse_args(arguments)


def multiplikation(output_file):
    """Do the shitnitz"""
    pagesize = A4
    font_name = "Helvetica"
    font_size = 12

    pdf = canvas.Canvas(output_file, pagesize=pagesize)
    pdf.setLineWidth(.3)
    pdf.setFont(font_name, font_size)
    width, height = pagesize

    margin_size = 100

    column_width = (width - 2 * margin_size) / 3
    row_height = (height - 2 * margin_size) / 20

    for row in range(20):
        for column in range(3):
            point_x = column * column_width + margin_size
            point_y = row * row_height + margin_size
            text = "10 x 10"
            text_width = stringWidth(text, font_name, font_size)
            pdf.drawString(point_x, point_y, "10 x 10")
            pdf.line(
                point_x + text_width + 10,
                point_y,
                point_x + column_width - 10,
                point_y)

    pdf.save()
    return 0


def main(arguments):
    """Main function."""
    global verbosity_level # pylint: disable=W0603, C0103

    command_line_options = check_arg(arguments)

    verbosity_level = command_line_options.verbose

    if command_line_options.version:
        print(f"{__file__} version {__version__}")
        print(__doc__)
        return 0

    if not command_line_options.output_file or len(command_line_options.output_file) != 1:
        print("Please specify output file.")
        return -2

 #  if not command_line_options.input or len(command_line_options.input) != 1:
 #  print("Please specify one input file.")
 #  print(f"command_line_options.input={command_line_options.input}")
 #  return -2

    return multiplikation(command_line_options.output_file[0])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

"""This script generates a pdf with multiplikation."""

import argparse
from random import Random
import sys
from time import time
from os.path import isfile, splitext
from reportlab.lib.pagesizes import A4 #, LETTER
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

__version__ = "0.2.0"

""" Changelog.
version  changes
0.1.0    created script
0.2.0    added random(weighted) factors
         added header and footer
         automatically setting output file name
"""

verbosity_level = 0 # pylint: disable=C0103


class MyRandom(Random):
    """Stupid class just to be able to get the seed value, which doesnt work anyway"""
    def __init__(self, x):
        Random.__init__(self, x)

    def seed(self, a=None, version=2):
        self.the_seed = a
        super(MyRandom, self).seed(a, version)

    def get_seed(self):
        """Return the seed used when initializing."""
        return self.the_seed


def get_factor_weight(factor):
    """Factors weighted..."""

    weight = 16

    if factor == 0:
        weight = 4
    elif factor == 1:
        weight = 5
    elif factor == 2:
        weight = 10
    elif factor % 10 == 0:
        weight = 10
    elif factor == 3:
        weight = 15
    elif factor == 4:
        weight = 15
    elif factor == 5:
        weight = 13

    return weight


def get_factor(factor_min, factor_max, prng):
    """get a random factor between factor_min and factor_max inclusive, using weighted factors

    factor weight             accumulated factor weight
    ^   #                     ^      34
    |   #                     |    19#
    |  ##                     |    # #
    |  ##                     |    # #
    |  ##                     |    # #
    |  ##                     |    # #
    |  ##                     |    # #
    | ###                     |  9 # #
    |####                     |  # # #
    |####                     |4 # # #
    |####                     |# # # #
    |####                     |# # # #
    --------> factor          --------> factor
     0123                      0 1 2 3

     get a random value between 1 and weight sum of max factor
     if v <= 4 -> factor is 0
     elif v <= 9 -> factor is 1
     elif v <= 10 -> factor is 2
     ..and so on
    """

    weight_sum = 0

    for factor in range(factor_min, factor_max + 1):
        weight_sum += get_factor_weight(factor)

    # get a random value that is used to find factor
    random_y = prng.randint(1, weight_sum)

    weight_sum = 0
    for factor in range(factor_min, factor_max + 1):
        weight_sum += get_factor_weight(factor)
        if weight_sum >= random_y:
            return factor
    return -1 # shouldn't occur


def check_arg(arguments=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--version', action='store_true')
    parser.add_argument('level', type=int)
    parser.add_argument('--seed', default=int(time()))
    parser.add_argument('output_file', nargs='*', default=None)
    parser.set_defaults(version=False)

    return parser.parse_args(arguments)


def get_multiplication_text(factor1_max, factor2_max, prng):
    """Create text factor x factor
    factor1 is 1.. factor1_max
    factor2 is 0.. factor2_max
    """

    factor1 = get_factor(1, factor1_max, prng)
    factor2 = get_factor(0, factor2_max, prng)

    # multiplication_symbol = u'\u00d7'

    if prng.randint(1, 2) == 1:
        return f"{factor1} \u00d7 {factor2}"
    else:
        return f"{factor2} \u00d7 {factor1}"


def multiplikation(output_file, factor_level, seed, max_factor=10, page_size=A4):
    """Do the shiznit
    factor_level, one of the factors should not be larger than this
    max_factor, the other factor's max
    """
    font_name = "Helvetica"
    font_size = 12
    columns = 4
    rows = 20

    if factor_level > max_factor:
        max_factor = factor_level

    pdf = canvas.Canvas(output_file, pagesize=page_size)
    pdf.setLineWidth(.3)
    pdf.setFont(font_name, font_size)
    width, height = page_size

    margin_size = 100

    column_width = (width - 2 * margin_size) / columns
    row_height = (height - 2 * margin_size) / rows

    spacing = 10

    prng = MyRandom(seed)

    for column in range(columns):
        for row in range(rows):
            point_x = column * column_width + margin_size
            point_y = row * row_height + margin_size
            text = get_multiplication_text(factor_level, max_factor, prng)
            text_width = stringWidth(text, font_name, font_size)
            pdf.drawString(point_x, point_y, text)
            pdf.line(
                point_x + text_width + spacing,
                point_y,
                point_x + column_width - spacing,
                point_y)

    # write header
    header_font_size = 24
    pdf.setLineWidth(1)
    pdf.line(
        margin_size / 2,
        height - margin_size,
        width - margin_size / 2,
        height - margin_size)

    pdf.setFont(font_name, header_font_size)
    text = f"Multiplikation {factor_level}"
    text_width = stringWidth(text, font_name, header_font_size)
    pdf.drawString(width / 2 - text_width / 2, height - margin_size + spacing, text)

    # write footer
    footer_font_size = 10
    pdf.line(
        margin_size / 2,
        margin_size - spacing,
        width - margin_size / 2,
        margin_size - spacing)
    pdf.setFont(font_name, footer_font_size)
    text = f"Multiplikation v{__version__} {{max_factor={max_factor}, seed={seed}}}"
    pdf.drawString(
        margin_size / 2,
        margin_size - spacing - footer_font_size,
        text)

    # add Copyright notice
    copyright_text = "Copyright \u00a9 2017 Patrik Fors"
    text_width = stringWidth(copyright_text, font_name, footer_font_size)
    pdf.drawString(
        width - margin_size / 2 - text_width,
        margin_size - spacing - footer_font_size,
        copyright_text)

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

    if command_line_options.output_file and len(command_line_options.output_file) > 1:
        print("Please specify only one output file.")
        return -2

    if not command_line_options.output_file:
        base_file_name = f"{command_line_options.level}"
    else:
        (base_file_name, _) = splitext(command_line_options.output_file[0])

    if isfile(f"{base_file_name}.pdf"):
        new_base_file_name = f"{base_file_name}0"
        suffix = 1
        while isfile(f"{new_base_file_name}.pdf"):
            new_base_file_name = f"{base_file_name}{suffix}"
            suffix += 1

        print(f"Output file already exist, using {new_base_file_name}.pdf.")
        base_file_name = new_base_file_name

    output_file = f"{base_file_name}.pdf"

 #  if not command_line_options.input or len(command_line_options.input) != 1:
 #  print("Please specify one input file.")
 #  print(f"command_line_options.input={command_line_options.input}")
 #  return -2

    return multiplikation(
        output_file,
        command_line_options.level,
        command_line_options.seed)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

"""This script generates a pdf with multiplikation."""

import argparse

import sys
from time import time
from os.path import isfile, splitext
from reportlab.lib.pagesizes import A4 #, LETTER
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from default_value_list import DefaultValueList
from random_with_seed import RandomWithSeed

__version__ = "0.3.0"

""" Changelog.
version  changes
0.1.0    created script
0.2.0    added random(weighted) factors
         added header and footer
         automatically setting output file name
0.3.0    made sure all terms of selected level occurs at least once
"""

_verbosity_level = 0 # pylint: disable=C0103


COPYRIGHT_TEXT = "Copyright \u00a9 2017 Patrik Fors"
FONT_NAME = "Helvetica"
FONT_SIZE = 12
HEADER_FONT_SIZE = 24
FOOTER_FONT_SIZE = 8
COLUMNS = 4
ROWS = 20
MARGIN_SIZE = 100
SPACING = 10
HEADER_LINE_WIDTH = 1
ANSWER_LINE_WIDTH = .3

FACTOR_PDF = DefaultValueList([4, 5, 10, 15, 15, 13], 16)


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

    # weight_sum = 0

    # for factor in range(factor_min, factor_max + 1):
    #     weight_sum += FACTOR_PDF[factor]

    weight_sum = sum(FACTOR_PDF[factor_min:factor_max + 1])

    # if weight_sum != weight_sum2:
    #     print(f"factor_min={factor_min}")
    #     print(f"factor_max={factor_max}")
    #     print(f"FACTOR_PDF={FACTOR_PDF}")
    #     print(f"weight_sum={weight_sum}, weight_sum2={weight_sum2}")

    # assert weight_sum == weight_sum2

    # get a random value that is used to find factor
    random_y = prng.randint(1, weight_sum)

    if _verbosity_level > 2:
        print(f"FACTOR_PDF={FACTOR_PDF}")
        print(f"random_y = {random_y}")
        print(f"factor_min={factor_min}")
        print(f"factor_max={factor_max}")

    for factor in range(factor_min, factor_max + 1):
        if sum(FACTOR_PDF[factor_min:factor + 1]) >= random_y:
            return factor

    return -1 # shouldn't occur


def check_arg(arguments=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--version', action='store_true')
    parser.add_argument('--seed', default=int(time()))
    parser.add_argument('level', type=int)
    parser.add_argument('output_file', nargs='*', default=None)
    parser.set_defaults(version=False)

    return parser.parse_args(arguments)


def get_multiplication_text(factor1, factor2, prng):
    """Format multiplication text
    The order of the factors are randomized.
    """

    # multiplication_symbol = u'\u00d7'
    if prng.randint(1, 2) == 1:
        return f"{factor1} \u00d7 {factor2}"
    return f"{factor2} \u00d7 {factor1}"


def get_random_multiplication_text(factor1_max, factor2_max, prng):
    """Create text factor x factor
    factor1 is 1.. factor1_max
    factor2 is 0.. factor2_max
    """

    factor1 = get_factor(1, factor1_max, prng)
    factor2 = get_factor(0, factor2_max, prng)

    return get_multiplication_text(factor1, factor2, prng)


def write_header(pdf, title, height, width):
    """Write header to pdf"""
    pdf.setLineWidth(HEADER_LINE_WIDTH)
    pdf.line(
        MARGIN_SIZE / 2,
        height - MARGIN_SIZE,
        width - MARGIN_SIZE / 2,
        height - MARGIN_SIZE)

    pdf.setFont(FONT_NAME, HEADER_FONT_SIZE)

    text_width = stringWidth(title, FONT_NAME, HEADER_FONT_SIZE)
    pdf.drawString(width / 2 - text_width / 2, height - MARGIN_SIZE + SPACING, title)


def write_footer(pdf, text, width):
    """Write footer to pdf"""
    pdf.line(
        MARGIN_SIZE / 2,
        MARGIN_SIZE - SPACING,
        width - MARGIN_SIZE / 2,
        MARGIN_SIZE - SPACING)
    pdf.setFont(FONT_NAME, FOOTER_FONT_SIZE)
    pdf.drawString(
        MARGIN_SIZE / 2,
        MARGIN_SIZE - SPACING - FOOTER_FONT_SIZE,
        text)

    # add Copyright notice
    text_width = stringWidth(COPYRIGHT_TEXT, FONT_NAME, FOOTER_FONT_SIZE)
    pdf.drawString(
        width - MARGIN_SIZE / 2 - text_width,
        MARGIN_SIZE - SPACING - FOOTER_FONT_SIZE,
        COPYRIGHT_TEXT)


def write_exercises(pdf, width, height, exercises):
    """Write multiplication exercises to pdf."""
    column_width = (width - 2 * MARGIN_SIZE) / COLUMNS
    row_height = (height - 2 * MARGIN_SIZE) / ROWS

    for column in range(COLUMNS):
        for row in range(ROWS):
            point_x = column * column_width + MARGIN_SIZE
            point_y = row * row_height + MARGIN_SIZE

            exercise_text = exercises.pop()
            text_width = stringWidth(exercise_text, FONT_NAME, FONT_SIZE)
            pdf.drawString(point_x, point_y, exercise_text)
            pdf.line(
                point_x + text_width + SPACING,
                point_y,
                point_x + column_width - SPACING,
                point_y)


def multiplikation(output_file, factor_level, seed, max_factor=10, page_size=A4):
    """Do the shiznit
    factor_level, one of the factors should not be larger than this
    max_factor, the other factor's max
    """

    if _verbosity_level > 3:
        print(f"seed type is {type(seed)}")

    if factor_level > max_factor:
        max_factor = factor_level

    pdf = canvas.Canvas(output_file, pagesize=page_size)
    pdf.setLineWidth(ANSWER_LINE_WIDTH)
    pdf.setFont(FONT_NAME, FONT_SIZE)
    width, height = page_size

    # Use given seed for reproducable random numbers
    prng = RandomWithSeed(seed)

    # Write main content
    exercises = []

    # make sure all products of selected level occurs at least once
    # so add them first to the array
    for factor in range(factor_level+1):
        exercises.append(get_multiplication_text(factor, factor_level, prng))

    for _ in range(COLUMNS * ROWS - len(exercises)):
        exercises.append(get_random_multiplication_text(factor_level, max_factor, prng))

    prng.shuffle(exercises) # better shuffle it


    # Write main content
    write_exercises(pdf, width, height, exercises)

    # Write header
    write_header(
        pdf,
        f"Multiplikation {factor_level}",
        height,
        width
        )

    # Write footer
    write_footer(
        pdf,
        f"Multiplikation v{__version__} {{max_factor={max_factor}, seed={seed}}}",
        width
    )

    pdf.save()
    return 0


def main(arguments):
    """Main function."""

    command_line_options = check_arg(arguments)

    global _verbosity_level # pylint: disable=W0603, C0103
    _verbosity_level = command_line_options.verbose

    if command_line_options.version:
        print(f"{__file__} version {__version__}")
        print(__doc__)
        return 0

    if command_line_options.level < 1:
        print("You cannot select a level < 1.")
        return -3

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

    return multiplikation(
        output_file,
        command_line_options.level,
        int(command_line_options.seed))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

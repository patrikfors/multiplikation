Multiplikation
==============

Generate multiplication exercise pdf's.

Usage
-----

Multiplikation is a simple script to generate a pdf with multiplication excercises with given "max table".

A typical use case is to generate an exercise pdf for a multiplication table. A parameter level is supplied
to select the largest factor used. If level 6 is selected, at least one of the factors are no larger than 6.

```bash
python multiplikation.py 6
```

The factors are random, but slightly weighted to reduce the number of free/easy multiplications. Least common are
factor 0, 1, 2, 10, 5, 3, 4, in that order.

If no output file name is given, the file name is set to ``<level>.pdf``.

```bash
python multiplikation.py 6 excercise.pdf
```

If the file, either specified or automatically selected, already exists, a numeric suffix is appended.

```bash
python multiplikation.py 6 excercise.pdf
python multiplikation.py 6 excercise.pdf
```

This would generate both ``exercise.pdf`` and ``excercise0.pdf``.

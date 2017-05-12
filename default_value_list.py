"""list type that returns a default value if index is out of bounds
adapted from http://stackoverflow.com/a/20218176/224585.
"""


class DefaultValueList(list):
    """list type that returns a default value if index is out of bounds
    adapted from http://stackoverflow.com/a/20218176/224585.
    """

    def __init__(self, arr, default_value):
        list.__init__(self, arr)
        self._default_value = default_value

    def __getitem__(self, item):
        if isinstance(item, slice):
            step = item.step if item and item.step else 1
            start = item.start if item and item.start else 0

            # print(f"item={item}")
            # print(f"start={start}")
            # print(f"stop={item.stop}")
            # print(f"step={step}")
            # print(f"range = {range(start, item.stop, step)}")
            return [self.__getitem__(i) for i in range(start, item.stop, step)]
        try:
            value = super(DefaultValueList, self).__getitem__(item)
        except IndexError:
            value = self._default_value
        return value

    def __getslice__(self, start, stop):
        return self.__getitem__(slice(start, stop, None))


if __name__ == '__main__':
    TEST_LIST = DefaultValueList([1, 2, 3, 4], 8)
    for index in range(-10, 10):
        print(f"TEST_LIST[{index}] = {TEST_LIST[index]}")

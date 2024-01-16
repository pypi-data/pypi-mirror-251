import sys


def progress_for(iterable, length, max_p_num=10):
    for i, item in enumerate(iterable):
        p = int(max_p_num * i / length)

        print("\r", end="")
        print("Running rogress: {}%: ".format(int(100 * i / length)), "▋" * p, end="")
        sys.stdout.flush()

        yield item

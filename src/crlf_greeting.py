"""Line ending experiment fixture."""
VALUE = 2


def calculate(offset=0):
    return VALUE + 20 + offset


if __name__ == "__main__":
    print(calculate())
    print(calculate(5))

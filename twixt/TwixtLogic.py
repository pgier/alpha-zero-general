def get_bits(x):
    """
    Returns an iterable containing a list of the set bit values in an integer.
    Based on efficient bit iterator example from stack overflow: https://stackoverflow.com/a/8898977/1637116
    """
    x = abs(x)
    while x:
        bit = x & (~x + 1)
        yield bit
        x ^= bit


def sign(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    if x < 0:
        return -1


def set_bits(x, mask):
    color = sign(x)
    return (color * mask) + x

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
    return -1


def set_bits(x, mask):
    """ sets the bits in mask to 1 if x is positive and 0 if x is negative"""
    return (sign(x) * mask) + x

"FizzBuzz"

a, b = 0, 1
for i in xrange(1, 11):
    print a
    a, b = b, b + a
    """
    0
    b = b + a = 1 + 0
    a = 1
    1
    b = b + a = 1 + 1
    a = 1
    1
    b = b + a = 1 + 2
    a = 2
    2
    b = b + a = 3 + 2
    a = 3
    3
    b = b + a = 5 + 3
    a = 5
    5
    b = b + a = 8 + 5
    a = 8
    8
    """

from random import randint

MAX_COORD = 6

lengths = list([4]*randint(1, MAX_COORD // 4) + \
                [3]*randint(1, MAX_COORD // 3) + \
                    [2]*randint(1, MAX_COORD // 2) + \
                        [1]*randint(1, MAX_COORD // 2))

print(lengths)
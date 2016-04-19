known = {}

def levenshtein_distance(a,b):
    """ Finds the difference between two strings/finds the least number of
        changes required to make one string into the other

        >>> levenshtein_distance('kitten','smitten')
        2
        >>> levenshtein_distance('','apple')
        5
        >>> levenshtein_distance('why','')
        3
    """
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)

    if (a,b) in known:
        return known[(a,b)]
    
    if a[0] == b[0]:
        option1 = levenshtein_distance(a[1:], b[1:])
    else:
        option1 = 1 + levenshtein_distance(a[1:], b[1:])
    
    option2 = levenshtein_distance(a, b[1:]) + 1
    option3 = levenshtein_distance(a[1:], b) + 1

    res = min(option1, option2, option3)
    known[(a,b)] = res
    return res

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
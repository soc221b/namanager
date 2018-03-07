import re


def gen_unique_str(string):
    u = '_'
    while u in string:
        u += '_'
    return u


def get_first_word(s):
    if s == '':
        return ('', -1, 0)
    start = 0 if len(s) else -1
    end = 1 if len(s) else -1
    while end < len(s):
        # abbr
        if (s[end - 1].isupper() and
            s[end].isupper() and
           (end + 1 != len(s) and s[end + 1].islower())):
            break

        if (re.search('[^a-z]', s[end]) and
           not s[end - 1].isupper()):
            break

        end += 1

    return (s[start:end], start, end)

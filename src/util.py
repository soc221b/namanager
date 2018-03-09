import re


def gen_unique_str(string):
    u = '_'
    while u in string:
        u += '_'
    return u


def get_first_word(s):
    try:
        beg = s.find(re.search('[A-Za-z]', s).group(0)) if len(s) else -1
    except Exception:
        beg = -1
    end = beg + 1 if len(s) else 0
    while end < len(s):
        # e.g., HTTPResponse
        if (s[end - 1].isupper() and
            s[end].isupper() and
           (end + 1 != len(s) and s[end + 1].islower())):
            break
        # e.g., HttpResponse or Http_response
        if s[end - 1].islower() and not s[end].islower():
            break
        # e.g., HTTP* or HTTP_
        if not s[end].isalpha():
            break

        end += 1

    return (s[beg:end], beg, end)


def get_words(string, include_non_letter=True):
    words = []
    while string != '':
        if include_non_letter and not string[0].isalpha():
            first_letter = re.search('[a-zA-Z]', string)
            if first_letter:
                i = string.find(first_letter.group(0))
                words += [string[:i]]
                string = string[i:]
            else:
                words += [string]
                string = ''
        else:
            tpl = get_first_word(string)
            if tpl[0]:
                string = string[tpl[2]:]
                words += [tpl[0]]
            else:
                string = ''

    return [w for w in words if w != '']


def convert_word_to_case(word, case):
    try:
        if case == 'upper_case':
            word = word.upper()
        if case == 'lower_case':
            word = word.lower()
        if case == 'camel_case':
            pass
        if case == 'pascal_case':
            pass
    except Exception:
        pass

    return word

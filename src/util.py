import re


def gen_unique_str(string):
    u = '_'
    while u in string:
        u += '_'
    return u


def get_first_word(s):
    try:
        beg = s.find(re.search('[A-Za-z]', s)[0]) if len(s) else -1
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

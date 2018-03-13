import helper # noqa


class TestHelper():
    def test_get_error_string(self):
        get_error_string = helper.get_error_string
        assert isinstance(get_error_string([]), str)
        assert isinstance(get_error_string(['a', 'b']), str)

    def test_gen_random_alphabet_string(self):
        gen_random_alphabet_string = helper.gen_random_alphabet_string
        strings = []
        for _ in range(0, 1000):
            s = gen_random_alphabet_string(1000)
            assert s not in strings
            strings.append(s)

    def test_gen_all_possible_pair(self):
        gen_all_possible_pair = helper.gen_all_possible_pair
        assert (gen_all_possible_pair('') == [])
        assert (gen_all_possible_pair('a') == [('a',)])
        assert (gen_all_possible_pair('ab') == [
            ('a',), ('b',), ('a', 'b'), ('b', 'a')
        ])
        assert (gen_all_possible_pair('abc') == [
            ('a',), ('b',), ('c',), ('a', 'b'), ('b', 'a'), ('a', 'c'),
            ('c', 'a'), ('b', 'c'), ('c', 'b'), ('a', 'b', 'c'),
            ('a', 'c', 'b'), ('b', 'a', 'c'), ('b', 'c', 'a'),
            ('c', 'a', 'b'), ('c', 'b', 'a')
        ])
        assert (gen_all_possible_pair([]) == [])
        assert (gen_all_possible_pair(['a']) == [('a',)])
        assert (gen_all_possible_pair(['a', 'bc']) == [
            ('a',), ('bc',), ('a', 'bc'), ('bc', 'a')
        ])
        assert (gen_all_possible_pair(['a', 'bc', 'def']) == [
            ('a',), ('bc',), ('def',), ('a', 'bc'), ('bc', 'a'), ('a', 'def'),
            ('def', 'a'), ('bc', 'def'), ('def', 'bc'), ('a', 'bc', 'def'),
            ('a', 'def', 'bc'), ('bc', 'a', 'def'), ('bc', 'def', 'a'),
            ('def', 'a', 'bc'), ('def', 'bc', 'a')
        ])

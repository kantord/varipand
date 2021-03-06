from varipand import expand_all

DEFAULT_CONFIG = {
    "delimiters": {
        "start": "(",
        "end": ")",
        "comma": "/",
    },
    "include_delimiter": False
}

ALTERNATIVE_CONFIG_1 = {
    "delimiters": {
        "start": "[ ",
        "end": " ]",
        "comma": ", ",
    },
    "include_delimiter": False
}


def test_expand_returns_an_iterator():
    assert hasattr(type(expand_all([""], DEFAULT_CONFIG)), '__iter__')


def test_expanding_empty_string_yield_empty_string():
    assert list(expand_all([""], DEFAULT_CONFIG)) == [""]


def test_expanding_a_pattern_without_variations_returns_the_pattern():
    assert list(expand_all(["Hello World!"], DEFAULT_CONFIG)) == [
        "Hello World!"]


def test_every_input_pattern_is_expanded():
    assert list(expand_all(["Hello World!", ""], DEFAULT_CONFIG)) == [
        "Hello World!", ""]


def test_every_value_is_only_yielded_once():
    assert list(expand_all(["Hello World!", "", ""], DEFAULT_CONFIG)) == [
        "Hello World!", ""]


def test_output_does_not_include_start_and_end_delimiters():
    assert list(expand_all(["Hello (World)!", ], DEFAULT_CONFIG)) == [
        "Hello World!"]


def test_supports_alternative_start_and_end_delimiters():
    assert list(expand_all(["Hello [ World ]!", ], ALTERNATIVE_CONFIG_1)) == [
        "Hello World!"]


def test_supports_multiple_parentheses():
    assert list(expand_all(["[ Hello ] [ World ]!", ], ALTERNATIVE_CONFIG_1)) == [
        "Hello World!"]


def test_returns_a_new_phrase_for_each_variant():
    assert list(expand_all(["Hello (World/You)(!/)", ], DEFAULT_CONFIG)) == [
        "Hello World!",
        "Hello You!",
        "Hello World",
        "Hello You",
    ]


def test_returns_a_new_phrase_for_each_variant_with_alternative_delimiter():
    assert list(expand_all(["Hello [ World, You ][ !,  ]", ], ALTERNATIVE_CONFIG_1)) == [
        "Hello World!",
        "Hello You!",
        "Hello World",
        "Hello You",
    ]

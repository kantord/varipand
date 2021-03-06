import itertools


def _get_prefix(pattern, settings):
    start_symbol = settings["delimiters"]["start"]

    return pattern.split(start_symbol, 1)


def _has_variants(pattern, settings):
    start_symbol = settings["delimiters"]["start"]

    return start_symbol not in pattern


def _get_variants_and_suffix(right_hand_side, settings):
    end_symbol = settings["delimiters"]["end"]
    raw_variants, suffix = right_hand_side.split(end_symbol, 1)

    return _variants_from_list(raw_variants, settings), suffix


def _variants_from_list(list_of_variants, settings):
    comma_symbol = settings["delimiters"]["comma"]

    return list_of_variants.split(comma_symbol)


def expand(settings):
    def f(pattern):

        if _has_variants(pattern, settings):
            yield pattern
            return

        prefix, right_hand_side = _get_prefix(pattern, settings)
        variants, suffix_pattern = _get_variants_and_suffix(
            right_hand_side, settings)
        for suffix in f(suffix_pattern):
            for variant in variants:
                yield "".join([prefix, variant, suffix])

    return f


def _deduplicated(items):
    already_yielded = set()

    for item in items:
        if item not in already_yielded:
            yield item
            already_yielded.add(item)


def expand_all(patterns, settings):
    """
        Expand a set of patterns into phrases
    """

    all_variants = itertools.chain(
        *[expand(settings)(pattern) for pattern in patterns])
    return _deduplicated(all_variants)

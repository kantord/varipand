import itertools


def _get_prefix(pattern, settings):
    start_symbol = settings["delimiters"]["start"]

    return pattern.split(start_symbol, 1)


def _has_variants(pattern, settings):
    start_symbol = settings["delimiters"]["start"]

    return start_symbol in pattern


def _get_variants_and_suffix(right_hand_side, settings):
    end_symbol = settings["delimiters"]["end"]
    raw_variants, suffix = right_hand_side.split(end_symbol, 1)

    return _variants_from_list(raw_variants, settings), suffix


def _variants_from_list(list_of_variants, settings):
    comma_symbol = settings["delimiters"]["comma"]

    return list_of_variants.split(comma_symbol)


def _phrases_based_on_pattern(pattern, settings):
    prefix, right_hand_side = _get_prefix(pattern, settings)
    variants, suffix_pattern = _get_variants_and_suffix(
        right_hand_side, settings)

    for suffix in expand(settings)(suffix_pattern):
        for variant in variants:
            yield "".join([prefix, variant, suffix])


def _deduplicated_iterable(items):
    already_yielded = set()

    for item in items:
        if item not in already_yielded:
            yield item
            already_yielded.add(item)


def expand(settings):
    """
    Expand a single pattern
    """
    def f(pattern):
        if not _has_variants(pattern, settings):
            yield pattern
            return

        phrases = _phrases_based_on_pattern(pattern, settings)
        for phrase in _deduplicated_iterable(phrases):
            yield phrase

    return f


def expand_all(settings):
    """
        Expand a set of patterns into phrases
    """

    def f(patterns):
        all_variants = itertools.chain(*map(expand(settings), patterns))
        return _deduplicated_iterable(all_variants)

    return f

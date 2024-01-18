import pytest
import re
import regex


@pytest.fixture()
def re_and_regex_instances():
    test_str = "THING"
    rep = re.compile(".*HIN.*")
    regexp = regex.compile(".*HIN.*", flags=regex.V1)
    return {
        're_pattern_instance': rep,
        'regex_pattern_instance': regexp,
        're_match_instance': rep.match(test_str),
        'regex_match_instance': regexp.match(test_str),
        're_scanner_instance': rep.scanner(test_str),
        'regex_scanner_instance': regexp.scanner(test_str),
        'regex_splitter_instance': regexp.splititer(test_str)
    }

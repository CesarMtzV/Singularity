from lexer import lexer
import testParams
import pytest

@pytest.mark.parametrize("test_input, expected", [
    (testParams.lexerTest1_data, testParams.lexerTest1_expected)
])
def test_addition(test_input, expected):
    lexer.input(test_input)
    
    actual = {}

    for tok in lexer:
        actual[tok.type] = tok.value
    
    assert actual == expected


from lexer import Lexer, Token

def run_lexer_test(test_name, input_str, expected_tokens):
    print(f"\nTest: {test_name}")
    print(f"Input: '{input_str}'")
    
    lexer = Lexer(input_str)
    tokens = lexer.tokenize()
    
    print("\nGenerated Tokens:")
    print([str(t) for t in tokens])
    
    print("\nExpected Tokens:")
    print([str(t) for t in expected_tokens])
    
    assert len(tokens) == len(expected_tokens), f"Token count mismatch: {len(tokens)} vs {len(expected_tokens)}"
    
    for i, (generated, expected) in enumerate(zip(tokens, expected_tokens)):
        assert generated.type == expected.type and generated.value == expected.value, \
               f"Token {i} mismatch: {generated} vs {expected}"
    
    print("Test passed!")

# Test cases
if __name__ == "__main__":
    # Test 1: Original test case with quoted strings and multi-word operators
    test1_input = '''if ("hello" is equal to 'hello') then do print 'multi word string' fi'''
    test1_expected = [
        Token('IF_OPEN'), 
        Token('LEFT_BRACKET'),
        Token('STRING', 'hello'),
        Token('EQUALS'),  # "is equal to"
        Token('STRING', 'hello'),
        Token('RIGHT_BRACKET'),
        Token('THEN'),
        Token('DO'),
        Token('OUTPUT'),
        Token('STRING', 'multi word string'),
        Token('IF_CLOSE')
    ]
    run_lexer_test("Basic string and operator recognition", test1_input, test1_expected)

    # Test 2: Mixed multi-word operators
    test2_input = "while x is greater than 5 divided by 2 multiplied by 3"
    test2_expected = [
        Token('WHILE_OPEN'),
        Token('ID', 'x'),
        Token('GREATER'),  # "is greater than"
        Token('INT', '5'),
        Token('DIVIDE'),   # "divided by"
        Token('INT', '2'),
        Token('MULTIPLY'), # "multiplied by"
        Token('INT', '3')
    ]
    run_lexer_test("Mathematical operators", test2_input, test2_expected)

    # Test 3: Edge cases with nested quotes
    test3_input = '''new var string test is "contains 'nested' quotes"'''
    test3_expected = [
        Token('NEW_VAR_IDENT'),
        Token('VAR'),
        Token('STRING'),
        Token('ID', 'test'),
        Token('ASSIGNMENT_OPERATOR'),
        Token('STRING', "contains 'nested' quotes")
    ]
    run_lexer_test("Nested quotes", test3_input, test3_expected)

    # Test 4: Complex expression with multiple types
    test4_input = '''new const int x is (5 divided by 2.5) is less than 3'''
    test4_expected = [
        Token('NEW_VAR_IDENT'),
        Token('CONST'),
        Token('INTEGER'),
        Token('ID', 'x'),
        Token('ASSIGNMENT_OPERATOR'),
        Token('LEFT_BRACKET'),
        Token('INT', '5'),
        Token('DIVIDE'),
        Token('FLOAT', '2.5'),
        Token('RIGHT_BRACKET'),
        Token('LESS'),  # "is less than"
        Token('INT', '3')
    ]
    run_lexer_test("Mixed types and operators", test4_input, test4_expected)

    # Test 5: Empty string case
    test5_input = '''print ""'''
    test5_expected = [
        Token('OUTPUT'),
        Token('STRING', '')
    ]
    run_lexer_test("Empty string", test5_input, test5_expected)

    print("\nAll tests completed!")
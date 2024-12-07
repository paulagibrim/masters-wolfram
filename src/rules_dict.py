def generate_rule_dict(rule_number):
    """
    Generate the dictionary for a given rule number in Wolfram's 1D automata.
    :param rule_number: Integer (0-255), the rule ID.
    :return: dict, mapping of neighbor states to next state.
    """
    # Convert the rule number to an 8-bit binary representation
    binary_representation = f"{rule_number:08b}"
    
    # Create a list of all possible neighbor combinations
    combinations = [
        (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
        (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1),
    ]
    
    # Map each combination to the corresponding bit in the rule's binary representation
    return {
        combo: int(binary_representation[7 - i])  # Reverse order of binary bits
        for i, combo in enumerate(combinations)
    }

# Generate all 256 rule dictionaries
rules = {i: generate_rule_dict(i) for i in range(256)}
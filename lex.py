def extract_quote_strings(string: str) -> list:
    """
    Extracts all substrings surrounded by a pair of quotes. Quotes can be
    single (') or double ("), but each pair of quotes must consist of two of
    the same quotes.
    
    For example, `extract_quote_strings('Hello, "world"!')` -> `["world"]`

    Parameters:
        string (str): the main string

    Returns:
        list: a list of all the substrings found, the original quotes are not 
        in the string
    """

    strings_found = []
    current_token = ""
    inside_quotes = False
    quote_char = ""  # To track which quote type we're inside (' or ")

    for char in string:
        if not inside_quotes:
            # Check if we find an opening quote
            if char == '"' or char == "'":
                inside_quotes = True
                quote_char = char  # Remember the type of quote
                current_token = char  # Start the token with the opening quote
        else:
            # We're inside quotes
            current_token += char
            if char == quote_char:
                # If it's the closing quote, save the token
                strings_found.append(current_token.strip(quote_char))
                current_token = ""
                inside_quotes = False
                quote_char = ""

    return strings_found


def is_following_rule(string: str, rule: dict) -> bool:
    match rule["rule_type"]:
        case "equal":
            return string == rule["check_string"]
        case "between":
            return (
                string.startswith(rule["start_string"])
                and string.endswith(rule["end_string"])
                and len(string) >= 2
            )
            

def split_rule_string(rule_string: str):
    (type_part, match_part) = rule_string.split("->")
    type_part = type_part.strip()
    match_part = match_part.strip()
    (class_name, subclass_name) = type_part.split(" ")
    
    return match_part, class_name, subclass_name 


rules_string = open("rules.lexif", "r").read()
rule_strings = [rule for rule in rules_string.split("\n") if rule.strip() != ""]
rules = []
for rule_string in rule_strings:
    rule_string = rule_string.replace("[NEWLINE]", '"\n"')
    
    (match_part, class_name, subclass_name) = split_rule_string(rule_string)
    
    rule = {"class": class_name, "subclass": subclass_name}

    # equal
    if match_part.startswith("is"):
        rule["rule_type"] = "equal"
        rule["check_string"] = extract_quote_strings(match_part)[0]
        rules.append(rule)
        continue

    # between two certain strings
    if match_part.startswith("between"):
        rule["rule_type"] = "between"

        end_strings = extract_quote_strings(match_part)
        

        rule["start_string"] = end_strings[0]
        rule["end_string"] = end_strings[1]
        rules.append(rule)
        continue

code = open("test_code.txt", "r").read()

tokens = []
current_token = ""
recent_token_end = -1
for i, char in enumerate(code):
    current_token += char

    for rule in rules:
        if is_following_rule(current_token, rule):
            tokens.append(
                {
                    "class": rule["class"],
                    "subclass": rule["subclass"],
                    "content": current_token,
                    "start_position": recent_token_end + 1,
                    "end_position": i
                }
            )
            recent_token_end = i
            current_token = ""
            break
if current_token != "":
    tokens.append(
        {
            "class": "ERROR",
            "subclass": "UNFIISHED_TOKEN",
            "content": current_token,
            "start_position": recent_token_end + 1
        }
    )

for rule in rule_strings:
    print(rule)
print()
for rule in rules:
    print(rule)
print()
for token in tokens:
    print(token)

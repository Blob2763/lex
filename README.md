# lex
A programming language tokenizer

## Setting up
1. Download `lex.py` by going to [lex/lex.py](https://github.com/Blob2763/lex/blob/main/lex.py) and pressing the download button
2. Add `lex.py` to the folder where you need to use it
> [!CAUTION]  
> `lex.py` has to be in the same folder for it to work, not a child folder or parent folder
3. Add the following code to the python file that is using lex
```py
from lex import tokenise
```

All done! You're now ready to use lex

## Usage
Tokenising code is very simple, you just need to provide a **rules file** and a **code file**

> [!NOTE]  
> The code file does not have to be a `.txt` file! You can choose any file extension

> [!IMPORTANT]  
> The rules file must have the `.lexif` file extension

Once you've added your rules file and code file, the file directory should look like this:
```
code.txt
lex.py
main.py
rules.lexif
```
In this example, `rules.lexif` is the rules file and `code.txt` is the code file for your custom programming language

To tokenise your code, put this in `main.py`, or whatever Python file is parsing your code:
```py
from lex import tokenise
tokens = tokenise("rules.lexif", "code.txt")
```

## How it Works
### The rules file
The rules file tells lex how to split up your code.
The rules file has different headings to keep the rules organised. Each heading starts with `#`

### Rules
All rules go under the `#RULES` heading

Here's what a rule looks like:
```
DELIMITER LPAREN -> is "("
```
Let's break it down:
| Class       | Subclass | Arrow | Rule type | Check string |
|-------------|----------|-------|-----------|--------------|
| `DELIMITER` | `LPAREN` | `->`  | `is`      | `"("`        |

#### Class and Subclass
This tells lex what this rule is looking out for and helps identify tokens. It doesn't change the functionality of the rule, but it is important that you have them as it makes it easier to process tokens later on

The class and the subclass must both have no spaces in their names, and they must be separated by a single space:
| Example                 | Good/Bad |
|-------------------------|----------|
| `LITERAL STRING`        | ✅        |
| `IDENTIFIER FUNC_PRINT` | ✅        |
| `literal string`        | ✅        |
| `LITERAL  STRING`       | ❌        |
| `IDENTIFIER FUNC PRINT` | ❌        |

You can use any class name you want, but here are some recommendations:
| Class name | Usage |
|------------|-------|
| `IDENTIFIER` | General names for variables or functions |
| `KEYWORD` | Things like `if`, `for`, `while`, etc. |
| `LITERAL` | Things that represent fixed values like strings, numbers, boolean values, etc. |
| `OPERATOR` | Things that perform operations like `+`, `-`, `*`, etc. |
| `DELIMITER` | Things that define boundaries in the code like `(`, `;`, `}`, etc. |
| `IGNORE` | Things to ignore in the code like comments or whitespace |

> [!WARNING]  
> The `ERROR` class name is reserved for lexing errors, like an unfinished token at the end of a file. Usage of the `ERROR` class is not prohibited, but it is not reccomended unless you know what you are doing.

> [!TIP]
> Classes like `ERROR` usually mean something is wrong with the user's code (assuming the rules in the rules file are good), so it is good practise to handle them in your parser

#### Arrow
The arrow on each rule shows how tokens are created with that rule. There are currently two types of arrow:
| Arrow    | Creation type | Meaning                                                                                                                                               |
|----------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `->`     | normal        | A new token will be made as soon as the rule is matched                                                                                               |
| `=>`     | greedy        | Maximises the length of the token. A new token will be made when adding the next character to the token will no longer make the token follow the rule |

#### Rule type
The rule type tells lex how to detect the token

| Rule type  | Meaning                                                                        | Example usage                           | Notes |
|------------|--------------------------------------------------------------------------------|-----------------------------------------|-------|
| `is`       | Looks for an exact match to a string                                           | `DELIMITER LPAREN -> is "("`            |       |
| `between`  | Looks for something that starts with the first string and ends with the second | `LITERAl STRING -> between '"' and '"'` | The word `and` is not really needed, as long as there is a gap between the strings, you can put anything in there. The surrounding strings are included in the token content. |
| `matches`  | Looks for a string that matched a regex pattern                                | `LITERAL DIGIT -> matches [0-9]`        | This is best used with the `=>` arrow for detecting longer strings |
| `endswith` | Looks for a string that ends with the given string                             | `FILETYPE IMAGE -> endswith ".png"`     | There will never be a `startswith` rule type due to how it will work just like the `is` rule type with `->` and will never find a complete match with the `=>` arrow |

#### Rule Priority
> [!NOTE]  
> Rules higher up in the file get checked first

`let` is a `KEYWORD LET`
```
#RULES
KEYWORD LET -> is "let"
IDENTIFIER VARIABLE => matches ^[a-zA-Z]+$
```

`let` is an `IDENTIFIER VARIABLE`
```
#RULES
IDENTIFIER VARIABLE => matches ^[a-zA-Z]+$
KEYWORD LET -> is "let"
```
`^[a-zA-Z]+$` is regex that matches a string of letters

#### Examples
Still confused? Here's some example rules and what they mean

Detects the string `print`
```
IDENTIFIER PRINT -> is "print"
```

Detects any string between double quotes (`"`)
```
LITERAl STRING -> between '"' and '"'
```

Detects a string of numbers
```
LITERAL NUMBER => matches [0-9]+
```


### Constants
All constants go under the `#CONSTANTS` heading

Here's what a constant definition looks like:
```
[NEWLINE] -> "\n"
```
Let's break it down:
| Name        | Arrow | Value  |
|-------------|-------|------- |
| `[NEWLINE]` | `->`  | `"\n"` |

> [!NOTE]  
> A constant name doesn't have to be surrounded by square brackets, but it can make them more recognisable

You don't have to use constants, but they are useful if you want to keep the rules file clean

> [!TIP]
> Constants are great for storing regex patterns to make them more human readable

After you have defined a constant, you can use it enywhere in a rule. You can not use constants in other constants

Here's an example:
```
#CONSTANTS
[DIGIT REGEX] -> [0-9]
#RULES
LITERAL DIGIT -> matches [DIGIT REGEX]
```

> [!IMPORTANT]  
> Constants are essentially find + replace, so don't forget to include speech marks if storing a string

### Tokens
The `tokenise` function returns a list of tokens in the order they appeared in the file. Here's an example of a token:
```json
{ "class": "LITERAl", "subclass": "STRING", "content": "'Hello, World!'", "start_position": 24, "end_position": 38, "line_number": 5 }
```

#### Error tokens
Error tokens look the same as normal tokens, but will always have the class `ERROR`. The subclass shows the type of error:
| Subclass | Meaning |
|----------|---------|
| `UNFINISHED_TOKEN` | There was some text at the end of the file that did not match a token. This could signify there is an error in the code somewhere within the token content |

## Nerd stuff
### How tokenising works
The way lex finds tokens is by building a token going from the start of the file to the end of the file, if the token matches a rule, the token is added to a list and a new token is built. If not, the next character is added.

Here's an example:
```
#RULES
IDENTIFIER PRINT -> is "print"
LITERAl STRING -> between '"' and '"'
DELIMITER LPAREN -> is "("
DELIMITER RPAREN -> is ")"
```
```py
print("Hello, World")
```

| Current token | Token list* |
|---------------|------------|
| `p` | `[]` |
| `pr` | `[]` |
| `pri` | `[]` |
| `prin` | `[]` |
| `print` | `[]` |
| `‎` | `[PRINT]` |
| `(` | `[PRINT]` |
| `‎` | `[PRINT, LPAREN]` |
| `"` | `[PRINT, LPAREN]` |
| `"H` | `[PRINT, LPAREN]` |
| `"He` | `[PRINT, LPAREN]` |
| `"Hel` | `[PRINT, LPAREN]` |
| `"Hell` | `[PRINT, LPAREN]` |
| `"Hello` | `[PRINT, LPAREN]` |
| `"Hello,` | `[PRINT, LPAREN]` |
| `"Hello, ` | `[PRINT, LPAREN]` |
| `"Hello, W` | `[PRINT, LPAREN]` |
| `"Hello, Wo` | `[PRINT, LPAREN]` |
| `"Hello, Wor` | `[PRINT, LPAREN]` |
| `"Hello, Worl` | `[PRINT, LPAREN]` |
| `"Hello, World` | `[PRINT, LPAREN]` |
| `"Hello, World"` | `[PRINT, LPAREN]` |
| `‎` | `[PRINT, LPAREN, STRING]` |
| `)` | `[PRINT, LPAREN, STRING]` |
| `‎` | `[PRINT, LPAREN, STRING, RPAREN]` |

*The class name, content, start position, and end position have been left out

### Other functions in `lex.py`
> [!CAUTION]
> These are helper functions for `tokenise()` editing them could break the functionality of the main tokeniser

> [!NOTE]
> Most of these functions do not have any real uses other than tokenisation, it is not recommended to use any of the functions listed below

#### `extract_quote_strings(string)`
Extracts all substrings surrounded by a pair of quotes. Quotes can be single (') or double ("), but each pair of quotes must consist of two of the same quotes.

For example, `extract_quote_strings('Hello, "world"!')` -> `["world"]`

Parameters:
| Name | Type | Description |
|------|------|-------------|
| `string` | `str` | the main string |


Returns:
| Name | Type | Description |
|------|------|-------------|
| `substrings_found` | `list` | a list of all the substrings found, the original quotes are not in the string |

#### `is_following_rule(string, rule)`
Checks whether a certain string is following a rule.

Parameters:
| Name | Type | Description |
|------|------|-------------|
| `string` | `str` | the string to test |
| `rule` | `dict` | the rule to test against |

Returns:
| Name | Type | Description |
|------|------|-------------|
| `is_pass` | `bool` | whether or not the string follows the rule |

#### `split_rule_string(rule_string)`
Splits a rule string into separate parts.

Parameters:
| Name | Type | Description |
|------|------|-------------|
| `rule_string` | `str` | the rule string to be split |

Returns:
| Name | Type | Description |
|------|------|-------------|
| `match_part` | `str` | all the text after the arrow |
| `class_name` | `str` | the name of the class of the rule |
| `subclass_name` | `str` | the name of the subclass of the rule |
| `match_type` | `str` | the type of match defined by the arrow |

#### `generate_rules(rules_file)`
Generates a list of rules based on the contents of a rules file.

Parameters:
| Name | Type | Description |
|------|------|-------------|
| `rules_file` | `str` | the rules in the rules file |

Returns:
| Name | Type | Description |
|------|------|-------------|
| `rules` | `list` | a list of all the rules as dictionaries |

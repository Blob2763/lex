# lex
A programming language tokenizer

## Setting up
1. Download `lex.py` by going to [lex/lex.py](https://github.com/Blob2763/lex/blob/main/lex.py) and pressing the download button
2. Add `lex.py` to the directory where you need to use it
> [!IMPORTANT]  
> `lex.py` has to be in the same directory for it to work, not a child directory or parent directory
3. Add the following code to the python file that is using lex
```py
from lex import tokenise
```

All done! You're now ready to use lex

## Usage
Tokenising code is very simple, you just need to provide a **rules file** and a **code file**

In this example, `rules.lexif` is the rules file and `code.txt` is the code file
```py
from lex import tokenise
tokens = tokenise("rules.lexif", "code.txt")
```

## How it Works
### The rules file
The rules file tells lex how to split up your code, it must have the file extension `.lexif`
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
| `IGNORE` | Things to ignore in the code like comments |

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
| `between`  | Looks for something that starts with the first string and ends with the second | `LITERAl STRING -> between '"' and '"'` | The word `and` is not really needed, as long as there is a gap between the strings, you can put anything in there |
| `matches`  | Looks for a string that matched a regex pattern                                | `LITERAL DIGIT -> matches [0-9]`        | This is best used with the `=>` arrow for detecting longer strings |
| `endswith` | Looks for a string that ends with the given string                             | `FILETYPE IMAGE -> endswith ".png"`     | There will never be a `startswith` rule type due to how it will work just like the `is` rule type with `->` and will never find a complete match with the `=>` arrow |

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

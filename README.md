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

## The rules file
The rules file tells lex how to split up your code, it must have the file extension `.lexif`

### Structure
The rules file has different headings to keep the rules organised. Each heading starts with `#`

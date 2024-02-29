import re

# Token types
TOKEN_TYPES = {
    'IDENTIFIER': r'[a-zA-Z_]\w*',
    'INTEGER': r'\d+',
    'OPERATOR': r'[+*<>&.@/:=˜|$!#%^_[\]{}"‘?]',
    'STRING': r"'(?:\\[tn\'\\]|[^'\n])*'",
    'SPACE': r'\s+',
    'COMMENT': r'//.*',
    'EOL': r'\n',
}

# Regular expression for tokenization
TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

def tokenize(program):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, program):
        for name, value in match.groupdict().items():
            if value is not None:
                tokens.append((name, value))
    return tokens

# Sample RPAL program
# rpal_program = """
# let Sum(A) = Psum (A, Order A)
# where
#   rec Psum(T, N) = N eq 0 -> 0 | Psum(T, N-1) + T
# in
#   Print(Sum(1,2,3,4,5))
# """
f = open("RPAL.txt", 'r')
rpal_program = f.read()


# Tokenize the RPAL program
tokens = tokenize(rpal_program)
print(tokens)

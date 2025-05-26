# lexer.py
import re

# Her token türü için bir düzenli ifade tanımı
token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),    # Tam veya ondalıklı sayı
    ('ID',       r'[A-Za-z_]\w*'),   # Değişken veya fonksiyon adı
    ('OP',       r'\+|\-|\*|\/|==|!=|<=|>=|<|>'),   # Operatörler (aritmetik & karşılaştırma)
    ('ASSIGN',   r'='),             # Atama operatörü
    ('NEWLINE',  r'\n'),            # Satır sonu
    ('SKIP',     r'[ \t]+'),        # Boşluk ve tab (atlanacak)
    ('COMMENT',  r'\#.*'),          # Yorum satırı (# ile başlayan)
    ('LPAREN',   r'\('),            # Sol parantez
    ('RPAREN',   r'\)'),            # Sağ parantez
    ('COLON',    r':'),             # İki nokta
    ('COMMA',    r','),             # Virgül
    ('MISMATCH', r'.'),             # Beklenmeyen karakter
]
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

# Anahtar kelimeler kümesi
keywords = {'if', 'else', 'while', 'for', 'def', 'return', 'in'}

class Token:
    """Bir token objesi: tür, değer, satır ve sütun bilgisi içerir."""
    def __init__(self, type, value, line, column):
        self.type   = type
        self.value  = value
        self.line   = line
        self.column = column
    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, line={self.line}, col={self.column})'

def lex(code):
    """
    Kaynak kodunu satır satır okuyarak Token dizisi üretir.
    Girdi, girintilere (INDENT/DEDENT) göre de tokenlara bölünür.
    """
    tokens = []
    lines = code.splitlines(keepends=True)
    indent_stack = [0]
    line_num = 1
    for line in lines:
        pos = 0
        # Satır başındaki boşluk sayısını ölçerek girinti (indent) hesaplanır
        indent = 0
        while pos < len(line) and line[pos] == ' ':
            indent += 1
            pos += 1
        stripped = line[pos:].strip('\r\n')
        if stripped == '':
            # Boş satırsa boş satırlardaki indent değişimi ignore edilir
            line_num += 1
            continue
        # Yeni bir blok girintisi varsa INDENT token ekle
        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            tokens.append(Token('INDENT', indent, line_num, 1))
        # Girinti azalıyorsa gereken sayıda DEDENT token ekle
        while indent < indent_stack[-1]:
            indent_stack.pop()
            tokens.append(Token('DEDENT', indent_stack[-1], line_num, pos+1))
        # Kalan kısımda tokenları regex ile ayır
        mo = get_token(line[pos:])
        col = pos
        while mo:
            kind = mo.lastgroup
            val  = mo.group()
            if kind == 'ID' and val in keywords:
                kind = 'KEYWORD'   # Anahtar kelime ise türünü KEYWORD yap
            if kind == 'NEWLINE':
                tokens.append(Token('NEWLINE', '', line_num, col+1))
                break
            elif kind == 'SKIP':
                pass  # boşluk/tab atla
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Beklenmeyen karakter {val!r} (satır {line_num})')
            else:
                if kind == 'COMMENT':
                    tokens.append(Token('COMMENT', val.strip(), line_num, col+1))
                    break  # yorumdan sonrası tokenize edilmez
                tokens.append(Token(kind, val, line_num, col+1))
            end = mo.end()
            col += end
            mo = get_token(line[pos+col-pos:])
        line_num += 1
    # Dosya sonu: açık girintileri kapat (DEDENT) ve EOF tokenı ekle
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Token('DEDENT', indent_stack[-1], line_num, 1))
    tokens.append(Token('EOF', '', line_num, 1))
    return tokens

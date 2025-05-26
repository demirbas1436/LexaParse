# parser.py
class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0]

    def error(self, msg):
        tok = self.current_token
        raise ParseError(f"Satır {tok.line}, sütun {tok.column}: {msg}, (bu token: '{tok.value}')")

    def consume(self, tok_type, value=None):
        """Beklenen türde tokenı yerinden tüket, değilse hata."""
        if (self.current_token.type == tok_type and
            (value is None or self.current_token.value == value)):
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            expected = value if value else tok_type
            self.error(f"Beklenen {expected}")

    def parse(self):
        """Programı baştan sona ayrıştır (statements), sonra dosya sonu gelmeli."""
        self.statements()
        if self.current_token.type != 'EOF':
            self.error("Dosya sonuna beklenmeyen girdi")

    def statements(self):
        """Birden fazla satırı ayrıştır."""
        # Geçerli token bir satır başlangıcı ise döngüye devam et
        while self.current_token.type in ('KEYWORD', 'ID'):
            val = self.current_token.value
            if val == 'if':
                self.if_statement()
            elif val == 'while':
                self.while_statement()
            elif val == 'for':
                self.for_statement()
            elif val == 'def':
                self.function_def()
            elif val == 'return':
                self.return_statement()
            else:
                # Atama veya ifade satırı
                self.simple_statement()

    def simple_statement(self):
        """Atama veya ifade satırı."""
        if self.current_token.type == 'ID':
            # Atama mı kontrol et
            if self.tokens[self.pos+1].type == 'ASSIGN':
                self.assignment()
            else:
                self.expression()
        else:
            self.error("Geçersiz ifade başlangıcı")
        # Satır sonu bekle
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')
        elif self.current_token.type in ('DEDENT', 'EOF'):
            return
        else:
            self.error("Satır sonu bekleniyor")

    def assignment(self):
        """ID = expression."""
        self.consume('ID')
        self.consume('ASSIGN')
        self.expression()

    def return_statement(self):
        """return expression."""
        self.consume('KEYWORD', 'return')
        self.expression()
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')
        elif self.current_token.type not in ('DEDENT', 'EOF'):
            self.error("Satır sonu bekleniyor")

    def if_statement(self):
        self.consume('KEYWORD', 'if')
        self.expression()
        self.consume('COLON')
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')
        else:
            self.error("if sonrasında yeni satır bekleniyor")
        # if bloğu
        if self.current_token.type == 'INDENT':
            self.consume('INDENT')
            self.statements()
            self.consume('DEDENT')
        else:
            self.error("if bloğu için girinti bekleniyor")
        # else/elif blokları
        while self.current_token.type == 'KEYWORD' and self.current_token.value == 'elif':
            self.consume('KEYWORD', 'elif')
            self.expression()
            self.consume('COLON')
            if self.current_token.type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                self.error("elif sonrasında yeni satır bekleniyor")
            if self.current_token.type == 'INDENT':
                self.consume('INDENT')
                self.statements()
                self.consume('DEDENT')
            else:
                self.error("elif bloğu için girinti bekleniyor")
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
            self.consume('KEYWORD', 'else')
            self.consume('COLON')
            if self.current_token.type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                self.error("else sonrasında yeni satır bekleniyor")
            if self.current_token.type == 'INDENT':
                self.consume('INDENT')
                self.statements()
                self.consume('DEDENT')
            else:
                self.error("else bloğu için girinti bekleniyor")
        # if satır sonu (opsiyonel)
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')

    def while_statement(self):
        self.consume('KEYWORD', 'while')
        self.expression()
        self.consume('COLON')
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')
        else:
            self.error("while sonrasında yeni satır bekleniyor")
        if self.current_token.type == 'INDENT':
            self.consume('INDENT')
            self.statements()
            self.consume('DEDENT')
        else:
            self.error("while bloğu için girinti bekleniyor")
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')

    def for_statement(self):
        self.consume('KEYWORD', 'for')
        self.consume('ID')
        self.consume('KEYWORD', 'in')
        self.expression()
        self.consume('COLON')
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')
        else:
            self.error("for sonrasında yeni satır bekleniyor")
        if self.current_token.type == 'INDENT':
            self.consume('INDENT')
            self.statements()
            self.consume('DEDENT')
        else:
            self.error("for bloğu için girinti bekleniyor")
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')

    def function_def(self):
        self.consume('KEYWORD', 'def')
        self.consume('ID')
        self.consume('LPAREN')
        # Parametreler (opsiyonel)
        if self.current_token.type == 'ID':
            self.consume('ID')
            while self.current_token.type == 'COMMA':
                self.consume('COMMA')
                self.consume('ID')
        self.consume('RPAREN')
        self.consume('COLON')
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')
        else:
            self.error("def sonrasında yeni satır bekleniyor")
        if self.current_token.type == 'INDENT':
            self.consume('INDENT')
            self.statements()
            self.consume('DEDENT')
        else:
            self.error("Fonksiyon gövdesi için girinti bekleniyor")
        if self.current_token.type == 'NEWLINE':
            self.consume('NEWLINE')

    def expression(self):
        """Karşılaştırmalı ifadeyi ayrıştır."""
        self.compare_expr()

    def compare_expr(self):
        self.add_expr()
        # Karşılaştırma operatörleri
        while self.current_token.type == 'OP' and self.current_token.value in ('==','!=','<','>','<=','>='):
            self.consume('OP')
            self.add_expr()

    def add_expr(self):
        self.term()
        # Toplama/Çıkarma
        while self.current_token.type == 'OP' and self.current_token.value in ('+','-'):
            self.consume('OP')
            self.term()

    def term(self):
        self.factor()
        # Çarpma/Bölme
        while self.current_token.type == 'OP' and self.current_token.value in ('*','/'):
            self.consume('OP')
            self.factor()

    def factor(self):
        tok = self.current_token
        if tok.type == 'OP' and tok.value == '-':
            # Unary minus
            self.consume('OP')
            self.factor()
        elif tok.type == 'NUMBER':
            self.consume('NUMBER')
        elif tok.type == 'ID':
            self.consume('ID')
            # Fonksiyon çağrısı kontrolü
            if self.current_token.type == 'LPAREN':
                self.consume('LPAREN')
                if self.current_token.type != 'RPAREN':
                    self.expression()
                    while self.current_token.type == 'COMMA':
                        self.consume('COMMA')
                        self.expression()
                self.consume('RPAREN')
        elif tok.type == 'LPAREN':
            self.consume('LPAREN')
            self.expression()
            self.consume('RPAREN')
        else:
            self.error("Sayı, değişken adı veya '(' bekleniyordu")

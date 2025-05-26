# main.py
import tkinter as tk
from lexical_analyzer import lex, Token
from parser import Parser, ParseError

def run_editor():
    root = tk.Tk()
    root.title("Python-Benzeri Dil Editörü")
    # Metin alanı (Text widget)
    text = tk.Text(root, wrap="none", font=("Consolas", 12))
    text.pack(expand=True, fill="both")
    # Tag tanımlamaları: renkler
    text.tag_configure("keyword", foreground="blue")
    text.tag_configure("number",  foreground="purple")
    text.tag_configure("comment", foreground="green")
    text.tag_configure("operator",foreground="orange")
    # Durum çubuğu (hata mesajları)
    status = tk.Label(root, text="Kodunuzu yazın...", anchor="w")
    status.pack(fill="x")

    def on_key_release(event=None):
        code = text.get("1.0", "end-1c")
        try:
            all_tokens = lex(code)
            tokens = [t for t in all_tokens if t.type != "COMMENT"]
        except SyntaxError as e:
            status.config(text=str(e))
            return
        # Eski tag'leri temizle
        for tag in ("keyword", "number", "comment", "operator"):
            text.tag_remove(tag, "1.0", "end")
        # Yeni tag'leri uygula
        for token in all_tokens:
            if token.type == "KEYWORD":
                tag = "keyword"
            elif token.type == "NUMBER":
                tag = "number"
            elif token.type == "COMMENT":
                tag = "comment"
            elif token.type in ("OP", "ASSIGN"):
                tag = "operator"
            else:
                continue
            start = f"{token.line}.{token.column - 1}"
            end = f"{token.line}.{token.column - 1 + len(token.value)}"
            try:
                text.tag_add(tag, start, end)
            except tk.TclError:
                pass
        # Ayrıştırma (syntax kontrol)
        try:
            parser = Parser(tokens)
            parser.parse()
            status.config(text="Geçerli sözdizimi")
        except ParseError as e:
            status.config(text=str(e))

    text.bind("<KeyRelease>", on_key_release)
    on_key_release()
    root.mainloop()

if __name__ == "__main__":
    run_editor()

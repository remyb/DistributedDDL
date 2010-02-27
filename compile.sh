#/bin/bash
echo "[*] Removing Dirty Files..."
rm sql.tokens sqlLexer.* sqlParser.*
echo "[*] Compiling new Grammer..."
java org.antlr.Tool sql.g
echo "[*] Converting Config File to Python Format..."
echo "[*] Done."

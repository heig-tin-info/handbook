from fontTools.ttLib import TTFont
import os

# Caractère à rechercher
char = ";"
codepoint = ord(char)

# Répertoire contenant les polices (ajoutez d'autres répertoires si nécessaire)
font_dirs = ["/usr/share/fonts", "~/.fonts", "~/.local/share/fonts"]

for font_dir in font_dirs:
    for root, dirs, files in os.walk(os.path.expanduser(font_dir)):
        for file in files:
            if file.endswith((".ttf", ".otf")):
                font_path = os.path.join(root, file)
                try:
                    font = TTFont(font_path)
                    for table in font["cmap"].tables:
                        if codepoint in table.cmap:
                            print(f"Font: {font_path} supports {char}")
                            break
                except:
                    continue

import subprocess
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont
import os
import pandas as pd
from typing import List, Union


class Fonts:
    """Manage system fonts using fc-list."""

    def __init__(self):
        self.fonts_db = pd.DataFrame(
            columns=["file", "family", "style", "charset", "languages", "fullname"]
        )
        self.load_fonts()

    def load_fonts(self):
        try:
            result = subprocess.run(
                [
                    "fc-list",
                    "-f",
                    "%{file}:::%{family[0]}:::%{style}:::%{charset}:::%{lang}:::%{fullname}\n",
                ],
                stdout=subprocess.PIPE,
            )

            rows = []
            for entry in result.stdout.decode("utf-8").split("\n"):
                if entry.strip():
                    file_path, family, style, charset, languages, fullname = (
                        entry.split(":::")
                    )
                    rows.append(
                        {
                            "file": file_path,
                            "family": family,
                            "style": style,
                            "charset": charset,
                            "languages": languages,
                            "fullname": fullname,
                        }
                    )

            self.fonts_db = pd.concat(
                [self.fonts_db, pd.DataFrame(rows)], ignore_index=True
            )

        except Exception as e:
            print(f"Erreur lors du chargement des polices: {str(e)}")

    def create(self):
        """Initialize the Fonts database."""
        self.load_fonts()

    def find_char(self, c: str) -> pd.DataFrame:
        """List fonts that contain the character c."""
        char_code = ord(c)

        def char_in_charset(charset):
            for interval in charset.split():
                parts = list(map(lambda x: int(x, 16), interval.split("-")))
                if len(parts) == 1:  # It's a single character
                    start = end = parts[0]
                else:
                    start, end = parts
                if start <= char_code <= end:
                    return True
            return False

        return self.fonts_db[self.fonts_db["charset"].apply(char_in_charset)]

    def find_font(self, pattern: str) -> pd.DataFrame:
        """List fonts using a pattern, e.g., Noto*rew."""
        return self.fonts_db[
            self.fonts_db["fullname"].str.contains(pattern, regex=True, na=False)
        ]

    def generate_font_with_char(self, chars: Union[str, List[str]], output_name: str):
        """Generate a single font with the given characters."""
        if isinstance(chars, str):
            chars = [chars]

        char_set = set(ord(c) for c in chars)

        # Recherche des polices compatibles
        compatible_fonts = []

        for _, row in self.fonts_db.iterrows():
            charset_set = parse_intervals(row["charset"])
            if any(c in charset_set for c in char_set):
                compatible_fonts.append(row["file"])

        if not compatible_fonts:
            print("Aucune police compatible trouvée.")
            return

        # Utiliser la première police compatible pour générer le sous-ensemble
        output_dir = "output_fonts"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"{output_name}.ttf")
        ttfont = TTFont(compatible_fonts[0])  # Utiliser la première police compatible

        subsetter = Subsetter()
        subsetter.populate(unicodes=char_set)
        subsetter.subset(ttfont)

        ttfont.save(output_path)
        print(f"Police générée: {output_path}")


# Utilitaires
def parse_intervals(interval_string):
    intervals = interval_string.split()
    char_set = set()

    for interval in intervals:
        if "-" in interval:
            start, end = interval.split("-")
            start = int(start, 16)
            end = int(end, 16)
            char_set.update(range(start, end + 1))
        else:
            char_set.add(int(interval, 16))

    return char_set


def is_in_intervals(char_code, interval_set):
    return char_code in interval_set


# Exemple d'utilisation
fonts = Fonts()
fonts.create()

# Rechercher des polices contenant un caractère spécifique
result = fonts.find_char("א")  # Caractère hébreu Aleph
print(result)

# Rechercher des polices par pattern
result = fonts.find_font("Noto.*Hebrew")
print(result)

# Générer une police avec des caractères spécifiques
fonts.generate_font_with_char(["א", "😊", "©"], "CustomSubset")

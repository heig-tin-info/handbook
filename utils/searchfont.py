"""Script to search for fonts supporting a specific character."""

import argparse
import os

from fontTools.ttLib import TTFont, TTLibError


def find_fonts_with_character(char: str) -> None:
    """Search for fonts supporting a specific character.

    Args:
        char: The character to search for in fonts.
    """
    codepoint = ord(char)

    # Répertoire contenant les polices (ajoutez d'autres répertoires si nécessaire)
    font_dirs = ["/usr/share/fonts", "~/.fonts", "~/.local/share/fonts"]

    found_count = 0

    for font_dir in font_dirs:
        expanded_dir = os.path.expanduser(font_dir)

        # Vérifier si le répertoire existe
        if not os.path.exists(expanded_dir):
            continue

        for root, dirs, files in os.walk(expanded_dir):
            for file in files:
                if file.endswith((".ttf", ".otf")):
                    font_path = os.path.join(root, file)
                    try:
                        font = TTFont(font_path)
                        for table in font["cmap"].tables:
                            if codepoint in table.cmap:
                                print(
                                    f"Font: {font_path} supports '{char}' (U+{codepoint:04X})"
                                )
                                found_count += 1
                                break
                        font.close()
                    except (TTLibError, KeyError, OSError):
                        # TTLibError: erreur de lecture de la police
                        # KeyError: table 'cmap' manquante
                        # OSError: problème d'accès au fichier
                        continue

    if found_count == 0:
        print(
            f"Aucune police trouvée supportant le caractère '{char}' (U+{codepoint:04X})"
        )
    else:
        print(f"\n{found_count} police(s) trouvée(s) au total.")


def main():
    """Parse arguments and run the font search."""
    parser = argparse.ArgumentParser(
        description="Search for fonts supporting a specific character."
    )
    parser.add_argument(
        "char", type=str, help="The character to search for (e.g., ';' or 'é')"
    )
    parser.add_argument(
        "--dirs",
        nargs="+",
        default=["/usr/share/fonts", "~/.fonts", "~/.local/share/fonts"],
        help="Additional font directories to search",
    )

    args = parser.parse_args()

    if len(args.char) != 1:
        parser.error("Le caractère doit être un seul caractère Unicode")

    find_fonts_with_character(args.char)


if __name__ == "__main__":
    main()

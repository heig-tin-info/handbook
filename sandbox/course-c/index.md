# Bases {#my-heading}

## Exercices de révision

Table: Modèle de données

| Modèle | `short` | `int` | `long` | `long long` | `size_t` | Système d'exploitation                                                                                                    |
| ---------------- | ------- | ----- | ------ | ----------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| **LP32**         | 16      | 16    | 32     |             | 32       | Windows 16-bits, Apple Macintosh                                                                             |
| **ILP32**        | 16      | 32    | 32     | 64          | 32       | Windows x86, Linux/Unix 32-bits                                                                                           |
| **LLP64**        | 16      | 32    | 32     | 64          | 64       | [Microsoft Windows](https://en.wikipedia.org/wiki/Microsoft_Windows) x86-64, [MinGW](https://en.wikipedia.org/wiki/MinGW) |
| **LP64**         | 16      | 32    | 64     | 64          | 64       | Unix, Linux, macOS, Cygwin                                                                                                |
| **ILP64**        | 16      | 64    | 64     | 64          | 64       | [HAL](https://en.wikipedia.org/wiki/HAL_Computer_Systems) (SPARC)                                                         |
| **SILP64**       | 64      | 64    | 64     | 64          | 64       | [UNICOS](https://en.wikipedia.org/wiki/UNICOS) (Super ordinateur)                                                         |

??? note "Autres alphabets"

    Le système d'écriture coréen (Hangul) est alphasyllabique, c'est-à-dire que chaque caractère représente une syllabe. Les lettres de base sont composées de 14 consonnes de base et 10 voyelles. Quant aux chiffres ils sont les mêmes qu'en occident.

    ```text
    ㄱ (g), ㄴ (n), ㄷ (d), ㄹ (r/l), ㅁ (m), ㅂ (b), ㅅ (s), ㅇ (ng), ㅈ (j), ㅊ (ch), ㅋ (k), ㅌ (t), ㅍ (p), ㅎ (h)

    ㅏ (a), ㅑ (ya), ㅓ (eo), ㅕ (yeo), ㅗ (o), ㅛ (yo), ㅜ (u), ㅠ (yu), ㅡ (eu), ㅣ (i)
    ```

    Les japonais utilisent trois systèmes d'écriture, le Hiragana, le Katakana et le Kanji. Les deux premiers sont des syllabaires et le dernier est un système d'écriture logographique. Le Hiragana et Katakana ont tous deux 46 caractères de base. Voici l'exemple du Katakana:

    ```text
    あ (a), い (i), う (u), え (e), お (o)
    か (ka), き (ki), く (ku), け (ke), こ (ko)
    さ (sa), し (shi), す (su), せ (se), そ (so)
    た (ta), ち (chi), つ (tsu), て (te), と (to)
    な (na), に (ni), ぬ (nu), ね (ne), の (no)
    は (ha), ひ (hi), ふ (fu), へ (he), ほ (ho)
    ま (ma), み (mi), む (mu), め (me), も (mo)
    や (ya), ゆ (yu), よ (yo)
    ら (ra), り (ri), る (ru), れ (re), ろ (ro)
    わ (wa), を (wo)
    ん (n)
    ```text
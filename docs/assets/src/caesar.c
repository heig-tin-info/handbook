void caesar(char str[], unsigned key)
{
    key %= 26;

    for (int i = 0; str[i]; i++)
    {
        char c = str[i];

        if (c >= 'a' && c <= 'z')
        {
            str[i] = ((c + key > 'z') ? c - 'z' + 'a' - 1 : c) + key;
        }
        else if (c >= 'A' && c <= 'Z')
        {
            str[i] = ((c + key > 'Z') ? c - 'Z' + 'A' - 1 : c) + key;
        }
    }
}

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
int shift(char c);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }

    int key_length = strlen(argv[1]);

    for (int i = 0; i < key_length; i++)
    {
        if ( isalpha(argv[1][i]) == 0)
        {
            printf("Usage: ./vigenere keyword\n");
            return 1;
        }
    }

    string keyword = argv[1];
    int key = 0;
    string text = get_string("plaintext: ");
    printf("ciphertext:");

    for (int i = 0, j = 0; i < strlen(text); i++)
    {
    if (isalpha(text[i]) > 0)
    {
        key = shift(tolower(keyword[(j) % key_length]))-97;
        if (islower(text[i]) == 0)
        {
            char changing_latter = (tolower(text[i]) - 97 + key)%26 + 97;
            printf("%c", toupper(changing_latter));
            j++;
        }
        else
        {
            char changing_latter = (text[i] - 97 + key)%26 + 97;
            printf("%c", changing_latter);
            j++;
        }
    }
    else
    {
        printf("%c", text[i]);
    }
    }
    printf("\n");
    return 0;
}


int shift(char c)
{
        return c;
}
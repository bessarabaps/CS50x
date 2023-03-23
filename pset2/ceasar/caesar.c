#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        string skey = argv[1];
        int only_int = 1;
        for (int i = 0; i < strlen(skey); i++)
        {
            if ( isdigit(skey[i]) == 0)
            {
                only_int = 0;
            }
        }
        if (only_int == 1)
        {
            int ikey = atoi(skey);
            string text = get_string("plaintext: ");
            printf("ciphertext:");
            for (int i = 0; i < strlen(text); i++)
            {
                if (isalpha(text[i]) > 0)
                {
                    int lower_latter = 1;
                    if (islower(text[i]) == 0)
                    {
                        char changing_latter = (tolower(text[i]) - 97 + ikey)%26 + 97;
                        printf("%c", toupper(changing_latter));
                    }
                    else
                    {
                        char changing_latter = (text[i] - 97 + ikey)%26 + 97;
                        printf("%c", changing_latter);

                    }
                }
                else
                {
                    printf("%c", text[i]);
                }
            }
            printf("\n");
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
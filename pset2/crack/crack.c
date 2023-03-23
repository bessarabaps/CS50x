#define _XOPEN_SOURCE

#include <unistd.h>
#include <crypt.h>
#include <stdio.h>
#include <string.h>
#include <cs50.h>


int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: crack <hash>\n");
        return 1;
    }

    const int letters_number = 53;

    string letters = "\0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string hash = argv[1];

    char salt[3];
    salt[0] = argv[1][0];
    salt[1] = argv[1][1];

    char key[6] = "";

    for (int five = 0; five < letters_number; five++)
    {
        for (int four = 0; four < letters_number; four++)
        {
            for (int three = 0; three < letters_number; three++)
            {
                for (int two = 0; two < letters_number; two++)
                {
                    for (int one = 0; one < letters_number; one++)
                    {
                        key[0] = letters[one];
                        key[1] = letters[two];
                        key[2] = letters[three];
                        key[3] = letters[four];
                        key[4] = letters[five];

                        if (strcmp(crypt(key, salt), hash) == 0)
                        {
                            printf("%s\n", key);
                            return 0;
                        }
                    }
                }
            }
        }
    }

    printf("Password couldn't be cracked!\n");

    return 2;
}
#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int coins = 0;
    float dollars = 0;
    do
    {
    dollars  = get_float("Change,$: ");   
    }
    while (dollars < 0);
    int cents = round(dollars * 100);
    while (cents > 0)
    {
        if (cents >= 25)
        {
            coins += 1;
            cents -= 25;
        }
        else if (cents >= 10)
        {
            coins += 1;
            cents -= 10;
        }
        else if (cents >= 5)
        {
            coins += 1;
            cents -= 5;
        }
        else if (cents >= 1)
        {
            coins += 1;
            cents -= 1;
        }
             
    }
    printf("I have, %i coin(s)\n", coins);
}

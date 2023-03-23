#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number = 0;
    long x1 = 0;
    long x2 = 0;
    int x1sum = 0;
    int x2sum = 0;
    int sum = 0;
    
    do
    {
        number = get_long("Card number: ");
    }
    while (number <= 0);
    
    for (x1 = number, x1sum = 0; x1 > 0; x1 /=100)
    {
        x1sum += x1 % 10;    
    }
        
    
    for (x2 = number / 10, x2sum = 0; x2 > 0; x2 /=100)
    {
        if (2 * (x2 % 10) > 9)
        {
            x2sum += (2 * (x2 % 10)) / 10;
            x2sum += (2 * (x2 % 10)) % 10;
        }
        else
            {
                x2sum += 2 * (x2 % 10);
            }
    }
    
    sum = x1sum + x2sum;
    
    if (sum % 10 == 0)
    {
        if ((number >= 340000000000000 && number < 350000000000000) ||
        (number >= 370000000000000 && number < 380000000000000))
        {
            printf("AMEX\n");
        }
        else if (number >= 5100000000000000 && number < 5600000000000000)
        {
            printf("MASTERCARD\n");
        }
        else if ((number >= 4000000000000 && number < 5000000000000) ||
         (number >= 4000000000000000 && number < 5000000000000000))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }   
    }
    else
    {
        printf("INVALID\n");
    }
}
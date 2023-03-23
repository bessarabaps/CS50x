#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int Height = 0;
    while (Height < 1 || Height > 8)
    {
     Height  = get_int("Height(1...8): ");   
    }
    Height++; 
    for (int i = 1; i < Height; i++)
    {
        for (int c = Height-1; c != i; c--)
        {            
            printf(" ");
        }
        for (int b = 0; b < i; b++)
        {     
            printf("#");
        }
        printf("\n");
    } 
}

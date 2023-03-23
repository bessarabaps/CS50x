#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }

    char *infile = argv[1];

    FILE *img;
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    unsigned char buffer[512];
    int count = 0;
    bool NewP = true;
    char filename[7];

    while (fread(buffer, 512, 1, inptr) == 1)
    {

        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (NewP == false)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            NewP = false;
            count++;
        }
        if (NewP == false)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    fclose(inptr);
    fclose(img);

    return 0;
}

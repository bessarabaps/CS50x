// Increase/decrease a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        fprintf(stderr, "Usage: n infile outfile\n");
        return 1;
    }

    bool increase = true;
    float f = atof(argv[1]);
    int n = 1;
    if ( f < 0.0 || f > 100)
    {
        fprintf(stderr, "n is not in range\n");
        return 5;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }


    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bfR;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfR = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, biR;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    biR = bi;

    if (f < 1)
    {
        increase = false;
        n = ceil(1/f);
        biR.biWidth = ceil(bi.biWidth * f);
        biR.biHeight = ceil(bi.biHeight * f);
    }
    else
    {
        increase = true;
        n = ceil(f);
        //updating outptr header info
        biR.biWidth = bi.biWidth * n;
        biR.biHeight = bi.biHeight * n;
    }

     // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int out_padding = (4 - (biR.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    //updating outptr header info
    biR.biSizeImage = abs(biR.biHeight)  * (biR.biWidth * sizeof(RGBTRIPLE) + out_padding);
    bfR.bfSize = biR.biSizeImage + bf.bfOffBits;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfR, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biR, sizeof(BITMAPINFOHEADER), 1, outptr);

    if (increase == false)
    {
        int p = 1;
        for (int i = 0, biHeight = abs(biR.biHeight); i < biHeight; i++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                if(p < n)
                {
                    fseek(outptr, -(sizeof(RGBTRIPLE)), SEEK_CUR);
                    p++;
                }
                else if( p == n)
                {
                    p = 1;
                }
            }

            // skip over padding, if any
            fseek(inptr, padding, SEEK_CUR);

            // then add it back (to demonstrate how)
            for (int k = 0; k < out_padding; k++)
            {
                fputc(0x00, outptr);
            }
            fseek(inptr, ((bi.biWidth * sizeof(RGBTRIPLE)) + padding)*(n-1), SEEK_CUR);
        }
    }
    else
    {
        // iterate over infile's scanlines
        for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
        {
            for (int z = 0; z < n; z++)
            {
                // iterate over pixels in scanline
                for (int j = 0; j < bi.biWidth; j++)
                {
                    // temporary storage
                    RGBTRIPLE triple;

                    // read RGB triple from infile
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                    // write RGB triple to outfile
                    for (int x = 0; x < n; x++)
                    {
                        fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                    }
                }

                // then add it back (to demonstrate how)
                for (int k = 0; k < out_padding; k++)
                {
                    fputc(0x00, outptr);
                }

                if (z < n - 1)
                {
                    fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
                }
            }

            // skip over padding, if any
            fseek(inptr, padding, SEEK_CUR);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
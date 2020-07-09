#include <stdio.h>
#include <stdlib.h>

void main()
{
    int n = 0;
    scanf("%d", &n);
    int s = 0;
    int p = 0;
    while (n > 0)
    {
        s = s + n;
        p = p*n;
        n = n - 1;
    }        
    printf("somme = %d, produit = %d", s, p);
}

/*
For < 16 , p>

void main()
{
    int n = 0;
 -> scanf("%d", &n);
    int s = 0;
 -> int p = 0;
 -> while (n > 0)
 -> {
        s = s + n;
 -----> p = p*n;
 -----> n = n - 1;
 -> }        
 -> printf("somme = %d, produit = %d", s, p);
}

*/
#include <stdio.h>
#include <stdlib.h>

void main()
{
    int a = 1;          
    int b = 2;
    int c = a;
    if(b == 2)
    {
        c  = 10;
    }
    printf("a = %d\n", a);
    printf("b = %d\n", b);
    printf("c = %d", c);
}



/*
For < 15 , c>

void main()
{
    int a = 1;
 -> int b = 2;
    int c = a;
 -> if(b == 2)
 -> {
 -----> c  = 10;
 -> }
    printf("a = %d\n", a);
    printf("b = %d\n", b);
 -> printf("c = %d", c);
}

*/
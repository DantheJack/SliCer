#include <stdio.h>
#include <stdlib.h>

void main()
{
    int f = 1;
    int t = 2;
    int g = f + t;
    int h = f + 4;
    f = 4;
    t = t + 1;
    h = g + t;
    return h;
}


/*
For < 13 , h>

void main()
{
 -> int f = 1;
 -> int t = 2;
 -> int g = f + t;
    int h = f + 4;
    f = 4;
 -> t = t + 1;
 -> h = g + t;
 -> return h;
}

*/
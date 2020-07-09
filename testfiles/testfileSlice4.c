
    int x = 1;          //
    int y = 8;
    int z = y + x;
    int i = 0;
    x = z * 2;          
    z = 24;

    do
    {
        x += x;
        for (i = 0; i < y; ++i) { }
    }

    z = y + x;
    print(x)



/*
For < ... , x >

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

*/
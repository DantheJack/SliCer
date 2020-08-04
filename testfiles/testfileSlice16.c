int a = 0;
int b = 0;
int c = 0;
int d = 0;
int e = 0;
int f = 0;

if(a == 0)
{
    b = 1;              // And the same goes for this line.
}
else if (c > d)
{
    b = 2               // While this line is not, because line 23 can never be executed after it.
}
else
{
    b = 3;              // This line is the very first definition of b that is meaningful for us
    if(e == 0)
    {
        b = 4;          // This line neither, obviously.
    }
    else if (f == a)
    {
        b = 5;          // But this line will not, since it cannot have any influence on line 23 !
    }
    else
    {
        f = b;          // Of course, this line is  going to be part of the slice
    }
}
    
return c ;


/*
0 .      --> [0, 0].   int a = 0 ;
1 .      --> [1, 1].   int b = 0 ;
2 .      --> [2, 2].   int c = 0 ;
3 .      --> [3, 3].   int d = 0 ;
4 .      --> [4, 4].   int e = 0 ;
5 .      --> [5, 5].   int f = 0 ;
6 .      --> [6, 6].   if ( a == 0 )
7 .      --> [7, 7].   {
8 .      --> [8, 8].   b = 1 ;
9 .      --> [9, 9].   }
10 .     --> [10, 10].   else
11 .     --> [10, 10].   {
12 .     --> [10, 10].   if ( c > d )
13 .     --> [11, 11].   {
14 .     --> [12, 12].   b = 2
15 .     --> [13, 13].   }
16 .     --> [14, 14].   else
17 .     --> [15, 15].   {
18 .     --> [16, 16].   b = 3 ;
19 .     --> [17, 17].   if ( e == 0 )
20 .     --> [18, 18].   {
21 .         [19, 19].   b = 4 ;
22 .     --> [20, 20].   }
23 .     --> [21, 21].   else
24 .     --> [21, 21].   {
25 .     --> [21, 21].   if ( f == a )
26 .     --> [22, 22].   {
27 .         [23, 23].   b = 5 ;
28 .     --> [24, 24].   }
29 .     --> [25, 25].   else
30 .     --> [26, 26].   {
31 .     --> [27, 27].   f = b ;
32 .     --> [28, 28].   }
33 .     --> [28, 28].   }
34 .     --> [29, 29].   }
35 .     --> [29, 29].   }
36 .         [30, 30].   return c ;
*/

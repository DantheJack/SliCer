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

1  -  int a = 0 ;
2  -  int b = 0 ;
3  -  int c = 0 ;
4  -  int d = 0 ;
5  -  if ( a == 0 )
6  -  {
7  -    b = 1 ;
8  -  }
9  -  else
10  - {
11  -     if ( a > d )
12  -     {
13  -         b = 2
14  -     }
15  -     else
16  -     {
17  -         b = 3 ;
18  -         if ( d == 0 )
19  -         {
20  -             b = 4 ;
21  -         }
22  -         else
23  -         {
24  -             if ( d == a )
25  -             {
26  -                 b = 5 ;
27  -             }
28  -             else
29  -             {
30  -                 c = b ;
31  -             }
32  -         }
33  -     }
34  - }
35  - return c ;

*/
1;
2 ;
 3 ; 4 ;
 5 \
 6;
 7; 8\
    \
    9;
10, 11; 12\
13\
14   \
   15\
   ;16;
17\
;;18{
    19;
    20\
    ;
;21}\
22; ""23;24\
"" \\
25;
for(26; 27<28.29;30++)\
{
do{;}while (2);(31)int a32 =\
33\
;}


\
float for1 = 2;
signed  char unsignedint="";

\
//here it was interresting because the statement end with '}'
//therefore the new one used to start on line 19 with '\'. Even 
//tho the only interesting text is "22;" on line 20.

//another interesting thing at line 23 : the for is bug-free only if
//it doesn't contain any parenthesis !
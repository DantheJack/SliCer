1
"2"
3 "4"
"5 6" 7
"8\"9" 10
11"12"13""14"15
16"""17 
18" 19'20''
21'"22'"\"\""\"\""23 
24" 

 " 
25"26""
27
"28
"29"
30 = "\" 31 ? // \\ 32;";

/*the function stringReducer does not work for the following case :

    outside_the_string " inside_the_string
    outside_the_string_again " inside_the_string_again "

#the upper code describes how the compiler understand the use of
#an odd number of double quotes in a line. This code wont compile,
#so I decided not to implement this specific situation. Instead,
#stringReducer will consider the code working as if it is :

    outside_the_string " inside_the_string \
    also_inside_the_string " outside_the_string_again "
*/

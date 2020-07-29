int a = 0;
int b = 1;
int c;
c = 12;
if (c!=2)
{ for(int i; i < b; i++) { if((i == 2) || ((i == 4) || i ==6)){
    a += b;}}
}
if(!!c){
if ((a > 0) && b<100 ) printf("\na<0");
else if(a>-10)
{
printf("\na<0 and a>-10");
}
if (b > 0) printf("\nb<0");
else if (a == 0) {printf("\na=0"); a++;}
else if (c == 12) printf("\nc=12");
else if (c > 11){
printf("\nc>11"); b--;}
else printf("none");
}else  
 {printf("not at all");}


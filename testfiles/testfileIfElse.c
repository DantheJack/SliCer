void main (void){
int a = 0;
int b = 0;
int c;

if(a == 0) a = 1;
if(a == 0) {a = 2;}
if(a == 0){
     a = 3;
}
if(a == 0) a = 4;
else a = 5;
if(a == 0) {a = 6;} else a = 7;
if(a == 0){
     a = 8;
} else
{
    a = 9;
}
if(a == 0) a = 10; a = 11;
if(a == 0) {a = 12;} a = 13;

/*******/

if(a == 0) a = 14;
else for(a = 0; a < 0; a++){if(a != 0) {a = a + 15;}}

/*******/

if(b == 0) b = 1;
else if(b == 2) b = 3;

if(b == 4) {b = 5;}
else if(b == 6) b = 7; b = 8;

if(b == 9){
     b = 10;
}
else  if  (b == 11){
    b = 12;
}
b = 13;

if(b == 14) b = 15;
else if (b == 16) {
    b = 17;
} else if (b == 18) b = 19;

if(b == 20) b = 21;
else if (b == 22) b = 23; else if (b == 24) b = 25;
else if (b == 26){
    b = 27;
    b = 28;
} else if (b == 29) b = 30; b = 31;

if(b == 29) b = 30;
else if (b == 31)
{
    b = 32;
    if(b == 33)
    {
        b = 34;
    }
    else if (b == 35) {
        if(b == 41)b = 42;else if(b == 43){b = 44;if(b == 45){b = 46;}else if (b == 47) {b = 48;}}else  if(b == 49){b = 50;b = 51;}
        else b = 52;if(b == 53)b = 54;else b = 55;b = 56;
    }
}
else if (b == 37)
{
    b = 38;
    for(c = 0; c < 100; c++){
    if(a>b){
        while(a>b){
            if(a<b/4) a = a + 3;
            else if (a<b/3) {a = a + 2;
            for(int i = 0; i < a; i++){
                if (c < 200) c = c + 10;
            }
            } else if(a<b/2){
                if (b > 100){
                    if (a != 42) {a = a + 4;}
                }
            }
        }
        if(c * 2 == 280){
            b = b + a;
        }
        else b = b + b;
    }
    else if (b<c) { for(int j = 0; j < c; j++){
        c = (a + j) * 10;
    }b = 100;}
    else {
        while (a > b){ if(b != a) b = b+2; else if (a == b * 2) a += 1;}
    }
}
}
else b = 40;


}
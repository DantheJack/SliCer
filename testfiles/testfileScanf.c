int main(void)
{
char c;
FILE *fp;
fp = fopen("file.txt", "r");
char name[10], other[15][5], lastname[23];
double result;
char buffer[80];
int c2d_4 = 0;

c2d_4 += getc(stdin);

c = fgetc(fp);
printf("%c", c);
printf("\n Please Enter your Last Name: \n");
gets(lastname);
printf("Enter your name : " );

char bif[15];
printf("Enter a string: ");
gets(bif);
printf("string is: %s\n", bif);

int trial = ungetc ('+', stdin);

char buf[15];
int limit = 15;
fgets(buf, limit, stdin);
printf("fgets is: %s\n", buf);

char c3d;
printf("Enter character: ");
c3d = getchar();
printf("getchar is: %c\n", c3d);

c = getc (fp);
/* replace ! with + */
if( c == '!' ) {
  ungetc ('+', fp);
} else {
  ungetc(c, fp);
}
int end = 0;
return end = c +  buf + c3d + name + lastname + bif;
}
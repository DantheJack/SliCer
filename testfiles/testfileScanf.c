void main(void)
{

char name[10], other[15][5], lastname[23];

printf("Quel est votre nom ? ");
fgets(name, 10, stdin);
printf("Ah ! Vous vous appelez donc %s !\n\n", name);

printf("%c", name);
}
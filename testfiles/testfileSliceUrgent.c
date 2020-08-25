int main (void)
{
/*calculates sum and product and mean
 of every integer between 0 and n*/
     int n = 0;
     int sum;
     int product;
     float mean;
     mean = 0.0;
     sum = 0;
     product = 0;
     scanf("%d", &n);
     mean = n;   
     while ( n > 0)
     {
          printf("n = %d", n);
          sum += n;
          product = product * n;
          n = n - 1;
     }
     mean = product / mean;
     printf("%d, %d, %d", sum, product, mean);
}
          
          

    
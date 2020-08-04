main()
{
    int H;
    H = 0;
    float x[12];
    float var2, var3, var4 ;
    float var5, var1;
    float ssq;
    float avg;
    float dev;
    int  i, n;
    int settings_Variable1, settings_Variable2 = 0, settings_Variable3;
    var4 = 0 ;
    var2 = 0 ;
    settings_Variable1 = 1;
    if(settings_Variable1 != 0){
    ssq = 0 ;
    dev = 0;
    settings_Variable3 = 1;
    scanf ("%d", &n);
    for ( i = 0 ; i < n ; i = i + 1)
    {
        scanf ("%f", &x[i]);
        if(settings_Variable1 <= 0 && settings_Variable1 != -3) var2 = var2 + x[i];
        else if (settings_Variable1 == var2) ssq = ssq + x[i] * x[i];
        else if (settings_Variable3 == var2) ++settings_Variable2;
    }
    avg = var2 / n; H = 8;
    if(settings_Variable2 == 0)
    {
        settings_Variable2 = 1;
    }
    else for(i = 0 ; i < n ; i = i + 1) {
        if(settings_Variable2 <= 0 && settings_Variable2 != -3) var2 = var2 + x[i];
        else if (settings_Variable2 == var2) ssq = ssq + x[i] * x[i];
        else if (settings_Variable3 == var2) dev = -1; var2 *= 10;
    }}
    else{
        scanf ("%d",&dev);
        scanf ("%d",&settings_Variable3);
        dev = 2*dev;
        var3 = dev*var2;
        scanf ("%d",&avg);
        var1 = settings_Variable3 + avg;
        var3 = (ssq  - n * avg * avg) / (n - 1);
        var4 = (ssq  - var2 * avg) / (n - 1);
        if(var2 == 0) var2 = var2 * var2 / n;
        if(var2 > 18) var3 = 0; else if (var2 > 0) var3 = 14;
        else var3 = 14; if (var3 == 0 || var3 == 14){
            for (i = 0; i < dev; i++) { var3 += var2; }
            scanf ("%d",&var2);
            var2 = (ssq  -  var2 ) / (n - 1);
            var2 = 0 ;
        }
        else if (settings_Variable3 % 2 == 0){
        for ( i = 0 ; i < n ; i = i + 1)
        {
        dev = x[i] - avg ;
        var4 = dev ;
        var2 = dev * dev ; H = dev * 2;
        }} else {
            while (var2 > 0){
                var2 = 6; H = 3;
                var5 = (var2 - var4 * var4 / n ) / (n -1);
                var1 = var2 / (n - 1);
                printf("variance (two pass): %f \n",var1);
            }
        }
        var5 = (var2 - var4 * var4 / n ) / (n -1);
        printf("variance (two pass): %f \n",var1);
        var3 = var3 + var1;
        var1 = var2 / (n - 1);
        var2 = -1 + var5;
        ssq = avg + var2 + H;
        printf ("%d %d\n",var3,var1);
    }
}
main()
{
    float x[12];
    float var2, var3, var4 ;
    float var5, var1;
    float t1, t2;
    float ssq;
    float avg;
    float dev;
    int  i, n;
    int settings_Variable1, settings_Variable2 = 0, settings_Variable3;
    t2 = 0 ;
    t1 = 0 ;
    fgets(settings_Variable1, 1, stdin);
    int red, green, blue, yellow;
    int sweet,sour,salty,bitter;
    if(settings_Variable1 != 0){
    ssq = 0 ;
    dev = 0;
    fgets(settings_Variable3, 1, stdin);
    scanf ("%d", &n);
    for ( i = 0 ; i < n ; i = i + 1)
    {
        scanf ("%f", &x[i]);
        if(settings_Variable1 <= 0 && settings_Variable1 != -3) t1 = t1 + x[i];
        else if (settings_Variable1 == t1) ssq = ssq + x[i] * x[i];
        else if (settings_Variable3 == t1) ++settings_Variable2;
    }
    avg = t1 / n;
    if(settings_Variable2 == 0)
    {
        fgets(settings_Variable2, 1, stdin);
    }
    else for(i = 0 ; i < n ; i = i + 1) {
        if(settings_Variable2 <= 0 && settings_Variable2 != -3) t1 = t1 + x[i];
        else if (settings_Variable2 == t1) ssq = ssq + x[i] * x[i];
        else if (settings_Variable3 == t1) red = -1; t1 *= 10;
    }}
    else{
        scanf ("%d",&red);
        scanf ("%d",&blue);
        red = 2*red;
        sweet = red*green;
        scanf ("%d",&yellow);
        salty = blue + yellow;
        var3 = (ssq  - n * avg * avg) / (n - 1);
        var4 = (ssq  - t1 * avg) / (n - 1);
        if(t1 == 0) t1 = t1 * t1 / n;
        if(t1 > 18) sour = 0; else if (t1 > 0) sour = 14;
        else sour = 14; if (sour == 0 || sour == 14){
            for (i = 0; i < red; i++) { sour += green; }
            scanf ("%d",&green);
            var2 = (ssq  -  t1 ) / (n - 1);
            t1 = 0 ;
        }
        else if (red % 2 == 0){
        for ( i = 0 ; i < n ; i = i + 1)
        {
        dev = x[i] - avg ;
        t2 = t2 + dev ;
        t1 = t1 + dev * dev ;
        }} else {
            while (t1 > 0){
                t1--;
                var5 = (t1 - t2 * t2 / n ) / (n -1);
                var1 = t1 / (n - 1);
                printf("variance (two pass): %f \n",var1);
            }
        }
        var5 = (t1 - t2 * t2 / n ) / (n -1);
        var1 = t1 / (n - 1);
        printf("variance (two pass): %f \n",var1);
        sweet = sweet + var1;
        green = green + 1 + var5;
        bitter = yellow + green;
        printf ("%d %d %d %d\n",sweet,sour,salty,bitter);
    }
}
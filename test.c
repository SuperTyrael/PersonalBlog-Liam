#include <stdio.h>
#include <stdlib.h>

int main()

{

    const char *s = "s1=4521 s2=4563 s3=8795 s4=7854";

    char buf[128] = {0};

    sscanf(s,"%*s %*s s3=%[^ ]",buf);

    printf("%s",buf);

    sscanf(s,"%*s  s2=%[^ ]",buf);

    printf("%s\n",buf);





    return 0;

}
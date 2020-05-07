#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLENS 150 

//void readData(void)
void linkExtraction(){
    char fileName[]="Final_Map.map";
    int n=MAXLENS;
    char buffer[MAXLENS];

    FILE *fp =fopen(fileName, "r");
    if (fp==NULL){
        printf("Error: Can not open the data document！");
        exit(1);
    }

    FILE *nodep=fopen("node.out", "w");
    FILE *linkp=fopen("link.out", "w");
    char slicedString[20] = {0};
    fgets(buffer, n, fp); //jump the first line
    while (!feof(fp) && !ferror(fp)){
        fgets(buffer, n, fp);
        if (buffer[1]=='l'){
            sscanf(buffer,"%*s id=%[^ ]",slicedString);
            fprintf(linkp, "%s ", slicedString);
            
            sscanf(buffer,"%*s%*s node=%[^ ]",slicedString);
            fprintf(linkp, "%s ", slicedString);
            
            sscanf(buffer,"%*s%*s%*s node=%[^ ]",slicedString);
            fprintf(linkp, "%s ", slicedString);
            
            sscanf(buffer,"%*s%*s%*s%*s%*s length=%[^ ]",slicedString);
            fprintf(linkp, "%s ", slicedString);
            
            sscanf(buffer,"%*s%*s%*s%*s%*s%*s veg=%[^ ]",slicedString);
            fprintf(linkp, "%s ", slicedString);
            
            sscanf(buffer,"%*s%*s%*s%*s%*s%*s%*s arch=%[^ ]",slicedString);
            fprintf(linkp, "%s\n", slicedString);
        }
    }
    fclose(fp);
    fclose(linkp);
    return;
    }

void nodeExtraction(){
    char fileName[]="Final_Map.map";
    int n=MAXLENS;
    char buffer[MAXLENS];

    FILE *fp =fopen(fileName, "r");
    if (fp==NULL){
        printf("Error: Can not open the data document！");
        exit(1);
    }

    FILE *nodep=fopen("node.out", "w");
    char slicedString[20] = {0};
    fgets(buffer, n, fp); //jump the first line
    while (!feof(fp) && !ferror(fp)){
        fgets(buffer, n, fp);
        if (buffer[1]=='l'){
            sscanf(buffer,"%*s id=%[^ ]",slicedString);
            fprintf(nodep, "%s ", slicedString);

            sscanf(buffer,"%*s%*s lat=%[^ ]",slicedString);
            fprintf(nodep, "%s ", slicedString);
            
            sscanf(buffer,"%*s%*s%*s lon=%[^ ]",slicedString);
            fprintf(nodep, "%s\n", slicedString);
        }
    }
    fclose(fp);
    fclose(nodep);
    return;
    }
    
    int main(int argc, char const *argv[])
    {
        linkExtraction();
        nodeExtraction();
        return 0;
    }
    

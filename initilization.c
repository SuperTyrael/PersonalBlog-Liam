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
    char slicedString[20];
    fgets(buffer, n, fp); //jump the first line
    while (!feof(fp) && !ferror(fp)){
        fgets(buffer, n, fp);
        if (buffer[1]=='l'){
            /*sscanf(buffer,"%*s id=%[^ ]",slicedString);
            fprintf(linkp, "%s ", slicedString);
            */ //id of link
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
    char slicedString[20];
    fgets(buffer, n, fp); //jump the first line
    while (!feof(fp) && !ferror(fp)){
        fgets(buffer, n, fp);
        if (buffer[1]=='n'){
            sscanf(buffer,"%*s id=%[^ ]",slicedString);
            fprintf(nodep, "%s ", slicedString);

            sscanf(buffer, "%*s%*s%*s lon=%[^ ]",slicedString);
            fprintf(nodep, "%s ", slicedString);

            sscanf(buffer, "%*s%*s lat=%[^ ]", slicedString);
            fprintf(nodep, "%s\n", slicedString);
        }
    }
    fclose(fp);
    fclose(nodep);
    return;
    }
    

void dataConcat(){
    FILE *linkp=fopen("link.out", "r");
    if (linkp==NULL ){
            printf("Error: Can not open the link data and node data document！");
            exit(1);
        }
    
    int n=MAXLENS;
    char bufferLink[MAXLENS];
    char targetString[20];
    char targetString1[20];
    char bufferNode[MAXLENS];
    char targetString2[20];
    FILE *data=fopen("finalData.out", "w");
    while (!feof(linkp) && !ferror(linkp)){
        fgets(bufferLink, n, linkp);
        sscanf(bufferLink, "%s", targetString);
        sscanf(bufferLink, "%*s %s", targetString1);
        FILE *nodep=fopen("node.out", "r");
        while (!feof(nodep) && !ferror(nodep)){
            fgets(bufferNode, n, nodep);
            sscanf(bufferNode, "%s", targetString2);
            if (strcmp(targetString, targetString2)==0 || strcmp(targetString1, targetString2)==0){
                char *s=strstr(bufferNode, " ");
                fprintf(data, "%s", s+1);
            }
        }
        fprintf(data, "\n");
        fclose(nodep);
    }
    fclose(linkp);
}


int main() {
    linkExtraction();
    nodeExtraction();
    dataConcat();
    return 0;
}

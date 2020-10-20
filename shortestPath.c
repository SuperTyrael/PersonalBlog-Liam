#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AdjacentList.h"
#include "createGraph.h"

#define INFI 999999

int chose(int *s, double *d, int n){
    int i, minpos, min;
    min=INFI;
    minpos=-1;
    for (i=0;i<n;i++){
        if (d[i]<min && !s[i]){
            min=d[i];
            minpos=i;
        }
    }
    return minpos;
}

void shortestPath(AdjacentList *G, int v, double *d, int *path){
    int i,j,k,w;
    Edge *p;
    p=G->adjList[v].firstEdge;
    int *s;
    if (v<0 || v>G->numVertices-1){
        return;
    }
    s=(int*)malloc(sizeof(int)*G->numVertices);
    //initilization
    for (i=0;i<G->numVertices;i++){
        s[i]=0; //whether the point is visited
        path[i]=-1; //record the point
        d[i]=INFI; //the distance between v and i;
    }
    //访问起始点的邻接点
    while(p!=NULL){       //traverse all the adjacent point around p
        d[p->adjVex]=p->weight;
        if (p->adjVex!=v && d[p->adjVex]<INFI){
            path[p->adjVex]=v;
        }
        p=p->next;
    }
    s[v]=1;
    d[v]=0;
    
    for (i=1;i<G->numVertices;i++)
    {
        k=chose(s,d, G->numVertices);
        if (k==-1) continue;
        s[k]=1; //该点已被访问
        p=G->adjList[k].firstEdge;
        if (p==NULL) continue;
        while (p!=NULL)
        {
            if (!s[p->adjVex] && d[k]+p->weight < d[p->adjVex]){
                d[p->adjVex]=d[k]+p->weight;
                path[p->adjVex]=k;
            }
            p=p->next;
        }
    }
    return;
}

void output(AdjacentList *G){
    int start, end;
    FILE *p=fopen("route.out", "w");
    printf("input the start\n");
    scanf("%d",&start);
    printf("input the end\n");
    scanf("%d",&end);
    double d[G->numVertices];
    int path[G->numVertices];
    shortestPath(G,start,d, path);
    printf("path: ");
    if (path[end]==-1){
        printf("no path\n");
        return;
    }
    while (path[end]!=-1)
    {
        fprintf(p, "%f %f\n", G->adjList[end].coordinates[0], G->adjList[end].coordinates[1]);
        end=path[end];
    }
    fprintf(p, "%f %f",G->adjList[start].coordinates[0], G->adjList[start].coordinates[1]);
    return;
}

int main(){
    AdjacentList *G=crateAdjacentList();
    output(G);
    return 0;
}
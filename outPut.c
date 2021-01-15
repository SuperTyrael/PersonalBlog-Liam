#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AdjacentList.h"
#include "createAdjList.h"
#include "shortestPath.h"
#include "initilization.h"

void output(AdjacentList *G, int start, int end)
{
    double distance=0.0;
    FILE *p = fopen("route.out", "w");
    double d[G->numVertices];
    int path[G->numVertices];
    shortestPath(G, start, d, path);
    distance=d[end];
    printf("path: ");
    if (path[end] == -1)
    {
        printf("no path\n");
        return;
    }
    while (path[end] != -1)
    {
        fprintf(p, "%f %f\n", G->adjList[end].coordinates[0], G->adjList[end].coordinates[1]);
        printf("%d<-", G->adjList[end].vertexId);
        end = path[end];
    }
    printf("START PROGRAMME\n\n");
    printf("The shortest distance is %f", distance);
    fprintf(p, "%f %f", G->adjList[start].coordinates[0], G->adjList[start].coordinates[1]);
    fclose(p);
    return;
}


void isolatedNode(AdjacentList *G){
    Edge *p;
    FILE *fp = fopen("isolateNode.out", "w");
    for (int i = 0; i < G->numVertices; i++)
    {
        p = G->adjList[i].firstEdge;
        if (p == NULL)
        {
            fprintf(fp, "%f %f\n", G->adjList[i].coordinates[0], G->adjList[i].coordinates[1]);
        }
    }
    fclose(fp);
    free(p);
}

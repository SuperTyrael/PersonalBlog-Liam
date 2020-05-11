#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "initilization.h"
#include "AdjacentList.h"

int vertexLocation(AdjacentList *G, int vertexId){ //find the position in adjlist[] by using it's vertexID
    for (int i=0;i<G->numVertices;i++){
        if (vertexId==G->adjList[i].vertexId) return i;
    }
    printf("ERROR");
    exit(-1);
}


AdjacentList *crateAdjacentList(){
    AdjacentList *graph = (AdjacentList *)malloc(sizeof(AdjacentList));
    FILE *nodep=fopen("node.out", "r");
    FILE *linkp=fopen("link.out", "r");
    char buffer[MAXLENS];
    char targetString[20];
    int num=MAXLENS;
    int i=0, n=0;
    while (!feof(nodep) && !ferror(nodep)){ //creat vertice list
        fgets(buffer, num, nodep);
        if (strcmp(buffer,"\n")==0) break;
        sscanf(buffer,"%s",targetString);
        graph->adjList[i].vertexId= atoi(targetString);
        sscanf(buffer,"%*s %s", targetString);
        graph->adjList[i].coordinates[0]=atof(targetString);
        sscanf(buffer,"%*s%*s %s",targetString);
        graph->adjList[i].coordinates[1]=atof(targetString);
        graph->adjList[i].firstEdge=NULL;
        i++;
    }
    graph->numVertices=i;
    int tmp=0;
    while (!feof(linkp) && !ferror(linkp)){//create edge list
        fgets(buffer, num, linkp);
        if (strcmp(buffer,"\n")==0) break;
        sscanf(buffer, "%s", targetString);
        int i =vertexLocation(graph, atoi(targetString));//location of the first node
        sscanf(buffer, "%*s %s",targetString);
        int j =vertexLocation (graph, atoi(targetString));//location of the second node
        sscanf(buffer, "%*s%*s %s", targetString);
        Edge *e;
        e=(Edge*)malloc(sizeof(Edge));
        e->weight=atof(targetString);
        e->adjVex=j;
        e->next=graph->adjList[i].firstEdge;
        graph->adjList[i].firstEdge=e;//头插法
        //symmetrical
        e=(Edge*)malloc(sizeof(Edge));
        e->weight=atof(targetString);
        e->adjVex=i;
        e->next=graph->adjList[j].firstEdge;
        graph->adjList[j].firstEdge=e;//头插法
        tmp++;
    }
    graph->numEdges=tmp;
    return graph;
    //printf("%d", graph->numVertices);
    //printf("%d", graph->numEdges);
    /*Edge *pf;
	for (i=0;i<graph->numVertices;i++)  
    {  
        int tmp2=0;
        pf=graph->adjList[i].firstEdge;
        printf("%d->",vertexLocation(graph,graph->adjList[i].vertexId));
        while(tmp2<4)  
        {   
			if(pf->next==NULL)
            {
                printf("empty");
            	printf("\n");
				break;	
			}
            else
            {
                printf("%d->", pf->adjVex);
                pf=pf->next;
                tmp2++;
            }
        } 
    } */ 
}


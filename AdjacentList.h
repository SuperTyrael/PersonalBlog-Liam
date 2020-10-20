#pragma once
#define MAX 10000

typedef struct Edge //define the link as edge in graph
{
    int adjVex; //position of the endvertex of the edge
    double weight; 
    struct Edge *next;
}Edge;

typedef struct Vertex{  //define the node as vertex in graph
    int vertexId;
    double coordinates[2]; //coordinates of nodes(vertex), (latitude,lontitude)
    Edge *firstEdge; //point to the edge of this vertex
}Vertex, adjList[MAX];  //adjacentlist which contains all (node)vertex

typedef struct {  
    Vertex adjList[MAX];  //initialize the adjacent list
    int numVertices; //total number of nodes
    int numEdges;  //total number of links
}AdjacentList; 



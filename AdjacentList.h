#define MAX 10000

typedef struct Edge //define the link as edge in graph
{
    int adjVex; //endvertex of the edge
    int weight; 
    struct Edge *next;
}Edge;

typedef struct Vertex{  //define the node as vertex in graph
    char coordinates[2]; //coordinates of nodes(vertex)
    Edge *firstEdge; //point to the edge of this vertex
}Vertex, adjList[MAX];  //adjacentlist which contains all (node)vertex

typedef struct {  
    Vertex adjList[MAX];  //initialize the adjacent list
    int numVertices; //total number of nodes
    int numEdges;  //total number of links
}AdjacentList; 



#include "painlessMesh.h"
#include <ESP8266WiFi.h>
#include "config.h"
#define   MESH_PREFIX     "whateverYouLike"
#define   MESH_PASSWORD   "somethingSneaky"
#define   MESH_PORT       5555

void newConnectionCallback(uint32_t nodeId) {
  Serial.printf("--> startHere: New Connection, nodeId = %u\n", nodeId);
}

void changedConnectionCallback() {
  Serial.printf("Changed connections %s\n", mesh.subConnectionJson().c_str());
} 

void receivedCallback( uint32_t from, String msg ) {
  Serial.printf("Received MSG from %u: %s\n", from, msg.c_str());
}

void setup() {
  Serial.begin(115200);
  
  //mesh.setDebugMsgTypes( ERROR | MESH_STATUS | CONNECTION | SYNC | COMMUNICATION | GENERAL | MSG_TYPES | REMOTE ); // all types on
  mesh.setDebugMsgTypes( ERROR | CONNECTION | COMMUNICATION );

  mesh.init( MESH_PREFIX, MESH_PASSWORD, MESH_PORT ); //initialize the mesh
  
  mesh.onNewConnection(&newConnectionCallback); //set callbacks
  mesh.onChangedConnections(&changedConnectionCallback);
  mesh.onReceive(&receivedCallback);

  /*
  for (int i = 0; i<CACHE_SIZE;i++){
    cache[i] = 2; //set to far to begin with
  }*/
}

void loop() {
  mesh.update(); //Mesh bg stuff
}

/*
void cacheSignal(int sig){
  for (int i = 1; i<CACHE_SIZE; i++){
    cache[i-1] = cache[i]; //move the cache down
  }
  cache[CACHE_SIZE-1] = sig; //insert our latest data


  //just to know what's going on
  //Serial.print("[");
  for (int i = 0; i<CACHE_SIZE; i++){
    //Serial.print(" ");
    //Serial.print(cache[i]);
  }
  //Serial.println("]");

  if (samecheck(cache, CACHE_SIZE)==1) return; //Check if our array is all the same
  //Serial.println("CONSISTENT");
}

int samecheck(const int a[], int n) //simple fn to check if array is same
{   
    while(--n>0 && a[n]==a[0]);
    return n!=0;
}*/



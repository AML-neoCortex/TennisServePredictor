// #ifdef ESP32
//   #include <WiFi.h>
// #else
//   #include <ESP8266WiFi.h>
// #endif

// void setup(){
//   Serial.begin(115200);
//   Serial.println();
//   Serial.print("ESP Board MAC Address:  ");
//   Serial.println(WiFi.macAddress());
// }
 
// void loop(){

// }
#include <ESP8266WiFi.h>
#include <espnow.h>

// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
    int id;
    int Xacc ;
    int Yacc ;
    int Zacc ;
    int Xori ;
    int Yori ;
    int Zori ;
    int Xmag ;
    int Ymag ;
    int Zmag ;
    int Xgyro ;
    int Ygyro ;
    int Zgyro ;
    int Xrot ;
    int Yrot ;
    int Zrot ;
    int Xlin ;
    int Ylin ;
    int Zlin ;
    int Xgrav ;
    int Ygrav ;
    int Zgrav ;
} struct_message;

// Create a struct_message called myData
struct_message myData;

// Create a structure to hold the readings from each board
struct_message board1;
struct_message board2;

// Create an array with all the structures
struct_message boardsStruct[2] = {board1, board2};

// Callback function that will be executed when data is received
void OnDataRecv(uint8_t * mac_addr, uint8_t *incomingData, uint8_t len) {
  char macStr[18];
  Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);
  memcpy(&myData, incomingData, sizeof(myData));
  //Serial.printf("Board ID %u: %u bytes\n", myData.id, len);
  //Update the structures with the new incoming data
  boardsStruct[myData.id-1].Xacc = myData.Xacc;
  Serial.printf("Xacc value: %d \n", boardsStruct[myData.id-1].Xacc);
  Serial.println();
    boardsStruct[myData.id-1].Yacc = myData.Yacc;
  Serial.printf("Yacc value: %d \n", boardsStruct[myData.id-1].Yacc);
  Serial.println();
    boardsStruct[myData.id-1].Zacc = myData.Zacc;
  Serial.printf("Zacc value: %d \n", boardsStruct[myData.id-1].Zacc);
  Serial.println();
  //   boardsStruct[myData.id-1].Xori = myData.Xori;
  // Serial.printf("Xori value: %d \n", boardsStruct[myData.Xori-1].Xori);
  // Serial.println();
  //   boardsStruct[myData.id-1].Yori = myData.Yori;
  // Serial.printf("Yori value: %d \n", boardsStruct[myData.id-1].Yori);
  // Serial.println();
  //   boardsStruct[myData.id-1].Zori = myData.Zori;
  // Serial.printf("Zori value: %d \n", boardsStruct[myData.id-1].Zori);
  // Serial.println();
  //   boardsStruct[myData.id-1].Xmag = myData.Xmag;
  // Serial.printf("Xmag value: %d \n", boardsStruct[myData.id-1].Xmag);
  // Serial.println();
  //     boardsStruct[myData.id-1].Ymag = myData.Ymag;
  // Serial.printf("Ymag value: %d \n", boardsStruct[myData.id-1].Ymag);
  // Serial.println();
  //     boardsStruct[myData.id-1].Zmag = myData.Zmag;
  // Serial.printf("Zmag value: %d \n", boardsStruct[myData.id-1].Zmag);
  // Serial.println();
  //     boardsStruct[myData.id-1].Xgyro = myData.Xgyro;
  // Serial.printf("Xgyro value: %d \n", boardsStruct[myData.id-1].Xgyro);
  // Serial.println();
  //     boardsStruct[myData.id-1].Ygyro = myData.Ygyro;
  // Serial.printf("Ygyro value: %d \n", boardsStruct[myData.id-1].Ygyro);
  // Serial.println();
  //     boardsStruct[myData.id-1].Zgyro = myData.Zgyro;
  // Serial.printf("Zgyro value: %d \n", boardsStruct[myData.id-1].Zgyro);
  // Serial.println();
  //     boardsStruct[myData.id-1].Xrot = myData.Xrot;
  // Serial.printf("Xrot value: %d \n", boardsStruct[myData.id-1].Xrot);
  // Serial.println();
  //     boardsStruct[myData.id-1].Yrot = myData.Yrot;
  // Serial.printf("Yrot value: %d \n", boardsStruct[myData.id-1].Yrot);
  // Serial.println();
  //     boardsStruct[myData.id-1].Zrot = myData.Zrot;
  // Serial.printf("Zrot value: %d \n", boardsStruct[myData.id-1].Zrot);
  // Serial.println();
  //     boardsStruct[myData.id-1].Xlin = myData.Xlin;
  // Serial.printf("Xlin value: %d \n", boardsStruct[myData.id-1].Xlin);
  // Serial.println();
  //     boardsStruct[myData.id-1].Ylin = myData.Ylin;
  // Serial.printf("Ylin value: %d \n", boardsStruct[myData.id-1].Ylin);
  // Serial.println();
  //     boardsStruct[myData.id-1].Zlin = myData.Zlin;
  // Serial.printf("Zlin value: %d \n", boardsStruct[myData.id-1].Zlin);
  // Serial.println();
  //     boardsStruct[myData.id-1].Xgrav = myData.Xgrav;
  // Serial.printf("Xgrav value: %d \n", boardsStruct[myData.id-1].Xgrav);
  // Serial.println();
  //     boardsStruct[myData.id-1].Ygrav = myData.Ygrav;
  // Serial.printf("Ygrav value: %d \n", boardsStruct[myData.id-1].Ygrav);
  // Serial.println();
  //     boardsStruct[myData.id-1].Zgrav = myData.Zgrav;
  // Serial.printf("Zgrav value: %d \n", boardsStruct[myData.id-1].Zgrav);
  // Serial.println();
}
 



void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(OnDataRecv);
}

void loop(){
  // Keep this loop empty
}
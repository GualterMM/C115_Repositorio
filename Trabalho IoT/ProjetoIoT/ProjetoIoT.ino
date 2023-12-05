#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Dados Wi-fi
const char* ssid = "WLL-Inatel";
const char* password = "inatelsemfio*";

// Dados MQTT
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient client(espClient);

// Dados sobre sensor e LEDs
const int trigPinSpecial = 15; // D8
const int echoPinSpecial = 13; // D7
const int trigPinRegular = 12; // D6
const int echoPinRegular = 14; // D5
int duration[2] = {0, 0};
int distance[2] = {0, 0};

// Array RGB de pinos
int specialPins[3] = {2, 0, 4}; // D4, D3, D2
int regularPins[2] = {5, 16}; // D1, D0

// Dado de temporarização para publicar dados no MQTT
unsigned long previousMillis = 0;

// Criando controle de vaga.
// [0] -> Vaga especial, [1] -> Vaga regular
// -1  =  ocupado            ->  vermelho
//  0  =  reservado          ->  amarelo
//  1  =  livre              ->  verde
//  2  =  livre (especial)   ->  azul
int8_t vagaStatus[2] = {1, 1};

// Variáveis de controle para vaga especial e reserva de vaga
bool especial = false;
bool reservada = false;

void setup() {
  Serial.begin(115200);

  // Inicializando LEDs, sensor e botão
  pinMode(echoPinSpecial, INPUT);
  pinMode(echoPinRegular, INPUT);
  pinMode(trigPinSpecial, OUTPUT);
  pinMode(trigPinRegular, OUTPUT);
  pinMode(specialPins[0], OUTPUT);
  pinMode(specialPins[1], OUTPUT);
  pinMode(specialPins[2], OUTPUT);
  pinMode(regularPins[0], OUTPUT);
  pinMode(regularPins[1], OUTPUT);

  // Conectando com Wi-Fi
  setup_wifi();

  // Conectando com MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Caso a conexão seja bem sucedida, fazer inscrição pro tópico de vagas
  if(client.connect("C115-Teste")) {
    Serial.println(("Conectado ao MQTT"));
    client.subscribe("c115/estacionamento/reservas/vaga1");
  } else {
    Serial.println("Falha na conexão.");
    Serial.println(client.state());
  }
  
}

void loop() {
  // Variável para temporarização de funções
  unsigned long currentMillis = millis();

  // Inicia loop do MQTT
  client.loop();

  // Limpa os sensores ultrasônicos
  digitalWrite(trigPinSpecial, LOW);
  digitalWrite(trigPinRegular, LOW);
  delayMicroseconds(2);

  // Manda um pulso pelos sensores
  digitalWrite(trigPinSpecial, HIGH);
  digitalWrite(trigPinRegular, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinSpecial, LOW);
  digitalWrite(trigPinRegular, LOW);

  // Pega a duração dos pulsos
  duration[0] = pulseIn(echoPinSpecial, HIGH);
  duration[1] = pulseIn(echoPinRegular, HIGH);

  // Verifica a distância baseada na duração dos pulsos
  distance[0] = duration[0] * 0.034 / 2;
  distance[1] = duration[1] * 0.034 / 2;

  // Atualiza status da vaga e cor do LED
  for(int i = 0; i < 2; i++) {
    if(distance[i] <= 50) { // Se o carro estiver na vaga, ela está OCUPADA
      vagaStatus[i] = -1;
    } else if(especial == 0 && reservada == 0) { // Se a vaga estiver disponível e não for especial, ela está LIVRE
      vagaStatus[i] = 1;
    } else if (especial == 1 && reservada == 0) { // Se a vaga estiver disponível e for especial, ela está LIVRE (ESPECIAL)
      vagaStatus[i] = 2;
    } else { // Caso contrário, ela está RESERVADA
      vagaStatus[i] = 0;
    }

    // Muda a cor dos LEDs respectivos
    switch(vagaStatus[i]) {
      default:
      case -1:
        setColor("RED", i == 0 ? specialPins : regularPins, i == 0 ? 3 : 2);
      break;

      case 0:
        setColor("YELLOW", i == 0 ? specialPins : regularPins, i == 0 ? 3 : 2);
      break;

      case 1:
        setColor("GREEN", i == 0 ? specialPins : regularPins, i == 0 ? 3 : 2);
      break;

      case 2:
        setColor("BLUE", specialPins, 3);
      break;
    }
  }

  // Envia dados aos tópicos MQTT a cada 2 segundos, para evitar sobrecarga
  if (currentMillis - previousMillis >= 2000) {
    previousMillis = currentMillis;

    client.publish("c115/estacionamento/sensores/sensor1", String(vagaStatus[0]).c_str());
    client.publish("c115/estacionamento/sensores/sensor2", String(vagaStatus[1]).c_str());
    client.publish("c115/estacionamento/vagas/vaga1", String(vagaStatus[0]).c_str());

    Serial.print("Publicado valor ");
    Serial.print(vagaStatus[0]);
    Serial.println(" para c115/estacionamento/sensor1.");
    Serial.print("Publicado valor ");
    Serial.print(vagaStatus[1]);
    Serial.println(" para c115/estacionamento/sensor2.");
  }
}

// Conecta o ESP8266 ao Wi-Fi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando-se a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

// Função de callback para lidar com mensagens recebidas pela inscrição de tópicos MQTT
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida no tópico: ");
  Serial.println(topic);

  // Converte o payload para um int e verifica se a vaga foi reservada
  int receivedValue = atoi((char*)payload);
  if (receivedValue == 1) {
    reservada = true;
  } else{
    reservada = false;
  }
}

// Altera a cor de um LED RGB de 3 ou 4 pinos.
// O pinos do array 'pins' devem ser inseridos em ordem
void setColor(String color, int pins[], int arraySize) {
  color.toUpperCase();

  if(arraySize >= 2) {
    if (color == "RED") {
      analogWrite(pins[0], 255);
      analogWrite(pins[1], 0);
      if (arraySize == 3) analogWrite(pins[2], 0);
    } else if (color == "BLUE") {
      analogWrite(pins[0], 0);
      analogWrite(pins[1], 0);
      if (arraySize == 3) analogWrite(pins[2], 255);
    } else if (color == "YELLOW") {
      analogWrite(pins[0], 255);
      analogWrite(pins[1], 255);
      if (arraySize == 3) analogWrite(pins[2], 0);
    } else if (color == "GREEN") {
      analogWrite(pins[0], 0);
      analogWrite(pins[1], 255);
      if (arraySize == 3) analogWrite(pins[2], 0);
    } else {
      analogWrite(pins[0], 255);
      analogWrite(pins[1], 0);
      if (arraySize == 3) analogWrite(pins[2], 0);
    }

  }
}
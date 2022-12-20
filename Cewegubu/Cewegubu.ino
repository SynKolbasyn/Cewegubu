#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "";
const char* password = "";
const char* mqtt_server = "";
const char* mqtt_name = "";
const char* mqtt_pass = "";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];

char* playerGameData;
unsigned int numOfPlayers;
String topicForPlayer = "/user/synkolbasyn/forPlayer";

struct MyStruct {
  String email;
  String password;
  String nickName;
  int money;
  int id;
};

MyStruct x;

class Player {
  public:
    String getEmail();
    String getPassword();
    String getNickName();
    int getMoneyValue();
    int getId();
    String getPrivateTopic();
    Player();
    Player(String email, String password, String nickName, int money, int id);

  private:
    String _email;
    String _password;
    String _nickName;
    int _money;
    int _id;
    String _privateTopic;
};

Player::Player() {}

Player::Player(String email, String password, String nickName, int money, int id) {
  _email = email;
  _password = password;
  _nickName = nickName;
  _money = money;
  _id = id;
  _privateTopic = topicForPlayer + String(id);
}

String Player::getEmail() {
  return _email;
}

String Player::getPassword() {
  return _password;
}

String Player::getNickName() {
  return _nickName;
}

int Player::getMoneyValue() {
  return _money;
}

int Player::getId() {
  return _id;
}
String Player::getPrivateTopic() {
  return _privateTopic;
}

Player playersList[100];

void saveToPlayersList(Player playerData) {
  playersList[numOfPlayers] = playerData;
  numOfPlayers = numOfPlayers + 1;
}

void setup_wifi() {
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  String text;
  for (int i = 0; i < length; i++) {
    text += (char)message[i];
  }
  Serial.println(text);
  playerGameData = (char*) text.c_str();

  char jsonPlayerData[text.length()] = {""};
  for (int i; i < text.length(); i++) {
    jsonPlayerData[i] = text[i];
  }
  DynamicJsonDocument playerData(1024);
  DeserializationError error = deserializeJson(playerData, jsonPlayerData);
  Serial.println();
  if (error) {
    Serial.println("ERROR");
    return;
  }
  // if (!playerData.isNull()) {
  //   x.email = playerData["email"];
  //   x.password = playerData["password"];
  //   x.nickName = playerData["nickName"];
  //   x.money = playerData["money"];
  //   x.id = playerData["id"];
  // }
  // Player playerDataClass = Player(x.email, x.password, x.nickName, x.money, x.id);
  String email = "";
  String password = "";
  String nickName = "";
  int money = 0;
  int id = 0;
  // if (!playerData.isNull()) {
  //   email = playerData["email"];
  //   password = playerData["password"];
  //   nickName = playerData["nickName"];
  //   money = playerData["money"];
  //   id = playerData["id"];
  // }
  Player playerDataClass = Player(String(email), String(password), String(nickName), (int)money, (int)id);
  String cmd = playerData["command"];
  Serial.println(cmd);
  // if (commands(cmd, playerDataClass)) {
  //   client.publish(playerDataClass.getPrivateTopic(), String(commands(cmd, playerDataClass)));
  //   Serial.println();
  // }
  // else {
  //   Serial.println();
  // }
  client.publish(playerDataClass.getPrivateTopic().c_str(), String(commands(cmd, playerDataClass)).c_str());
  Serial.println(String(commands(cmd, playerDataClass)));
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client", mqtt_name, mqtt_pass)) {
      Serial.println("connected");
      client.subscribe("/user/synkolbasyn/forServer");
    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
    }
  }
}

bool commands(String command, Player playerData) {
  if (command == "register") {
    return reg(playerData);
  }
  if (command == "login") {
    return login(playerData);
  }
}

bool reg(Player player) {
  for (int i; i < numOfPlayers; i++) {
    if (player.getEmail() == playersList[i].getEmail()) {
      return 0;
    }
    if (player.getNickName() == playersList[i].getNickName()) {
      return 0;
    }
  }
  saveToPlayersList(player);
  return 1;
}

bool login(Player player) {
  for (int i; i < numOfPlayers; i++) {
    if (player.getEmail() != playersList[i].getEmail()) {
      continue;
    }
    if (player.getPassword() != playersList[i].getPassword()) {
      return 0;
    }
  }
  return 1;
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  char jsonGameData[] = "{\"player\":[{\"email\":\"umirotvorenie.bot@yandex.ru\",\"password\":\"12344321\",\"nickName\":\"Umirotvorenie\",\"money\":10}],\"players\":1}";
  DynamicJsonDocument gameData(16384);
  DeserializationError error = deserializeJson(gameData, jsonGameData);
  if (error) {
    Serial.println("ERROR");
  }
  else {
    int num = gameData["players"];
    Serial.println(String(num));
  }
  x.email = "umirotvorenie.bot@yandex.ru";
  x.password = "12344321";
  x.nickName = "Umirotvorenie";
  x.money = 10;
  x.id = 0;
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 1000) {
    lastMsg = now;
    client.publish("/user/synkolbasyn/gamedata", playerGameData);
  }
}

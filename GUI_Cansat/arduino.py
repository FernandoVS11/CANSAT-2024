float lectura;
float voltaje;

void setup() {
  
  Serial.begin(9600);
  pinMode(A0,INPUT);
}

void loop() {
  lectura = analogRead(A0);
  voltaje = ((lectura/1023)*5.5);
  
  for (int i = 0; i < 10; i++) {
    Serial.print(voltaje);
    if(i != 9){
      Serial.print(",");
    }
  }

  
  Serial.println("");

  delay(200);
}

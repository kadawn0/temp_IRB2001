/*
 * -----------------------------
 * IRB2001 -2017-1
 * Modulo: Control de Sistemas Roboticos
 * -----------------------------
 * Programa Base Tarea del Modulo
 * -----------------------------
 */

//-----------------------------------
// IMPORTAR librearias
#include "DualVNH5019MotorShield.h"
DualVNH5019MotorShield md;

// Definición de PINs
#define encoder0PinA  19
#define encoder0PinB  18
#define encoder1PinA  20
#define encoder1PinB  21

// Variables Tiempo
unsigned long time_ant = 0;
const int Period = 10000;   // 10 ms = 100Hz
float escalon = 0;
const float dt = Period *0.000001f;
float motorout    = 0.0;

// Variables de los Encoders y posicion
volatile long encoder0Pos = 0;
volatile long encoder1Pos = 0;
long newposition0;
long oldposition0 = 0;
long newposition1;
long oldposition1 = 0;
unsigned long newtime;
float vel0;
float vel1;
volatile float pos_prom = 0;
float ref_pos = 4250.0;
float k_p = 0.3; // 0.875 ----- 0.675                         0.65
float k_i = 0.008; //0.0008 ---- 2.6318485 ----- 2.49        0.0009
float k_d = 0.026; //0.028 ---- 0.095108 ----- 0.095            0.03
float integral = 0.0;
volatile float error = 0.0;
volatile float error_old = 0.0;
float derivada = 0;
float contador = 0;


//-----------------------------------
// CONFIGURACION
void setup()
{
	// Configurar MotorShield
	md.init();
	
	// Configurar Encoders
	pinMode(encoder0PinA, INPUT);
	digitalWrite(encoder0PinA, HIGH);       // Incluir una resistencia de pullup en la entrada
	pinMode(encoder0PinB, INPUT);
	digitalWrite(encoder0PinB, HIGH);       // Incluir una resistencia de pullup en la entrada
	pinMode(encoder1PinA, INPUT);
	digitalWrite(encoder1PinA, HIGH);       // Incluir una resistencia de pullup en la entrada
	pinMode(encoder1PinB, INPUT);
	digitalWrite(encoder1PinB, HIGH);       // Incluir una resistencia de pullup en la entrada
	attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoder0A, CHANGE);  // encoder 0 PIN A
	attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoder0B, CHANGE);  // encoder 0 PIN B
	attachInterrupt(digitalPinToInterrupt(encoder1PinA), doEncoder1A, CHANGE);  // encoder 1 PIN A
	attachInterrupt(digitalPinToInterrupt(encoder1PinB), doEncoder1B, CHANGE);  // encoder 1 PIN B
	
	
	// Configurar Serial port
	Serial.begin(115200);           //Inicializar el puerto serial (Monitor Serial)
	Serial.println("start");
}

//-----------------------------------
// CONFIGURANDO INTERRUPCIONES
void doEncoder0A()
{
	if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) {
		encoder0Pos++;
	} else {
		encoder0Pos--;
	}
}

void doEncoder0B()
{
	if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) {
		encoder0Pos--;
	} else {
		encoder0Pos++;
	}
}

void doEncoder1A()
{
	if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
		encoder1Pos++;
	} else {
		encoder1Pos--;
	}
}

void doEncoder1B()
{
	if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
		encoder1Pos--;
	} else {
		encoder1Pos++;
	}
}


//-----------------------------------
// LOOP PRINCIPAL
void loop() {
	if ((micros() - time_ant) >= Period)
	{
		newtime = micros();
		
		//-----------------------------------
		// Ejemplo variable alterando cada 10 segundos
		if ((newtime / 5000000) % 2)
			ref_pos = 4250 ;
		else
			ref_pos = 0;
		
		
		//-----------------------------------
		// Actualizando Informacion de los encoders
		newposition0 = encoder0Pos;
		newposition1 = encoder1Pos;
		
		//-----------------------------------
		// Calculando Velocidad del motor
		float rpm = 31250;
		vel0 = (float)(newposition0 - oldposition0) * rpm / (newtime - time_ant); //RPM
		vel1 = (float)(newposition1 - oldposition1) * rpm / (newtime - time_ant); //RPM
		oldposition0 = newposition0;
		oldposition1 = newposition1;
		
		//-----------------------------------
		// Salida al Motor
		pos_prom = (newposition0 - newposition1)/2;
		error = ref_pos - pos_prom;
		integral += error*dt;
		derivada = (error - error_old)/dt;
		motorout = k_p*error + k_i*integral + k_d*derivada;
		error_old = error;   
		
		
		// Motor Voltage
		md.setM1Speed(motorout);
		md.setM2Speed(-motorout);
		
		
		
		//
		
		// Reportar datos
		
		//    Serial.print(",");
		//    Serial.print(newposition1);
		//    Serial.print(",");
		//    Serial.print(ref);
		//    Serial.print(",");
		//    Serial.print(vel0);
		//    Serial.print(",");
		//    Serial.print(vel1);
		//    Serial.print(", ");
		//    Serial.print(" Motor Out 0: ");
		//    Serial.print(motorout);
		//    Serial.print(", ");
		//    Serial.print(" Motor Out 1: ");
		//    Serial.println(motorout);
		//Serial.print(vel0);
		//Serial.print(", ");
		//Serial.print(ref);
		//Serial.print(", ");
		//Serial.println(newtime);
		//Serial.print("$,");
		//Serial.print(newtime);
		//Serial.print(",");
		Serial.println(pos_prom);
		time_ant = newtime;
	}
	
}


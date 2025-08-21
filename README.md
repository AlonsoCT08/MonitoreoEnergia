# MonitoreoEnergia

Este proyecto permite monitorear el consumo de energía de dispositivos mediante un microcontrolador y visualizar los datos en una interfaz gráfica.

## Estructura del proyecto

- **QTCreator/**  
  Contiene los scripts de la interfaz gráfica desarrollada en Qt Creator. Esta interfaz recibe los datos del microcontrolador a través del puerto serial y muestra gráficos de energía acumulada y carga.

- **MicroPython/**  
  Contiene los scripts para el microcontrolador (ESP32) que se encargan de leer las señales de voltaje y corriente, calcular energía y carga, y enviar los datos a la interfaz.

## Descripción general

El sistema consiste en:
1. **Microcontrolador:** Captura datos de energía mediante sensores o circuitos de medición.  
2. **Interfaz Qt:** Recibe los datos por UART/USB, los guarda en archivos CSV y los visualiza en tiempo real.  

## Requisitos

- Python 3.x  
- Pqt para la interfaz gráfica  
- MicroPython en el ESP32  
- Librerías de comunicación serial (`pyserial`)  

## Uso

1. Cargar los scripts de MicroPython al ESP32.  
2. Abrir la interfaz en Qt Creator y configurar el puerto COM correspondiente.  
3. Visualizar los datos en tiempo real y almacenarlos automáticamente en CSV.  


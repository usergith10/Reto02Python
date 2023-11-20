# Reto02Python
Este es el ejercicio correspondiente al reto 02 en python
Consolidador de Boletas y Generador de PDF
Este script de Python está diseñado para consolidar la información de boletas de pago almacenadas en archivos de texto, crear un DataFrame con la información y luego generar un archivo PDF consolidado. También incluye una función para enviar el PDF por correo electrónico Gmail.

Requisitos o Consideraciones

- Python 3
- Librerías a importar de Python: 
1 pandas "pip install pandas"
2 fpdf "pip install fpdf"
3 dotenv "pip install python-dotenv"
4 cryptography "pip install cryptography"
- Depositar los archivos de textos en la carpeta del archivo python
- Depositar el archivo "secretprd.key" en la carpeta del archivo python
- Depositar el archivo ".env.prod" dentro de la carpeta "RutaDelArchivoPython/Environment"

Uso
Coloca los archivos de boletas en el mismo directorio que este script.

Ejecuta el script utilizando Python 3:

En cmd
python GeneratePdfSendMail.py
El script procesará los archivos, creará un archivo PDF consolidado llamado consolidado.pdf y lo enviará por correo electrónico.

Configuración de Correo Electrónico Gmail
Antes de ejecutar el script, asegúrate de configurar la información de correo electrónico en el código fuente:

En python

Ajusta las siguientes variables:
smtp_port = 587                  (Puerto SMTP)
smtp_server = "smtp.gmail.com"  (Servidor Google SMTP)
email_from: Dirección de correo electrónico remitente.
email_to: La dirección de correo electrónico de los destinatarios (["correo1@com,Correo2@net,etc"]). 
subject = Asunto del correo.
pswd: La contraseña de tu dirección de correo electrónico (Recuerda que antes se tiene que configurar Gmail, "Crear y utilizar contraseñas de aplicación").

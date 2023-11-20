import pandas as pd # Instalar la biblioteca pandas: pip install pandas
from fpdf import FPDF  # Instalar la biblioteca fpdf: pip install fpdf
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Para funcionalidad de desencrytar
from io import open
import os
from dotenv import load_dotenv # Instalar la biblioteca fpdf: pip install python-dotenv
from cryptography.fernet import Fernet # Instalar la biblioteca cryptography: pip install cryptography

# Función para enviar correo a multiples destinatarios y con el adjunto
def send_emails(email_list):

    for person in email_list:

        # Cuerpo del correo
        body = f"""
        Estimados, Se envía el consolidado de las boletas para su revisión.
        
        Bot Python
        """

        # Definiendo las parte del correo
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Asignando el texto que va el body del correo
        msg.attach(MIMEText(body, 'plain'))

        # Asignando el archivo que sera el adjunto del correo
        filename = "consolidado.pdf"

        # Abriendo el archivo adjunto como binario
        attachment= open(filename, 'rb')  # r de read and b de binary

        # Codificar a base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Casteando a string
        text = msg.as_string()

        # Conectando con el servidor
        print("Conectando con el servidor...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Conectado exitosamente al server de correo")   

        # Enviando el correo al destinatario
        print(f"Enviando correo a: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Correo enviado a: {person}")      

    # Cerramos el puerto
    TIE_server.quit()

# Funcion para extraer información de los archivos de textos 
def extract_information(file_content):
    # Expresión regular para realizar la busqueda 
    pattern = re.compile(r"Nombres y Apellidos: (.+?)\nCargo: (.+?)\nSueldo: (.+?)\nMes: (.+?)\nDías Trabajados: (\d+)", re.UNICODE)  
    # Buscar coincidencias
    match = pattern.search(file_content)
    # Si existe coincidencia entonces retornar datos  
    if match:
        return {
            "Nombres y Apellidos": match.group(1),
            "Cargo": match.group(2),
            "Sueldo": float(match.group(3).replace('S/ ', '')),  # Convertir a número
            "Mes": match.group(4),
            "Días Trabajados": match.group(5)               
        }
    else:
        return None

# Función para convertir dataframe a pdf
def create_pdf(dataframe, output_path='consolidado.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=6)

    # Títulos de columnas
    for col in dataframe.columns:
        pdf.cell(40, 10, col, 1)
    pdf.ln()

    # Contenido del dataframe
    for _, row in dataframe.iterrows():
        for col in dataframe.columns:
            pdf.cell(40, 10, str(row[col]), 1)
        pdf.ln()

    pdf.output(output_path)

# Función para cargar el archivo key
def load_key():   
    return open("secretprd.key", "rb").read()

# Función para descencriptar mensaje
def decrypt_message(encrypted_message):
    try:
        key = load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
    
        return decrypted_message.decode()
    except Exception as otherExcep:
        print(otherExcep)

# ================== Funcion Main ===============================
if __name__ == "__main__":
    data_list = []

    #Leyendo las variables del archivo de configuración de acuerdo al ambiente
    load_dotenv("./Environment/.env.prod")

    #Obtener variables de configuración
    print(f"Leyendo datos configurados")

    smtp_port=os.getenv("SMTP_PORT")
    smtp_server=os.getenv("SMTP_SERVER")
    email_from=os.getenv("EMAIL_FROM")
    email_to=os.getenv("EMAIL_TO")
    subject=os.getenv("SUBJECT")
    CR_PassTemp=os.getenv("PASSWORD_EMAIL")
    pswd=""      
    print(f"Desencriptado password")
    pswd=decrypt_message(CR_PassTemp.encode())     

    email_list = [email_to] # Lista de correos destinatarios

    # Recorrer los 9 archivos
    for i in range(1, 10):
        file_path = f"Boleta -  ({i}).txt"

        try:
            # Abrimos el archivo y obtenemos su contenido
            with open(file_path, 'r',encoding='utf-8') as file:
                content = file.read()
                info = extract_information(content)

                if info:
                    data_list.append(info)
                else:
                    print(f"No se encontró coincidencias en el archivo {file_path}")

        except FileNotFoundError:
            print(f"El archivo {file_path} no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error al procesar el archivo {file_path}: {e}")

    # Crear un dataframe a partir de la lista de datos
    df = pd.DataFrame(data_list)

    # Crear el PDF consolidado
    create_pdf(df) 
      
   # Ejecutar funcion de enviar correo
    send_emails(email_list)
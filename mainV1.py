import os
import smtplib 
from email.message import EmailMessage
from Crypto.Cipher import AES
import base64

# Comprimir el directorio public_html
os.system("zip backup$(date +%Y%m%d).zip public_html")
os.system("openssl enc -aes-256-cbc -salt -in backup$(date +%Y%m%d).zip -out backup$(date +%Y%m%d).zip")
 
# Conectar al servidor ftp y enviar datos
os.system("lftp 127.0.0.1 -u ftp -e 'put 'backup$(date +%Y%m%d).zip'; quit'")

# Eliminar el archivo local
os.system("rm backup$(date +%Y%m%d).zip")
 
# Desencriptar contraseña
def decrypt_password(key, encrypted_password):
    # Decodificamos la contraseña cifrada en base64
    encrypted_password = base64.b64decode(encrypted_password)

    # Creamos el objeto AES en modo CBC
    cipher = AES.new(key, AES.MODE_CBC, key)

    # Desciframos la contraseña
    password = cipher.decrypt(encrypted_password).rstrip(b'{').decode()

    return password

key = b'Sixteen byte key'
encrypted_password = b'Nj8X0A18iP+kHxiOmOo9ICwmTkmwbllMdDIgdPcl8Xo='

# Desciframos la contraseña
password = decrypt_password(key, encrypted_password)

# Enviar correo
email_subject = "Transferencia FTP" 
sender_email_address = "rramos71@ieszaidinvergeles.org" 
receiver_email_address = "pruebavergeles@gmail.com" 
email_smtp = "smtp.gmail.com" 
email_password = password

# Create an email message object 
message = EmailMessage() 

# Configure email headers 
message['Subject'] = email_subject
message['From'] = sender_email_address 
message['To'] = receiver_email_address 

# Crear el texto del mensaje
message.set_content("Se ha realizado correctamente la subida del archivo al servidor") 

# Establecer conexion y puertos
server = smtplib.SMTP(email_smtp, '587') 

# Identificar el usuario en el servidor
server.ehlo() 

# Asegurar conexion segura
server.starttls() 

# Inicio de sesion en el correo electronico
server.login(sender_email_address, email_password) 

# Envio del correo
server.send_message(message) 

# Cerrar conexion
server.quit() 
 
# TAREA CRONTAB
# 0 3 * * * /usr/bin/python3 /home/rubix712/script/main.py
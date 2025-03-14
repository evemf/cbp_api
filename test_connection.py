import smtplib

EMAIL = "evemolina7@gmail.com"
PASSWORD = "xiuakkrrvzfpjkhk"  # Usa tu contraseña de aplicación

try:
    # Conéctate usando SMTP_SSL en el puerto 465
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, PASSWORD)
    
    # Mensaje
    from_email = EMAIL
    to_email = "evemolina7@gmail.com"  
    subject = "Test Email SMTP 465"
    body = "Este es un correo de prueba usando SMTP en puerto 465."
    
    email_message = f"Subject: {subject}\n\n{body}"
    
    # Envía el correo
    server.sendmail(from_email, to_email, email_message)
    server.quit()

    print("✅ Correo enviado correctamente en puerto 465")
except Exception as e:
    print(f"❌ Error: {e}")

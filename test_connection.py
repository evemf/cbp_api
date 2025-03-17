from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = "$2b$12$wRuaY5sbL6WpUD3MR4p7ievKGpSesG1LsubDCm4SB/f/xNNlmvQiO"  # Hashed password de la BD
input_password = "Neo#2017"  # La contraseña que estás usando para iniciar sesión

if pwd_context.verify(input_password, hashed_password):
    print("✅ Contraseña válida")
else:
    print("❌ Contraseña inválida")

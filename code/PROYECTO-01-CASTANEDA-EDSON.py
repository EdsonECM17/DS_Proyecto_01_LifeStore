from data.lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

# Se agrega lista de usuarios validos para login
admin_users = {'ecastaneda': 'lifestore12345', 'cguillen': 'holamundo'}

# Login de usuario
acesso = False # If true, accede a la información de LifeStore
additional_attempts = 2 # Intentos extra en caso de login fallido
user = input("Ingrese su usuario: ")
password = input("Ingrese su contraseña: ")
while acesso is False and additional_attempts > 0:
     
    # Validar si el usuario existe
    if user in admin_users.keys():
        #  Caso: Usuario/Contraseña validos
        if password == admin_users[user]:
            acesso = True
            print("Bienvenido "+user+".")
    # Caso: usuario o contraseña son invalidos
    if acesso is False:
        additional_attempts-=1
        print("Error con el usuario o contraseña proporcionados. Revise e intente nuevamente.")
        # Reingresar datos para siguiente iteración
        user = input("Ingrese su usuario nuevamente: ")
        password = input("Ingrese su contraseña nuevamente: ")

# Acceso correcto
if acesso:
    print("Acesso a Datos")

# 3 intentos fallidos
else:
    print("Demasiados intentos.\nEl acesso se ha desabilitado para este equipo.\n"+
          "Para poder acceder nuevamente, acercarse con el equipo de TI de Life Store.")

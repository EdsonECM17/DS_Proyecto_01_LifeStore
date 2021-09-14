from os import access
import pandas as pd

# Declaro ruta donde encontrar el archivo con los usuarios permitidos
USER_FILE_PATH = "data/users.csv"

def login(login_attempts:int = 3):
    """Función para iniciar sesion. Mediante funciones input, el usuario escribe su
       usuario y contraseña. Si los datos concuerdan con alguno de los usuarios registrados,
       la función retorna un True. En caso de no validarse correctamente, el usuario cuenta con
       intentos adicionales definidos en la variable login_attempts. En caso de error todos los
       intentos, la función retorna un false.

    Args:
        login_attempts (int, optional): Intentos de conexión que tiene permitidos el
                                        usuario. Defaults to 3.
    """
    # Inicializar variables
    successful_login = False  # If true, accede a la información de LifeStore. False al empezar.
    # Leer tabla donde se encuentran los usuarios permitidos
    user_table = pd.read_csv(USER_FILE_PATH)
    # Iniciar intento de login
    while successful_login is False and login_attempts > 0:
        # Caso: todos los intentos de registro son fallidos. Terminar la función con un False. 
        if login_attempts == 0:
            print("Demasiados intentos.\nEl acceso se ha desabilitado para este equipo.\n"+
                  "Para poder acceder nuevamente, acercarse con el equipo de TI de Life Store.")
            return False
        # Descontar un intento. 
        login_attempts-=1
        # Ingresar datos de entrada 
        user = input("Ingrese su usuario: ")
        password = input("Ingrese su contraseña: ")
        # Caso Usuario-Contraseña Validos
        if user_table['user_name'].str.contains(user).any():
            # Conseguir resto de los datos para ese usuario especifico
            user_data = user_table.loc[user_table['user_name'].str.contains(user)]
            # Si la contraseña concuerda con el usuario, concede acesso
            if user_data['password'].str.contains(password)[0]:
                successful_login = True
                print("Bienvenido "+user_data['name'][0]+".\n")
                return True
        # Caso: usuario o contraseña son invalidos
        if successful_login is False and login_attempts>0:
            print("\nError con el usuario o contraseña proporcionados. Revise e intente nuevamente.")

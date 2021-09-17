"""
MENU_UTILS

Funciones auxiliares para el menú de consola que se usa en la función principal.
Entre estas funciones se encuentras las siguientes:
    - Función para desplegar menú y seleccionar opción de dicho menú.
    - Función para validar si se hace nueva consulta o cierra sesión.

"""


def select_menu(menu_options: dict) -> int:
    """ Función auxiliar para desplegar menú en consola.
        Regresa unicamente la opción seleccionada.

    Args:
        menu_options (dict): Diccionario que tienen enteros como llaves
                             y las diferentes opciones como valores. 

    Returns:
        int: caso seleccionado del menú.
    """
    while True:
        print("\n¿Qué desea consultar?:")
        for key in menu_options.keys():
            print(f"{key}.- {menu_options[key]}")
        selected_option = input("Ingrese el número de la acción deseada:")
        # Validar que el dato sea entero o volver a poner el menu
        try:
            selected_option = int(selected_option)
        except:
            # Si el dato ingresado no es un entero, se indica error vuelve a mostrar menu.
            print("El valor ingresado no es un número. Ingrese el dato en el formato correcto.\n")
            continue
        # Validar que que el dato se encuentre dentro de las opciones indicadas
        if selected_option not in menu_options.keys():
            # Si no existe la opción, se presenta mensaje de error y se vuelve a mostrar menu.
            print("El número ingresado no se encuentra en el menú. Seleccione otra opción.\n")
            continue
        else:
            # Si el numero esta dentro del menu, se sale del while para terminar
            break
    return selected_option


def validate_continue() -> bool:
    """ Función para validar si se desea continuar dentro de la sesión o cerrala.

    Returns:
        bool: Boolean que indica si continuar o no haciendo consultas
    """
    while True:
        selected_option = input("¿Desea consultar otra opción (Y o N)?:").upper()
        # Validar si se selecciono una de las dos opciones
        if selected_option not in ["Y", "N"]:
            print("El dato no fue ingresado correctamente, favor de seleccionar una de las opciones especificadas.\n")
            continue
        else:
            # Convertir a selección a boolean
            if selected_option == 'Y':
                selected_option = True
            elif selected_option == 'N':
                selected_option = False
            break

    return selected_option

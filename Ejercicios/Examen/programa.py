import random
#Importamos de string la paqueteria ascii para poder generar la letra de opcion de los incisos
from string import ascii_lowercase
#Importamos pathlib, ya que crea una ruta concreta para la plataforma en la que se ejecuta el código
#Ademas hacemos uso de try y except por si hubiera problemas con la version de Python
import pathlib
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

print(input("Introduce tu nombre:"))
NUM_PREGUNTAS_EXAMEN = 10
#Importamos nuestro banco de preguntas de extension TOML
BANCO_PREGUNTAS =pathlib.Path(__file__).parent / "preguntas.toml"
PREGUNTAS = tomllib.loads(BANCO_PREGUNTAS.read_text())

num_preguntas = min(NUM_PREGUNTAS_EXAMEN, len(PREGUNTAS))
preguntas = random.sample(list(PREGUNTAS.items()), k=num_preguntas)

#Creamos un metodo para que se lea la respuesta que proporcione el usuario
def obtener_respuesta(pregunta, alternativas):
    print(f"{pregunta}?")
    alternativas_etiquetadas = dict(zip(ascii_lowercase, alternativas))
    for etiqueta, alternativa in alternativas_etiquetadas.items():
        print(f"  {etiqueta}) {alternativa}")

    while (respuesta_elegida := input("\n¿Elección? ")) not in alternativas_etiquetadas:
        print(f"Por favor responda una de {', '.join(alternativas_etiquetadas)}")

    return alternativas_etiquetadas[respuesta_elegida]

#Realiza la ejecución del examen, almacenando aciertos y errores
def ejecutar_examen():
    preguntas = preparar_preguntas(
        BANCO_PREGUNTAS, num_preguntas=NUM_PREGUNTAS_EXAMEN
    )
    num_correctas = 0
    num_incorrectas = 0
    for num, pregunta in enumerate(preguntas, start=1):
        print(f"\nPregunta {num}:")
        num_correctas += hacer_pregunta(pregunta)
        num_incorrectas += hacer_pregunta(pregunta)

    print(f"\nObtuviste {num_correctas} correctas de {num} preguntas")
    print(f"\nObtuviste {num_incorrectas} correctas de {num} preguntas")

#Permite revolver el paquete de preguntas que se realizaran del banco de preguntas
def preparar_preguntas(path, num_preguntas):
    preguntas = tomllib.loads(path.read_text())["preguntas"]
    num_preguntas = min(num_preguntas, len(preguntas))
    return random.sample(preguntas, k=num_preguntas)

#Permite crear la manera en que se presentaran las preguntas al usuario y aumentar puntajes
def hacer_pregunta(pregunta):
    respuesta_correcta = pregunta["respuesta"]
    opciones = [pregunta["respuesta"]] + pregunta["alternativas"]
    opciones_orden = random.sample(opciones, k=len(opciones))
    
    respuesta = obtener_respuesta(pregunta["pregunta"], opciones_orden)
    if respuesta == respuesta_correcta:
        print("⭐ Correcto ⭐")
        return 1
    else:
        print(f"La respuesta es {respuesta_correcta!r}, no ❌{respuesta!r}❌")
        return 0

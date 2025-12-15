import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pywhatkit
from datetime import datetime

# Motor de texto a voz
motor = pyttsx3.init()
nombre_asistente = "kai"

# wikipedia en español
wikipedia.set_lang("es")

# Función para cambiar de voz
def cambiar_voz(idioma="español"):
    voces = motor.getProperty('voices')
    if idioma == "español":
        motor.setProperty('voice', voces[2].id)  
    elif idioma == "ingles":
        motor.setProperty('voice', voces[0].id)  
    hablar(f"Ahora estoy usando una voz en {idioma}")

# Función para hablar
def hablar(texto):
    motor.say(texto)
    motor.runAndWait()

# Función para convertir audio a texto
def escuchar_comando():
    reconocedor = sr.Recognizer()
    
    with sr.Microphone() as fuente:
        print("Escuchando...")
        audio = reconocedor.listen(fuente)
        
        try:
            comando = reconocedor.recognize_google(audio, language="es-ES") 
            print(f"Usted dijo: {comando}")
            return comando.lower()
       
        except sr.UnknownValueError:
            hablar("Lo siento, no entendí eso.")
            return ""
        
        except sr.RequestError:
            hablar("No puedo conectar con el servicio de reconocimiento de voz.")
            return ""

# Obtener hora
def obtener_hora():
    hora_actual = datetime.now().strftime("%H:%M:%S")
    hablar(f"La hora actual es {hora_actual}")

# Buscar en Wikipedia
def buscar_wikipedia(consulta):
    resultados = wikipedia.summary(consulta, sentences=2, auto_suggest=False)
    hablar(f"De acuerdo con Wikipedia, {resultados}")
    print(resultados)

# Abrir Google
def abrir_google():
    webbrowser.open("https://www.google.com")
    hablar("Abriendo Google.")

# Reproducir YouTube
def reproducir_video_youtube(titulo_video):
    pywhatkit.playonyt(titulo_video)
    hablar(f"Reproduciendo {titulo_video} en YouTube.")

# Procesar comandos
def procesar_comando(comando):
    if nombre_asistente in comando:
        comando = comando.replace(nombre_asistente, "").strip()

        if "hora" in comando:
            obtener_hora()
        
        elif "busca en wikipedia" in comando:
            consulta = comando.replace("busca en wikipedia", "").strip()
            if consulta:
                buscar_wikipedia(consulta)
            else:
                hablar("Por favor, di qué quieres buscar en Wikipedia.")
        
        elif "abre google" in comando:
            abrir_google()

        elif "reproduce" in comando and "youtube" in comando:
            titulo_video = comando.replace("reproduce", "").replace("en youtube", "").strip()
            if titulo_video:
                reproducir_video_youtube(titulo_video)
            else:
                hablar("Por favor, di el nombre del video que quieres reproducir en YouTube.")
    
        elif "cambia a voz en español" in comando:
            cambiar_voz(idioma="español")
        
        elif "cambia a voz en ingles" in comando:
            cambiar_voz(idioma="ingles")

        else:
            hablar("Lo siento, no puedo realizar esa acción.")
    
    else:
        hablar("Debes llamarme por mi nombre antes de dar una orden.")

# Ejecutar asistente
if __name__ == "__main__":
    hablar(f"Hola, soy {nombre_asistente}, tu asistente virtual. ¿En qué puedo ayudarte hoy?")
    
    while True:
        comando = escuchar_comando()
        if comando:
            procesar_comando(comando)


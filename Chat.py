import spacy
import random
import tkinter as tk
from tkinter import scrolledtext

# Cargar modelo de español
nlp = spacy.load("es_core_news_sm")

# Opciones de recetas
recetas = {
    "desayuno": ["Caldo con arepa y chocolate", "Huevos revueltos con pan", "Avena con frutas"],
    "almuerzo": ["Arroz con pollo", "Bandeja paisa", "Sopa de verduras"],
    "cena": ["Arepa con queso", "Sándwich de pollo", "Ensalada ligera"],
    "salado": ["Empanadas", "Tamales", "Pizza casera"],
    "dulce": ["Postre de tres leches", "Arroz con leche", "Brownies de chocolate"]
}

# Para saber si el bot ya dio alguna recomendación
dio_recomendacion = False

def procesar_mensaje(mensaje):
    global dio_recomendacion
    doc = nlp(mensaje.lower())
    lemas = [token.lemma_ for token in doc]

    #print("\n[Depuracion] Tokens, Lemas y POS:")
    #for token in doc:
      #  print(token.text, "->", token.lemma_, "|", token.pos_)

    # Despedida
    if any(palabra in lemas for palabra in ["adiós", "chao", "salir", "hasta"]):
        return "Ha sido un gusto ayudarte, hasta luego :D"
    
    # Responder a agradecimientos
    if dio_recomendacion and any(palabra in lemas for palabra in ["gracias", "okey", "valer"]):
        dio_recomendacion = False
        return "¡Con gustooo! ¿Quieres otra recomendación?"
    
    # Saludos
    if ("hola" in lemas or "buena" in lemas or "buen" in lemas and 
        any(palabra in lemas for palabra in ["día", "tarde", "noche"])):
        return "¡Hola! Soy tu recomendador de recetas. ¿Prepararás desayuno, almuerzo, cena o algo dulce/salado?"
    
    # Buscar recetas por categoría
    for categoria in recetas.keys():
        if categoria in lemas:
            dio_recomendacion = True
            return f"Te recomiendo preparar: {random.choice(recetas[categoria])}"
    
    # Respuesta por defecto
    return "No entendí bien :( ¿Quieres una receta para desayuno, almuerzo, cena, algo salado o dulce?"

# Crear la ventana principal
root = tk.Tk()
root.title("Chat Recomendador de Recetas")
root.geometry("500x600")
root.configure(bg="#d8b4fe")  # Fondo lila

# Área de chat (scrolledtext para mostrar la conversación)
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=50, font=("Arial", 12), state="disabled", spacing1=5, spacing3=5)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Configurar tags para colores de texto
chat_area.tag_configure("user", foreground="#1e40af")  # Azul para el usuario
chat_area.tag_configure("bot", foreground="#6b21a8")   # Morado para el bot

# Cuadro de texto para la entrada del usuario
entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.X, expand=True, ipady=5)  # Ajustar altura con ipady

# Botón para enviar mensajes
send_button = tk.Button(root, text="Enviar", font=("Arial", 12), bg="#4f46e5", fg="white", command=lambda: enviar_mensaje(), height=2)
send_button.pack(padx=5, pady=5, side=tk.LEFT)

def enviar_mensaje():
    mensaje = entry.get().strip()
    if not mensaje:
        return
    
    # Mostrar mensaje del usuario
    chat_area.configure(state="normal")
    chat_area.insert(tk.END, f"Tú: {mensaje}\n\n", "user")  # Añadir espacio extra y tag de color
    chat_area.configure(state="disabled")
    entry.delete(0, tk.END)
    
    # Procesar mensaje y mostrar respuesta del bot
    respuesta = procesar_mensaje(mensaje)
    chat_area.configure(state="normal")
    chat_area.insert(tk.END, f"Bot: {respuesta}\n\n", "bot")  # Añadir espacio extra y tag de color
    chat_area.configure(state="disabled")
    chat_area.yview(tk.END)  # Auto-scroll al final
    
    # Si el bot responde "cerrar", desactivar la entrada
    if respuesta == "Ha sido un gusto ayudarte, hasta luego :D":
        entry.config(state="disabled")
        send_button.config(state="disabled")

# Permitir enviar mensajes con la tecla Enter
entry.bind("<Return>", lambda event: enviar_mensaje())

# Mensaje inicial
chat_area.configure(state="normal")
chat_area.insert(tk.END, "Bot: ¡Bienvenido! Saluda para comenzar.\n\n", "bot")
chat_area.configure(state="disabled")

# Iniciar la aplicación
root.mainloop()
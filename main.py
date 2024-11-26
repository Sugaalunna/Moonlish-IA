import streamlit as luna #type: ignore
from groq import Groq #type: ignore

# luna.header("Hola")
# luna.subheader("Chau")

# luna.set_page_config(page_title='Mi primer ChatBot')

# nombre = luna.text_input('Escribi tu nombre')

# luna.button('Saludar')
# luna.write(f'Hola {nombre} bienvenido a Talento Tech')

# option = luna.selectbox('¿Con quién perdió Boca la semana pasada?', ['Riestra', 'Independiente'])

# if option == 'Riestra':
#     luna.success('¡CORRECTO!')
# elif option == 'Independiente':
#     luna.error('¡INCORRECTO!')

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#def = palabra designada para brindar una funcion

def configurar_page():
    luna.sidebar.title('Mi APP con IA')
    elejirModelo = luna.sidebar.selectbox('Elegí un modelo',options=MODELOS,index=0)

    if elejirModelo == 'llama3-8b-8192':
        luna.title('Mi sesión de llama3-8b-8192')
        luna.header(f'llama3-8b-8192')
    elif elejirModelo == 'llama3-70b-8192':
        luna.title('Mi sesión de llama3-70b-8192')
        luna.header(f'llama3-70b-8192')
    elif elejirModelo == 'mixtral-8x7b-32768':
        luna.title('Mi sesión de mixtral-8x7b-32768')
        luna.header(f'mixtral-8x7b-32768')
    return elejirModelo

    # modelo = config_chatbot()
    # print(modelo)

#mensaje = luna.chat_input('ENVIA UN MENSAJE A CHATGPT')

def config_user_groq():
    api_key = luna.secrets["API_KEY"]
    return Groq(api_key=api_key)

def config_model(cliente,modelo,mensajeDeRecibo):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role":"user", "content": mensajeDeRecibo}],
        stream=True
    )
    # clienteUsuario = config_user_groq()

    # mensaje = luna.chat_input('ENVIA UN MENSAJE A CHATGPT')

    # if mensaje:
    # config_model(clienteUsuario,modelo,mensaje)
    # print(mensaje)

def cache():
    if "mensajes" not in luna.session_state:
        luna.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    luna.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in luna.session_state.mensajes:
        with luna.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            luna.markdown(mensaje["content"])

def area_chat():
        contenedorDelChat = luna.container(height=400,border=True)
        with contenedorDelChat:
            mostrar_historial()

def main():
    modelo = configurar_page()
    clienteUsuario = config_user_groq()
    cache()

    mensaje = luna.chat_input("Escribí tu mensaje")

    if mensaje:
        actualizar_historial("user", mensaje, "👩🏻‍💻")

        chat_completo = config_model(clienteUsuario, modelo, mensaje)

        respuesta_completa = ""
        for frase in chat_completo:
            if frase.choices[0].delta.content:
                respuesta_completa += frase.choices[0].delta.content
        
        actualizar_historial("assistant", respuesta_completa, "🤖")
    
    area_chat()

if __name__ == "__main__":
    main()

# color picker para buscar paleta de colores en google
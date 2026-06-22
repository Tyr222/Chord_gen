import streamlit as st
from midiutil import MIDIFile
import random
import base64
import streamlit.components.v1 as components
#MyMIDI.addNote(track, channel, pitch, time, duration, volume)
# duration = 4 ➔ Semibreve (dura 4 batidas)

# duration = 2 ➔ Mínima (dura 2 batidas)

# duration = 1 ➔ Semínima (dura 1 batida)

# duration = 0.5 ➔ Colcheia (dura meia batida)


st.title("CHORD GEN", text_alignment='center')


tons = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
tom_maior  = [0, 2, 4, 5, 7, 9, 11]  # R T T S T T T
tom_menor  = [0, 2, 3, 5, 7, 8, 10]  # R T S T T S T
notas = {
    "C": 60, "C#": 61, "D": 62, "D#": 63,
    "E": 64, "F": 65, "F#": 66, "G": 67,
    "G#": 68, "A": 69, "A#": 70, "B": 71
}
lista_acordes = []
nomes_acordes = []
#cria a chave do session state! não havendo valores ele mostra os botões e o texto.
if "modo" not in st.session_state:
    st.session_state.modo = None
    st.markdown("**Escolha o modo!**", text_alignment="center")

col1, col2, = st.columns(2, gap="xxsmall")

#Se não tiver nada salvo, ele oferece duas opções. 
# Sendo uma delas selecionadas ele executa um rerun, fazendo o codigo cair no else e pulando o if
if st.session_state.modo is None:
    with col1:
        maior = st.button(icon="🎼", label="MODO MAIOR", use_container_width=True)
        if maior:
            st.session_state.modo = "maior"
            st.rerun()

    with col2:
        menor = st.button(icon="🎶", label="MODO MENOR", use_container_width=True)
        if menor:
            st.session_state.modo = "menor"
            st.rerun()
else:       
    #modo já escolhido
    voltar = st.button("Voltar", icon_position="left")
    
    st.markdown(f"Modo {(st.session_state.modo).capitalize()} selecionado!", text_alignment="center")
    opcoes = st.form("opcoes")
    with opcoes:
        tonalidade = st.selectbox(f"Escolha a tonalidade", [t for t in tons], )
        bpm = st.number_input("BPM", 0, 200, value=60)
        num_acordes = st.number_input("Quantidade de acordes", 2, 6, value=2)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            gen = st.form_submit_button("Gerar progressão!")
        
        
        if gen:
            modo = st.session_state.modo
            tradutor_notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            while len(lista_acordes) < num_acordes:
                if modo == "maior":
                    escala_midi = [notas[tonalidade] + f for f in tom_maior]
                    tonica = [escala_midi[0], escala_midi[0]+4, escala_midi[0]+7]
                    grau_maior = [escala_midi[0], escala_midi[3], escala_midi[4]]
                    grau_menor = [escala_midi[1], escala_midi[2], escala_midi[5]]
                    grau_b5 = [escala_midi[6]]
                    root_note = random.choice(escala_midi)
                    if root_note in grau_maior:
                        chord = [root_note, root_note+4, root_note+7]
                        nome_cifra = tradutor_notas[root_note % 12]
                    elif root_note in grau_menor:
                        chord = [root_note, root_note+3, root_note+7]
                        nome_cifra = tradutor_notas[root_note % 12] + "m"
                    elif root_note in grau_b5:
                        chord = [root_note, root_note+3, root_note+6]
                        nome_cifra = tradutor_notas[root_note % 12] + "dim"

                elif modo == "menor":
                    escala_midi = [notas[tonalidade] + f for f in tom_menor]
                    tonica = [escala_midi[0], escala_midi[0]+3, escala_midi[0]+7]
                    grau_maior = [escala_midi[2], escala_midi[5], escala_midi[6]]
                    grau_menor = [escala_midi[0], escala_midi[3], escala_midi[4]]
                    grau_b5 = [escala_midi[1]]
                    root_note = random.choice(escala_midi)
                    if root_note in grau_maior:
                            chord = [root_note, root_note+4, root_note+7]
                            nome_cifra = tradutor_notas[root_note % 12]
                    elif root_note in grau_menor:
                            chord = [root_note, root_note+3, root_note+7]
                            nome_cifra = tradutor_notas[root_note % 12] + "m"
                    elif root_note in grau_b5:
                            chord = [root_note, root_note+3, root_note+6]
                            nome_cifra = tradutor_notas[root_note % 12] + "dim"
                
                lista_acordes.append(chord)
                nomes_acordes.append(nome_cifra)

                if len(lista_acordes) == num_acordes:
                    break
        
            if tonica not in lista_acordes:
                indice = random.randint(0, len(lista_acordes) - 1)
                lista_acordes[indice] = tonica
                nomes_acordes[indice] = tonalidade if modo == "maior" else tonalidade + "m"

        if voltar:
            st.session_state.modo = None
            st.rerun()

        # st.write(lista_acordes)
        print(lista_acordes)
     
        # MIDI note number
    track    = 0
    channel  = 0
    time     = 0   # In beats
    duration = 2   # In beats
    tempo    = bpm  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track,time, tempo)

    for acorde in lista_acordes:
        for nota in acorde:
            MyMIDI.addNote(track, channel, nota, time, duration, volume)
        time = time + duration 
    
    with open("generated_chord.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
    
# 1. Lemos o arquivo gerado e convertemos para texto (Base64)
    with open("generated_chord.mid", "rb") as f:
        midi_data = f.read()
        b64_midi = base64.b64encode(midi_data).decode("utf-8")

    # 2. O bloco HTML/JS "mágico" usando o html-midi-player do Google
    html_player = f"""
    <script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.23.1/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.5.0"></script>
    
    <midi-player
        src="data:audio/midi;base64,{b64_midi}"
        sound-font="https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus"
        style="width: 100%;">
    </midi-player>
    """

    # 3. Injetamos o player na tela do Streamlit
    components.html(html_player, height=60)
    # EXIBIÇÃO DAS CIFRAS: Centralizadas, sem asteriscos e com nova cor
    st.write("")
    cifras_formatadas = " &nbsp;&nbsp;➔&nbsp;&nbsp; ".join(nomes_acordes)
    
    # Troque o #FFFFFF (Branco) pelo código da cor que você preferir!
    st.markdown(f"<h3 style='text-align: center; color: #FFFFFF;'>{cifras_formatadas}</h3>", unsafe_allow_html=True)
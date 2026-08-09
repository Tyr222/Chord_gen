from flask import Flask, render_template, request, jsonify
import random, base64, io
from midiutil import MIDIFile


app = Flask(__name__)

tons = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
modos = ["Maior", "Menor Natural", "Menor Harmônico"]
tom_maior  = [0, 2, 4, 5, 7, 9, 11]  # R T T S T T T
tom_menor  = [0, 2, 3, 5, 7, 8, 10]  # R T S T T S T
tom_menor_harmonico = [0, 2, 3, 5, 7, 8, 11] # R T S T T S TT
notas = {
    "C": 60, "C#": 61, "D": 62, "D#": 63,
    "E": 64, "F": 65, "F#": 66, "G": 67,
    "G#": 68, "A": 69, "A#": 70, "B": 71
}

@app.route("/")
def home():
    return render_template('index.html', tons=tons, modos=modos)


@app.route("/gerar")
def gerar_musica():
    lista_acordes = []
    lista_cifra = []
    graus = []
    tom = request.args.get("tom", "C")
    modo = request.args.get("modo", "Maior")
    quantidade = int(request.args.get("quantidade", "4"))
    while len(lista_acordes) < quantidade:
        if modo == "Maior":
            escala_midi = [notas[tom] + t for t in tom_maior]
            acorde_tonica = [escala_midi[0], escala_midi[0]+4, escala_midi[0]+7]
            grau_maior = [escala_midi[0], escala_midi[3], escala_midi[4]]
            grau_menor = [escala_midi[1], escala_midi[2], escala_midi[5]]
            grau_b5 = [escala_midi[6]]
            nota_fundamental_aleatoria = random.choice(escala_midi)
            if nota_fundamental_aleatoria in grau_maior:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+4, nota_fundamental_aleatoria+7]
                cifra = tons[nota_fundamental_aleatoria % 12]
            elif nota_fundamental_aleatoria in grau_menor:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+3, nota_fundamental_aleatoria+7]
                cifra = tons[nota_fundamental_aleatoria % 12] + "m"
            elif nota_fundamental_aleatoria in grau_b5:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+3, nota_fundamental_aleatoria+6]
                cifra = tons[nota_fundamental_aleatoria % 12] + "(b5)"

            if nota_fundamental_aleatoria == escala_midi[0]:
                grau = "I"
            if nota_fundamental_aleatoria == escala_midi[1]:
                grau = "ii"
            if nota_fundamental_aleatoria == escala_midi[2]:
                grau = "iii"
            if nota_fundamental_aleatoria == escala_midi[3]:
                grau = "IV"
            if nota_fundamental_aleatoria == escala_midi[4]:
                grau = "V"
            if nota_fundamental_aleatoria == escala_midi[5]:
                grau = "vi"
            if nota_fundamental_aleatoria == escala_midi[6]:
                grau = "vii°"

        elif modo == "Menor Natural":
            escala_midi = [notas[tom] + f for f in tom_menor]
            acorde_tonica = [escala_midi[0], escala_midi[0]+3, escala_midi[0]+7]
            grau_maior = [escala_midi[2], escala_midi[5], escala_midi[6]]
            grau_menor = [escala_midi[0], escala_midi[3], escala_midi[4]]
            grau_b5 = [escala_midi[1]]
            nota_fundamental_aleatoria = random.choice(escala_midi)
            if nota_fundamental_aleatoria in grau_maior:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+4, nota_fundamental_aleatoria+7]
                cifra = tons[nota_fundamental_aleatoria % 12]
            elif nota_fundamental_aleatoria in grau_menor:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+3, nota_fundamental_aleatoria+7]
                cifra = tons[nota_fundamental_aleatoria % 12] + "m"
            elif nota_fundamental_aleatoria in grau_b5:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+3, nota_fundamental_aleatoria+6]
                cifra = tons[nota_fundamental_aleatoria % 12] + "(b5)"

            if nota_fundamental_aleatoria == escala_midi[0]:
                grau = "vi"
            if nota_fundamental_aleatoria == escala_midi[1]:
                grau = "vii°"
            if nota_fundamental_aleatoria == escala_midi[2]:
                grau = "I"
            if nota_fundamental_aleatoria == escala_midi[3]:
                grau = "ii"
            if nota_fundamental_aleatoria == escala_midi[4]:
                grau = "iii"
            if nota_fundamental_aleatoria == escala_midi[5]:
                grau = "IV"
            if nota_fundamental_aleatoria == escala_midi[6]:
                grau = "V"

        else:
            escala_midi = [notas[tom] + f for f in tom_menor_harmonico]
            acorde_tonica = [escala_midi[0], escala_midi[0]+3, escala_midi[0]+7]
            grau_maior = [escala_midi[2], escala_midi[5]]
            grau_menor = [escala_midi[0], escala_midi[3]]
            grau_emprestimo = [escala_midi[4]]
            grau_diminuto = [escala_midi[1], escala_midi[6]]
            nota_fundamental_aleatoria = random.choice(escala_midi)
            if nota_fundamental_aleatoria in grau_maior:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+4, nota_fundamental_aleatoria+7]
                cifra = tons[nota_fundamental_aleatoria % 12] 
            elif nota_fundamental_aleatoria in grau_menor:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+3, nota_fundamental_aleatoria+7]
                cifra = tons[nota_fundamental_aleatoria % 12] + "m"
            elif nota_fundamental_aleatoria in grau_diminuto:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+3, nota_fundamental_aleatoria+6, nota_fundamental_aleatoria+9]
                cifra = tons[nota_fundamental_aleatoria % 12] + "dim"
            elif nota_fundamental_aleatoria in grau_emprestimo:
                acorde = [nota_fundamental_aleatoria, nota_fundamental_aleatoria+4, nota_fundamental_aleatoria+7]
                cifra = tons[nota_fundamental_aleatoria % 12]
            if nota_fundamental_aleatoria == escala_midi[0]:
                grau = "vi" 
            if nota_fundamental_aleatoria == escala_midi[1]:
                grau = "vii°" 
            if nota_fundamental_aleatoria == escala_midi[2]:
                grau = "I" 
            if nota_fundamental_aleatoria == escala_midi[3]:
                grau = "ii" 
            if nota_fundamental_aleatoria == escala_midi[4]:
                grau = "III" 
            if nota_fundamental_aleatoria == escala_midi[5]:
                grau = "IV"
            if nota_fundamental_aleatoria == escala_midi[6]:
                grau = "V" 

        lista_cifra.append(cifra)
        lista_acordes.append(acorde)
        graus.append(grau)
        if len(lista_acordes) == quantidade:
            break

    if acorde_tonica not in lista_acordes:
        indice = random.randint(0, len(lista_acordes) - 1)
        lista_acordes[indice] = acorde_tonica
        lista_cifra[indice] = tom if modo == "Maior" else tom + "m"
        graus[indice] = "I" if modo == "Maior" else "vi" 


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    track    = 0
    channel  = 0
    time     = 0   # In beats
    duration = 2   # In beats
    tempo    = 100  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track,time, tempo)

    for acorde in lista_acordes:
        for nota in acorde:
            MyMIDI.addNote(track, channel, nota, time, duration, volume)
        time = time + duration 

    #Para evitar conflitos com 2 requisições feitas ao mesmo tempo, ao invés de codificar o nome do arquivo MIDI
    #Usei o io.BytesIO() para criar um buffer em memória sem precisar escrever o arquivo em disco.
    #Por fim, codifiquei para base64 usando a lib de memso nome.
    buffer_midi = io.BytesIO() 
    MyMIDI.writeFile(buffer_midi)
    b64_midi = base64.b64encode(buffer_midi.getvalue()).decode("utf-8")

    return jsonify({
        "midi":b64_midi,
        "lista":lista_cifra,
        "graus":graus
    })



if __name__ == "__main__":
    app.run(debug=True)
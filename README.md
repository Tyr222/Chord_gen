# 🎵 CHORD GEN

**CHORD GEN** is an automatic harmonic progression generator built with Python. It creates musical logic based on real music theory, generates MIDI files instantly, and renders an audio synthesizer directly in the browser so the user can listen to the composition.

## 🚀 Features

* **Smart Generation:** Creates mathematically coherent chord progressions within Major and Minor modes, ensuring the presence of the root note (tonic).
* **Customization:** Allows the user to choose the Key, the tempo (BPM), and the exact number of chords in the progression.
* **Integrated Web Synthesizer:** Uses the Google Magenta engine via JavaScript to play the generated MIDI files directly in the browser, using real piano sounds.
* **Dynamic Chords:** Displays the names of the generated chords in real-time on the interface to facilitate study or application of the harmony on real instruments.

## 🛠️ Technologies Used

* **Python:** Main language responsible for all backend logic and scale calculations.
* **Streamlit:** Framework used to build the entire web interface (Front-end) quickly and reactively.
* **MidiUtil:** Python library responsible for writing the notes, durations, and beats into a physical `.mid` file.
* **Google Magenta:** Web/JavaScript component injected into the code to synthesize and play the audio.
* **HTML/CSS:** Used natively within Streamlit to style buttons, colors, and interface responsiveness.

## 💻 How to run the project locally

If you want to clone this repository and run it on your machine, follow these steps:

1. Clone the repository:
```bash
git clone [https://github.com/Tyr222/chord-gen.git](https://github.com/Tyr222/chord-gen.git)

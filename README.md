# Human Voice Activity Detector

This project is a Human Voice Activity Detector built using Streamlit, PyAudio, Matplotlib, Librosa, and PyTorch. It allows users to upload audio files, and detect speech segments in the provided audio.

## Setup

Open the folder in your preferred IDE and before running the project, make sure to install the required dependencies. You can use the following commands:

```bash
pip install -r requirements.txt
```
Additionally, if you are running the project in a virtual environment, activate it before installing the dependencies.

## Running the App

To run the Streamlit app, use the following command:

```bash
streamlit run app.py
```
This will start the app and open it in your default web browser. You can then interact with the Human Voice Activity Detector.

## Usage

### Recording Audio

```bash
1.Enter a filename and set the duration for recording in the provided form.
2.Click the "Record" button to start recording from the microphone.
3.Click the "Stop Recording" button to stop the recording.
4.Download the recorded audio using the provided download button.
```

### Upload the Recorded Audio File
```bash
1.Use the "Upload Audio" button to upload a WAV file.
2.The app will display the waveform and play the raw audio.
```

### Speech Detection

```bash
1.The app processes the audio file using a pre-trained speech detection model.
2.Detected speech segments are highlighted in the waveform plot.
3.If no speech is detected, an error message is displayed.
```
### Resetting the App

```bash
Click the "Reset" button to clear the current recording or uploaded audio and start over
```

## Important Notes

```bash
• Ensure that the required system dependencies for PyAudio are installed. If not, uncomment the # RUN apt-get update && apt-get install -y portaudio19-dev line in the requirements.txt file.
• The app uses a pre-trained speech detection model from the "snakers4/silero-vad" repository. It will automatically download the model during the first run.
```

## Contributors
 
#### • Mridul kant Kaushik
#### • Shubham Shandilya

## 
# Happy voice detecting!

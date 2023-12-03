import streamlit as st
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from matplotlib.colors import ListedColormap
import torch
from pprint import pprint
import tempfile
import helper as hp
from io import BytesIO

reset = False

st.title("Human Voice Activity Detector")

# record audio
st.subheader("Record Audio From Microphone")
with st.form("enter_info_form"):
    filename = st.text_input("FILENAME")+".wav"
    duration = st.number_input("DURATION", min_value=0)
    record_button = st.form_submit_button("Record")
    
    
st.session_state["recording_done"] = False

if record_button:
    
    if "recording_state" not in st.session_state:
        st.session_state["recording_state"] = True
    
    try:
        hp.record_Audio(filename, duration)
        
        # reading the conent of the audio file 
        with open(filename, 'rb') as file:
            audio_content = file.read()
            audio_file = BytesIO(audio_content)     # converting it to BytesIO format 
            
        st.download_button(
            label=f"Download {filename}",
            data = audio_file,
            file_name=filename,
            mime="audio/wav",
        )
        
    except ValueError as e:
        st.error(str(e))    
# TODO
#upload audio file with streamlit
else:
    audio_file = st.file_uploader("Upload Audio", type=["wav"])
    reset = True

if audio_file is not None:
    # Save the uploaded audio file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(audio_file.getvalue())
        # tmp_file.write(audio_file.read())
        tmp_file_name = tmp_file.name

    # audio_file.seek(0)   # Seek to the beginning of the file
    tmp_file.close()
    # print(audio_file)
    plt.figure(figsize = (14,5))
    data, sample_rate = librosa.load(tmp_file_name,sr=16000)
    # Plot the waveform
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(data, sr=16000)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()

    # Display the plot in Streamlit
    st.audio(data, format="audio/wav", sample_rate=sample_rate)
    st.caption("Raw Audio Waveform")
    st.pyplot(plt)

    with st.spinner('Processing the audio file...'):
        torch.set_num_threads(1)

        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                    model='silero_vad',
                                    force_reload=True)

        (get_speech_timestamps,
        _, read_audio,
        *_) = utils

        sampling_rate = 16000
        wav = read_audio(audio_file, sampling_rate=sampling_rate) #type(wav) = <class 'torch.Tensor'>
        # print(wav)
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=sampling_rate)
        # pprint(speech_timestamps)

        plt.figure(figsize = (14,5))
        # data,sample_rate = librosa.load(local_audio_file_path, sr=sampling_rate)
        librosa.display.waveshow(np.array(wav), sr = sampling_rate)
        if len(speech_timestamps) != 0:
            plt.title("Detected Speech Segments")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            for timestamp in speech_timestamps:
                start_time = timestamp['start'] / sampling_rate
                end_time = timestamp['end'] / sampling_rate
                plt.axvspan(start_time, end_time, alpha=0.5, color='gray', label='Detected Speech')

            st.success("Speech Segments Detected!")
            st.caption("Model Output with Detected Speech Segments")
            st.pyplot(plt)
        else:
            print("No Speech Detected")
            st.error("No Speech Detected")

if st.session_state['recording_done'] or reset:            
    if st.button("Reset", ):
        st.session_state["recording_state"] = False
        st.rerun()  
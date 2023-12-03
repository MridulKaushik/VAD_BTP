import streamlit as st
from pyaudio import paInt16, PyAudio
import wave
    
def record_Audio(filename, duration):
    """
     A audio-recording helping function Using PyAudio 
    """
    
    if not filename:
        raise ValueError("Filename not specified. Please provide a filename!")
    
    CHUNK = 1024
    FORMAT = paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_TIME = duration

    
    recording_state = st.session_state.get("recording_state", False)
    recording_info_placeholder = st.empty()
    if recording_state:
        
        recording_info_placeholder.info("Recording... ")


        with wave.open(filename, 'wb') as f:
            p = PyAudio()
            f.setnchannels(CHANNELS)
            f.setsampwidth(p.get_sample_size(FORMAT))
            f.setframerate(RATE)
            default_output_device_index = p.get_default_output_device_info()['index']
            defualt_input_device_index = p.get_default_input_device_info()['index']
            print("Input - ", p.get_default_input_device_info(), defualt_input_device_index)
            print(default_output_device_index, default_output_device_index)    
            stream = p.open(format=FORMAT, 
                            channels=CHANNELS, 
                            rate=RATE,
                            input=True,
                            output=True,
                            input_device_index=defualt_input_device_index,
                            output_device_index=default_output_device_index)
            
            
            stop_button = st.button("Stop Recording")
                
            for _ in range(0, RATE // CHUNK * RECORD_TIME):
                
                f.writeframes(stream.read(CHUNK))
                
                if stop_button:
                    break
                    
            
            recording_info_placeholder.success("Recording Completed\nThese are the results:")
            
            st.session_state["recording_done"] = True
                
            stream.close()
            p.terminate()

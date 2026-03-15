# stt_local 

import requests
import json

def transcribe_audio(audio_file, api_url, model="Systran/faster-whisper-base"):
    """
    Transcribes audio using the Whisper API.

    Args:h
        audio_file (str): Path to the audio file.
        api_url (str):  The URL of the Whisper API endpoint.
        model (str): The Whisper model to use.  Defaults to "Systran/faster-whisper-small".

    Returns:
        str: The transcribed text, or None if there was an error.
    """

    try:
        with open(audio_file, 'rb') as f:
            files = {'file': f}
            payload = {
                "model": model,
                "language": "en"  # Let Whisper auto-detect the language
            }

            response = requests.post(api_url, files=files, data=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            data = response.json()
            # Check for 'text' in the response.  API responses can vary.
            if 'text' in data:
                return data['text']
            elif 'segments' in data and len(data['segments']) > 0:
                # If the API returns segments, concatenate them to create the full text
                transcribed_text = " ".join([segment['text'] for segment in data['segments']])
                return transcribed_text
            else:
                print(f"Error: Unexpected response format from API.  Response: {data}")
                return None

    except FileNotFoundError:
        print(f"Error: Audio file not found at {audio_file}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred during the request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON response: {e}")
        return None


if __name__ == "__main__":
    # STT configuration
    # IMPORTANT: For local testing, replace "localhost" with the actual IP address of your STT server.
    api_url="http://localhost:8000/v1/audio/transcriptions"
    # Default path to your audio file
    audio_file = "chanakya_robot.wav"

    # Call the transcription function
    transcription = transcribe_audio(audio_file, api_url)

    if transcription:
        print("Transcription:")
        print(transcription)
    else:
        print("Transcription failed.")
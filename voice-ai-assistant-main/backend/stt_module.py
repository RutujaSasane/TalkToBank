import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import speech recognition libraries
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    logger.warning("SpeechRecognition not available")

try:
    import openai
    OPENAI_AVAILABLE = True
    openai.api_key = os.getenv('OPENAI_API_KEY', '')
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI Whisper not available")


def speech_to_text_google(audio_path: str) -> str:
    """
    Convert speech to text using Google Speech Recognition (free)
    """
    if not SR_AVAILABLE:
        raise Exception("SpeechRecognition library not installed")
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Record audio data
            audio_data = recognizer.record(source)
            
        # Use Google Speech Recognition (free)
        text = recognizer.recognize_google(audio_data)
        logger.info(f"Transcribed text (Google): {text}")
        return text
    
    except sr.UnknownValueError:
        logger.error("Google Speech Recognition could not understand audio")
        raise Exception("Could not understand audio")
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition: {e}")
        raise Exception("Speech recognition service error")


def speech_to_text_whisper(audio_path: str, language: str = None) -> str:
    """
    Convert speech to text using OpenAI Whisper API
    
    Args:
        audio_path: Path to audio file
        language: Language code (en, hi, mr) or None for auto-detect
    """
    if not OPENAI_AVAILABLE or not openai.api_key:
        raise Exception("OpenAI API not available or API key not set")
    
    try:
        with open(audio_path, 'rb') as audio_file:
            params = {
                "model": "whisper-1",
                "file": audio_file
            }
            # Add language if specified (Whisper supports: en, hi, mr, etc.)
            if language:
                params["language"] = language
            
            transcript = openai.Audio.transcribe(**params)
        
        text = transcript.get('text', '')
        logger.info(f"Transcribed text (Whisper): {text}")
        return text
    
    except Exception as e:
        logger.error(f"Whisper transcription error: {str(e)}")
        raise Exception(f"Whisper transcription failed: {str(e)}")


def speech_to_text(audio_path: str, method: str = 'auto', language: str = None) -> str:
    """
    Main speech-to-text function
    
    Args:
        audio_path: Path to audio file
        method: 'google', 'whisper', or 'auto' (tries Whisper first, falls back to Google)
        language: Language code (en, hi, mr) for multilingual support
    
    Returns:
        Transcribed text
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    if method == 'whisper':
        return speech_to_text_whisper(audio_path, language)
    
    elif method == 'google':
        return speech_to_text_google(audio_path)
    
    elif method == 'auto':
        # Try Whisper first (more accurate, supports multilingual), fall back to Google
        if OPENAI_AVAILABLE and openai.api_key:
            try:
                return speech_to_text_whisper(audio_path, language)
            except Exception as e:
                logger.warning(f"Whisper failed, falling back to Google: {str(e)}")
        
        # Fall back to Google (primarily supports English)
        if SR_AVAILABLE:
            return speech_to_text_google(audio_path)
        
        raise Exception("No speech recognition method available")
    
    else:
        raise ValueError(f"Unknown method: {method}")


if __name__ == '__main__':
    # Test the STT module
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        try:
            text = speech_to_text(audio_file)
            print(f"Transcribed: {text}")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Usage: python stt_module.py <audio_file_path>")

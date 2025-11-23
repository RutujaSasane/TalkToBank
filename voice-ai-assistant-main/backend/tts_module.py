import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import TTS libraries
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logger.warning("gTTS not available")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests library not available")


def text_to_speech_gtts(text: str, output_path: str, lang: str = 'en', **kwargs) -> bool:
    """
    Convert text to speech using Google Text-to-Speech (free)
    
    Args:
        text: Text to convert
        output_path: Path to save audio file
        lang: Language code (default: 'en')
    
    Returns:
        True if successful
    """
    if not GTTS_AVAILABLE:
        raise Exception("gTTS library not installed")
    
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
        logger.info(f"Generated TTS audio (gTTS): {output_path}")
        return True
    
    except Exception as e:
        logger.error(f"gTTS error: {str(e)}")
        raise Exception(f"Text-to-speech failed: {str(e)}")


def text_to_speech_elevenlabs(text: str, output_path: str, voice_id: Optional[str] = None) -> bool:
    """
    Convert text to speech using ElevenLabs API (premium)
    
    Args:
        text: Text to convert
        output_path: Path to save audio file
        voice_id: ElevenLabs voice ID (optional)
    
    Returns:
        True if successful
    """
    if not REQUESTS_AVAILABLE:
        raise Exception("requests library not installed")
    
    api_key = os.getenv('ELEVENLABS_API_KEY', '')
    if not api_key:
        raise Exception("ElevenLabs API key not set")
    
    # Default voice ID (you can change this)
    if not voice_id:
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"Generated TTS audio (ElevenLabs): {output_path}")
            return True
        else:
            raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")
    
    except Exception as e:
        logger.error(f"ElevenLabs error: {str(e)}")
        raise Exception(f"Text-to-speech failed: {str(e)}")


def text_to_speech(text: str, output_path: str, method: str = 'auto', **kwargs) -> bool:
    """
    Main text-to-speech function
    
    Args:
        text: Text to convert
        output_path: Path to save audio file
        method: 'gtts', 'elevenlabs', or 'auto' (tries ElevenLabs first, falls back to gTTS)
        **kwargs: Additional arguments for specific methods
    
    Returns:
        True if successful
    """
    if not text:
        raise ValueError("Text cannot be empty")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if method == 'elevenlabs':
        return text_to_speech_elevenlabs(text, output_path, **kwargs)
    
    elif method == 'gtts':
        return text_to_speech_gtts(text, output_path, **kwargs)
    
    elif method == 'auto':
        # Try ElevenLabs first (better quality), fall back to gTTS
        elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY', '')
        if REQUESTS_AVAILABLE and elevenlabs_api_key:
            try:
                return text_to_speech_elevenlabs(text, output_path, **kwargs)
            except Exception as e:
                logger.warning(f"ElevenLabs failed, falling back to gTTS: {str(e)}")
        
        # Fall back to gTTS
        if GTTS_AVAILABLE:
            return text_to_speech_gtts(text, output_path, **kwargs)
        
        raise Exception("No text-to-speech method available")
    
    else:
        raise ValueError(f"Unknown method: {method}")


if __name__ == '__main__':
    # Test the TTS module
    import sys
    
    if len(sys.argv) > 1:
        test_text = ' '.join(sys.argv[1:])
        output_file = "test_output.mp3"
        
        try:
            text_to_speech(test_text, output_file)
            print(f"Audio saved to: {output_file}")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Usage: python tts_module.py <text to convert>")

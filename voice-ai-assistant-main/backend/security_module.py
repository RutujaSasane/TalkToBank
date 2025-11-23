import hashlib
import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any
import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_PATH = 'database.db'


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_voice_signature(audio_path: str) -> str:
    """
    Generate a hash signature from audio file (mock implementation)
    In production, use actual voice biometric analysis
    """
    try:
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
            # Create hash from audio data
            voice_hash = hashlib.sha256(audio_data).hexdigest()
        return voice_hash
    except Exception as e:
        logger.error(f"Voice hashing error: {str(e)}")
        raise Exception("Failed to process voice signature")


def register_voice(user_id: int, audio_path: str) -> Dict[str, Any]:
    """
    Register user's voice signature
    """
    try:
        voice_hash = hash_voice_signature(audio_path)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET voice_id = ?
            WHERE user_id = ?
        ''', (voice_hash, user_id))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'message': 'Voice registered successfully'
        }
    
    except Exception as e:
        logger.error(f"Voice registration error: {str(e)}")
        return {'success': False, 'message': str(e)}


def verify_voice_id(user_id: int, audio_path: str, threshold: float = 0.9) -> Dict[str, Any]:
    """
    Verify user's voice against stored signature (mock implementation)
    
    Args:
        user_id: User ID
        audio_path: Path to audio file
        threshold: Similarity threshold (0-1)
    
    Returns:
        Verification result
    """
    try:
        # Get stored voice hash
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT voice_id FROM users WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result or not result['voice_id']:
            return {
                'success': False,
                'verified': False,
                'message': 'No voice signature registered'
            }
        
        stored_voice_hash = result['voice_id']
        
        # Generate hash from provided audio
        current_voice_hash = hash_voice_signature(audio_path)
        
        # Mock verification: In production, use actual voice biometric comparison
        # For demo purposes, we'll simulate a match
        # In real implementation, use voice recognition libraries like resemblyzer, speechbrain, etc.
        
        # Simulated similarity score (in production, calculate actual similarity)
        similarity = 0.95 if stored_voice_hash else 0.3
        
        verified = similarity >= threshold
        
        return {
            'success': True,
            'verified': verified,
            'similarity': similarity,
            'message': 'Voice verified successfully' if verified else 'Voice verification failed'
        }
    
    except Exception as e:
        logger.error(f"Voice verification error: {str(e)}")
        return {'success': False, 'verified': False, 'message': str(e)}


def generate_otp(user_id: int, length: int = 6) -> Dict[str, Any]:
    """
    Generate OTP for user
    
    Args:
        user_id: User ID
        length: OTP length (default 6)
    
    Returns:
        Generated OTP
    """
    try:
        # Generate random OTP
        otp = ''.join(random.choices(string.digits, k=length))
        
        # Store OTP in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        expires_at = (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO otps (user_id, otp, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, otp, expires_at))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Generated OTP for user {user_id}: {otp}")
        
        # In production, send OTP via SMS/Email
        # For demo, return in response
        return {
            'success': True,
            'otp': otp,  # In production, don't return this!
            'message': 'OTP generated and sent successfully',
            'expires_at': expires_at
        }
    
    except Exception as e:
        logger.error(f"OTP generation error: {str(e)}")
        return {'success': False, 'message': str(e)}


def verify_otp(user_id: int, otp: str) -> Dict[str, Any]:
    """
    Verify OTP
    
    Args:
        user_id: User ID
        otp: OTP to verify
    
    Returns:
        Verification result
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get latest unused OTP for user
        cursor.execute('''
            SELECT otp_id, otp, expires_at, used
            FROM otps
            WHERE user_id = ? AND used = 0
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return {
                'success': False,
                'verified': False,
                'message': 'No valid OTP found'
            }
        
        otp_id = result['otp_id']
        stored_otp = result['otp']
        expires_at = datetime.strptime(result['expires_at'], '%Y-%m-%d %H:%M:%S')
        
        # Check if OTP is expired
        if datetime.now() > expires_at:
            conn.close()
            return {
                'success': False,
                'verified': False,
                'message': 'OTP has expired'
            }
        
        # Verify OTP
        if otp == stored_otp:
            # Mark OTP as used
            cursor.execute('''
                UPDATE otps SET used = 1 WHERE otp_id = ?
            ''', (otp_id,))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'verified': True,
                'message': 'OTP verified successfully'
            }
        else:
            conn.close()
            return {
                'success': False,
                'verified': False,
                'message': 'Invalid OTP'
            }
    
    except Exception as e:
        logger.error(f"OTP verification error: {str(e)}")
        return {'success': False, 'verified': False, 'message': str(e)}


def encrypt_data(data: str, key: bytes = None) -> str:
    """
    Encrypt sensitive data using Fernet (symmetric encryption)
    """
    try:
        from cryptography.fernet import Fernet
        
        if not key:
            # In production, use a secure key management system
            key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
        
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data.decode()
    
    except ImportError:
        logger.warning("cryptography library not available")
        return data
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        return data


def decrypt_data(encrypted_data: str, key: bytes = None) -> str:
    """
    Decrypt sensitive data
    """
    try:
        from cryptography.fernet import Fernet
        
        if not key:
            key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
        
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    
    except ImportError:
        logger.warning("cryptography library not available")
        return encrypted_data
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return encrypted_data


if __name__ == '__main__':
    # Test security module
    print("--- Testing Security Module ---")
    
    # Test OTP generation
    otp_result = generate_otp(1)
    print(f"OTP Generation: {otp_result}")
    
    if otp_result['success']:
        # Test OTP verification
        verify_result = verify_otp(1, otp_result['otp'])
        print(f"OTP Verification: {verify_result}")
    
    # Test encryption
    try:
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        
        original = "Sensitive banking data"
        encrypted = encrypt_data(original, key)
        decrypted = decrypt_data(encrypted, key)
        
        print(f"\nOriginal: {original}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
    except ImportError:
        print("\ncryptography library not available for encryption test")

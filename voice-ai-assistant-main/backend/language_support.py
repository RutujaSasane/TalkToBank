"""
Multilingual Support Module for TalkToBank
Supports English, Hindi, Marathi, and Hinglish
"""
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Language detection patterns
LANGUAGE_PATTERNS = {
    'hindi': [
        r'[अ-ह]',  # Devanagari script
        r'\b(क्या|कैसे|कितना|बैलेंस|ट्रांसफर|लेनदेन|खाता)\b',
    ],
    'marathi': [
        r'[अ-ह]',  # Devanagari script (shared with Hindi)
        r'\b(काय|कसे|किती|शिल्लक|हस्तांतरण|व्यवहार|खाते)\b',
    ],
    'hinglish': [
        r'\b(kyunki|kyun|kya|kaise|kitna|balance|transfer|transaction)\b',
        r'\b(mere|tumhara|apka|hoga|hoga|kar|do|lo)\b',
    ]
}

# Translation mappings for common banking terms
BANKING_TRANSLATIONS = {
    'hindi': {
        'balance': 'शिल्लक',
        'transfer': 'ट्रांसफर',
        'transaction': 'लेनदेन',
        'account': 'खाता',
        'amount': 'राशि',
        'check': 'जांच',
        'show': 'दिखाएं',
        'last': 'अंतिम',
        'loan': 'ऋण',
        'interest': 'ब्याज',
    },
    'marathi': {
        'balance': 'शिल्लक',
        'transfer': 'हस्तांतरण',
        'transaction': 'व्यवहार',
        'account': 'खाते',
        'amount': 'रक्कम',
        'check': 'तपासा',
        'show': 'दाखवा',
        'last': 'शेवटचे',
        'loan': 'कर्ज',
        'interest': 'व्याज',
    }
}

# Response templates in different languages
RESPONSE_TEMPLATES = {
    'en': {
        'balance': "Your {account_type} account balance is ₹{balance:,.2f}.",
        'transfer_success': "Successfully transferred ₹{amount:,.2f} to {recipient}.",
        'transactions': "Here are your last {count} transactions.",
        'no_transactions': "You have no recent transactions.",
        'clarification': "I didn't understand. Could you please clarify?",
        'error': "Sorry, I encountered an error. Please try again.",
    },
    'hi': {
        'balance': "आपका {account_type} खाता शिल्लक ₹{balance:,.2f} है।",
        'transfer_success': "₹{amount:,.2f} {recipient} को सफलतापूर्वक ट्रांसफर किया गया।",
        'transactions': "यहां आपके अंतिम {count} लेनदेन हैं।",
        'no_transactions': "आपके पास कोई हालिया लेनदेन नहीं है।",
        'clarification': "मैं समझ नहीं पाया। कृपया स्पष्ट करें?",
        'error': "क्षमा करें, एक त्रुटि हुई। कृपया पुनः प्रयास करें।",
    },
    'mr': {
        'balance': "तुमचे {account_type} खाते शिल्लक ₹{balance:,.2f} आहे.",
        'transfer_success': "₹{amount:,.2f} {recipient} ला यशस्वीरित्या हस्तांतरित केले.",
        'transactions': "येथे तुमचे शेवटचे {count} व्यवहार आहेत.",
        'no_transactions': "तुमच्याकडे कोणतेही अलीकडील व्यवहार नाहीत.",
        'clarification': "मला समजले नाही. कृपया स्पष्ट करा?",
        'error': "क्षमा करा, एक त्रुटी आली. कृपया पुन्हा प्रयत्न करा.",
    }
}


def detect_language(text: str) -> str:
    """
    Detect language from text
    Returns: 'en', 'hi', 'mr', or 'hinglish'
    """
    text_lower = text.lower()
    
    # Check for Devanagari script (Hindi/Marathi)
    if re.search(r'[अ-ह]', text):
        # Try to distinguish Hindi vs Marathi (improved heuristic)
        hindi_indicators = ['क्या', 'कैसे', 'कितना', 'बैलेंस', 'ट्रांसफर', 'लेनदेन', 'खाता', 'मेरा', 'आपका', 'दिखाएं', 'बताओ']
        marathi_indicators = ['काय', 'कसे', 'किती', 'शिल्लक', 'हस्तांतरण', 'व्यवहार', 'खाते', 'माझे', 'तुमचे', 'दाखवा', 'सांगा', 'माझी', 'तुमची']
        
        hindi_count = sum(1 for word in hindi_indicators if word in text_lower)
        marathi_count = sum(1 for word in marathi_indicators if word in text_lower)
        
        # If Marathi indicators found, prioritize Marathi
        if marathi_count > 0:
            if marathi_count >= hindi_count:
                return 'mr'
        # If only Hindi indicators found, return Hindi
        if hindi_count > 0:
            return 'hi'
        # Default to Hindi if Devanagari but no clear indicators (most common)
        return 'hi'
    
    # Check for Hinglish patterns
    hinglish_patterns = [
        r'\b(kyunki|kyun|kya|kaise|kitna)\b',
        r'\b(mere|tumhara|apka|hoga|kar|do|lo)\b',
    ]
    for pattern in hinglish_patterns:
        if re.search(pattern, text_lower):
            return 'hinglish'
    
    # Default to English
    return 'en'


def translate_banking_term(term: str, target_lang: str) -> str:
    """
    Translate common banking terms
    """
    if target_lang in BANKING_TRANSLATIONS:
        return BANKING_TRANSLATIONS[target_lang].get(term.lower(), term)
    return term


def get_response_template(key: str, lang: str = 'en') -> str:
    """
    Get localized response template
    """
    if lang in RESPONSE_TEMPLATES and key in RESPONSE_TEMPLATES[lang]:
        return RESPONSE_TEMPLATES[lang][key]
    # Fallback to English
    return RESPONSE_TEMPLATES['en'].get(key, '')


def normalize_hinglish_to_english(text: str) -> str:
    """
    Convert Hinglish text to English for processing
    """
    # Common Hinglish to English mappings
    mappings = {
        'kyunki': 'because',
        'kyun': 'why',
        'kya': 'what',
        'kaise': 'how',
        'kitna': 'how much',
        'mere': 'my',
        'tumhara': 'your',
        'apka': 'your',
        'hoga': 'will be',
        'kar': 'do',
        'do': 'give',
        'lo': 'take',
        'balance': 'balance',
        'transfer': 'transfer',
        'transaction': 'transaction',
    }
    
    text_lower = text.lower()
    for hinglish, english in mappings.items():
        text_lower = text_lower.replace(hinglish, english)
    
    return text_lower


if __name__ == '__main__':
    # Test language detection
    test_texts = [
        "check my balance",
        "मेरा बैलेंस बताओ",
        "तुमचे शिल्लक दाखवा",
        "mere balance kya hai",
        "transfer 500 to Rohan",
    ]
    
    for text in test_texts:
        lang = detect_language(text)
        print(f"Text: {text}")
        print(f"Detected Language: {lang}")
        print()


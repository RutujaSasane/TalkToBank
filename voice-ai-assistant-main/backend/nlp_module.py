import re
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Try to import OpenAI, but make it optional
try:
    import openai
    OPENAI_AVAILABLE = True
    openai.api_key = os.getenv('OPENAI_API_KEY', '')
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available. Using pattern-based NLP only.")


def detect_intent_with_patterns(text: str) -> Dict[str, Any]:
    """
    Pattern-based intent detection (fallback method)
    """
    text = text.lower().strip()
    
    # Intent patterns - Comprehensive banking/financial knowledge base
    patterns = {
        'greeting': [
            r'^(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))\b',
            r'\b(hi|hello|hey)\s+(there|assistant|bot)\b',
        ],
        'help': [
            r'^(help|what\s+can\s+you\s+do|how\s+can\s+you\s+help)\b',
            r'\b(show|tell)\s+(me\s+)?(features|capabilities|options)\b',
            r'\bwhat\s+(are|is)\s+(your|the)\s+(features|services)\b',
        ],
        'thank_you': [
            r'\b(thank|thanks|thankyou|thx)\b',
            r'\bappreciate\s+it\b',
            r'\bthat\s+helps?\b',
        ],
        'check_balance': [
            r'\b(check|show|what|what\'s|whats|tell me)\b.*(balance|amount)',
            r'\bbalance\b',
            r'how much.*\b(have|got|do i have)\b',
            r'\bmy\s+(account|bank)\s+balance\b',
            r'\bcurrent\s+balance\b',
        ],
        'transfer_funds': [
            r'\b(transfer|send|pay|give)\b.*\b(money|rupees|₹|\d+)\b',
            r'\bsend\s+₹?\d+',
            r'\btransfer.*to\b',
            r'\bmake\s+a\s+payment\b',
            r'\bpay\s+someone\b',
            # Marathi/Hindi patterns for transfer
            r'हस्तांतरण',  # transfer (Marathi)
            r'ट्रांसफर',  # transfer (Hindi transliteration)
            r'भेज',  # send (Hindi)
            r'पाठव',  # send (Marathi)
        ],
        'transaction_history': [
            r'\b(show|display|get|view|check|see)\b.*(?:my\s+)?(?:last|recent)?\s*(?:transaction|history|statement|payment)',
            r'\b(show|display|get|view|check|see)\s+(?:me\s+)?(?:my\s+)?(?:last|recent)\s+\d+\s+(?:transaction|payment)',
            r'\blast\s+(?:my\s+)?\d+\s+(?:transaction|payment)',
            r'\brecent\s+(?:transaction|payment)',
            r'\bmy\s+(bank\s+)?statement\b',
            r'\btransaction\s+(?:history|details|list)\b',
            r'\bcheck\s+(?:my\s+)?(?:last|recent)\s+\d+\s+transaction',
            # Marathi/Hindi patterns for transactions
            r'व्यवहार',  # transactions (Marathi)
            r'लेनदेन',  # transactions (Hindi)
            r'दाखवा',  # show (Marathi)
            r'दिखाएं',  # show (Hindi)
            r'बताओ',  # tell (Hindi)
            r'शेवटचे',  # last (Marathi)
            r'अंतिम',  # last (Hindi)
            r'पिछले',  # recent (Hindi)
            r'माझे.*व्यवहार',  # my transactions (Marathi)
            r'मेरे.*लेनदेन',  # my transactions (Hindi)
        ],
        'loan_details': [
            r'\b(loan|emi|debt)\b',
            r'\binterest\s+rate\b',
            r'\bdue\s+date\b',
            r'\bhome\s+loan\b',
            r'\bpersonal\s+loan\b',
            r'\bloan\s+balance\b',
        ],
        'set_reminder': [
            r'\b(remind|reminder|alert)\b',
            r'\bremind\s+me\b',
            r'\bset\s+reminder\b',
        ],
        # Credit Card related
        'credit_card_info': [
            r'\bcredit\s+card\b',
            r'\bcard\s+(limit|balance|statement)\b',
            r'\boutstanding\s+(amount|balance)\b',
            r'\bcard\s+payment\s+due\b',
            r'\bminimum\s+payment\b',
        ],
        # Fixed Deposit / Investment
        'investment_info': [
            r'\bfixed\s+deposit\b',
            r'\bfd\s+(rate|interest)\b',
            r'\brecurring\s+deposit\b',
            r'\brd\s+account\b',
            r'\bmutual\s+fund\b',
            r'\binvestment\s+(portfolio|return)\b',
        ],
        # Account opening/management
        'account_services': [
            r'\bopen\s+(new\s+)?account\b',
            r'\bclose\s+account\b',
            r'\baccount\s+type\b',
            r'\bsavings\s+account\b',
            r'\bcurrent\s+account\b',
            r'\bupdate\s+(my\s+)?(mobile|email|address)\b',
        ],
        # Debit/ATM card services
        'card_services': [
            r'\bdebit\s+card\b',
            r'\batm\s+card\b',
            r'\bcard\s+(block|lost|stolen)\b',
            r'\brequest\s+(new\s+)?card\b',
            r'\bcard\s+pin\b',
            r'\batm\s+location\b',
        ],
        # Cheque services
        'cheque_services': [
            r'\bcheque\s+book\b',
            r'\brequest\s+cheque\b',
            r'\bcheque\s+status\b',
            r'\bstop\s+cheque\b',
            r'\bcheque\s+bounce\b',
        ],
        # Interest rates
        'interest_rates': [
            r'\binterest\s+rate\b',
            r'\bsavings\s+(account\s+)?interest\b',
            r'\bfd\s+rate\b',
            r'\bloan\s+(interest\s+)?rate\b',
            r'\bcurrent\s+rate\b',
        ],
        # Tax related
        'tax_info': [
            r'\btax\b',
            r'\btds\b',
            r'\bform\s+16\b',
            r'\bform\s+26as\b',
            r'\binterest\s+certificate\b',
            r'\btax\s+saving\b',
        ],
        # Insurance
        'insurance_info': [
            r'\binsurance\b',
            r'\blife\s+insurance\b',
            r'\bhealth\s+insurance\b',
            r'\binsurance\s+policy\b',
            r'\bpremium\s+payment\b',
        ],
        # UPI/Digital payments
        'digital_payment': [
            r'\bupi\b',
            r'\bupi\s+id\b',
            r'\bqr\s+code\b',
            r'\bdigital\s+payment\b',
            r'\bphone\s+pay\b',
            r'\bgoogle\s+pay\b',
        ],
        # NEFT/RTGS/IMPS
        'bank_transfer': [
            r'\bneft\b',
            r'\brtgs\b',
            r'\bimps\b',
            r'\bifsc\s+code\b',
            r'\bbeneficiary\b',
        ],
        # Bill payments
        'bill_payment': [
            r'\b(pay|payment)\s+(bill|bills)\b',
            r'\belectricity\s+bill\b',
            r'\bwater\s+bill\b',
            r'\bgas\s+bill\b',
            r'\bmobile\s+recharge\b',
            r'\bdth\s+recharge\b',
        ],
        # Account statements
        'statement_request': [
            r'\b(account|bank)\s+statement\b',
            r'\be-?statement\b',
            r'\bdownload\s+statement\b',
            r'\bmonthly\s+statement\b',
        ],
        # Financial advice
        'financial_advice': [
            r'\bfinancial\s+(advice|planning|help)\b',
            r'\bbudget\b',
            r'\bsaving\s+(money|plan)\b',
            r'\binvestment\s+advice\b',
            r'\bretirement\s+planning\b',
        ],
        # Account balance inquiry variants
        'balance_inquiry': [
            r'\bmin(imum)?\s+balance\b',
            r'\baverage\s+balance\b',
            r'\bavailable\s+balance\b',
            r'\btotal\s+balance\b',
        ],
        # Branch/Bank info
        'branch_info': [
            r'\bbranch\s+(location|near|address)\b',
            r'\bnearest\s+branch\b',
            r'\bbank\s+(hours|timing)\b',
            r'\bcustomer\s+(care|service|support)\b',
        ],
        # Forex/Currency
        'forex_info': [
            r'\bforeign\s+exchange\b',
            r'\bforex\b',
            r'\bcurrency\s+(exchange|rate)\b',
            r'\btravel\s+card\b',
        ],
        # Complaints/Disputes
        'complaint_dispute': [
            r'\bcomplaint\b',
            r'\bdispute\s+(transaction|charge)\b',
            r'\bunauthorized\s+(transaction|charge)\b',
            r'\bfraud\b',
            r'\breport\s+(issue|problem)\b',
        ],
    }
    
    # Detect intent
    detected_intent = 'unknown'
    for intent, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, text):
                detected_intent = intent
                break
        if detected_intent != 'unknown':
            break
    
    # Extract entities
    entities = {}
    
    # Extract amount (for transfers)
    amount_match = re.search(r'₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)', text)
    if amount_match:
        amount_str = amount_match.group(1).replace(',', '')
        try:
            entities['amount'] = float(amount_str)
        except ValueError:
            pass
    
    # Extract recipient name (for transfers)
    # Look for "to [name]" or "send [name]"
    recipient_patterns = [
        r'\bto\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'\bsend\s+(?:₹?\d+\s+)?to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
    ]
    for pattern in recipient_patterns:
        recipient_match = re.search(pattern, text, re.IGNORECASE)
        if recipient_match:
            entities['recipient'] = recipient_match.group(1).title()
            break
    
    # Extract transaction limit
    limit_patterns = [
        r'\b(?:last|recent)\s+(?:my\s+)?(\d+)\s+(?:transaction|payment|statement)',
        r'\b(?:last|recent)\s+(\d+)',
        r'\b(\d+)\s+(?:transaction|payment|statement)',
        r'\bshow\s+(?:me\s+)?(?:my\s+)?(?:last\s+)?(\d+)\s+(?:transaction|payment)',
    ]
    for pattern in limit_patterns:
        limit_match = re.search(pattern, text, re.IGNORECASE)
        if limit_match:
            try:
                entities['limit'] = int(limit_match.group(1))
                break
            except (ValueError, IndexError):
                pass
    
    # Extract account type
    if 'savings' in text:
        entities['account_type'] = 'savings'
    elif 'current' in text or 'checking' in text:
        entities['account_type'] = 'current'
    
    # Extract reminder message
    if detected_intent == 'set_reminder':
        reminder_patterns = [
            r'remind\s+me\s+to\s+(.+?)(?:\s+(?:on|by|next|tomorrow)|\s*$)',
            r'reminder\s+(?:to\s+)?(.+?)(?:\s+(?:on|by|next|tomorrow)|\s*$)',
        ]
        for pattern in reminder_patterns:
            reminder_match = re.search(pattern, text, re.IGNORECASE)
            if reminder_match:
                entities['message'] = reminder_match.group(1).strip()
                break
        
        # Extract due date
        date_patterns = [
            r'(?:on|by)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
            r'(?:on|by)\s+(\d{1,2}(?:st|nd|rd|th)?)',
            r'(tomorrow|next\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday))',
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, text, re.IGNORECASE)
            if date_match:
                entities['due_date'] = date_match.group(1)
                break
    
    return {
        'intent': detected_intent,
        'entities': entities,
        'confidence': 0.8 if detected_intent != 'unknown' else 0.3
    }


def detect_intent_with_openai(text: str) -> Dict[str, Any]:
    """
    Use OpenAI GPT for more sophisticated intent detection
    """
    try:
        prompt = f"""You are a banking assistant NLP system. Analyze the following user query and respond with a JSON object containing:
- intent: one of [check_balance, transfer_funds, transaction_history, loan_details, set_reminder, credit_card_info, investment_info, account_services, card_services, cheque_services, interest_rates, tax_info, insurance_info, digital_payment, bank_transfer, bill_payment, statement_request, financial_advice, balance_inquiry, branch_info, forex_info, complaint_dispute, unknown]
- entities: an object with relevant extracted information (amount, recipient, account_type, limit, message, due_date)
- confidence: a score between 0 and 1

User query: "{text}"

Response (JSON only):"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a JSON-only NLP parser for banking queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        import json
        result = json.loads(result_text)
        
        return result
    
    except Exception as e:
        logger.error(f"OpenAI intent detection error: {str(e)}")
        # Fall back to pattern-based detection
        return detect_intent_with_patterns(text)


def detect_intent(text: str) -> Dict[str, Any]:
    """
    Main intent detection function
    Uses OpenAI if available, otherwise falls back to pattern matching
    """
    if OPENAI_AVAILABLE and openai.api_key:
        try:
            return detect_intent_with_openai(text)
        except Exception as e:
            logger.warning(f"OpenAI detection failed, using patterns: {str(e)}")
    
    return detect_intent_with_patterns(text)


if __name__ == '__main__':
    # Test the NLP module
    test_queries = [
        "Check my balance",
        "Transfer 500 to Rohan",
        "Show my last 3 transactions",
        "What's my loan interest rate?",
        "Remind me to pay EMI next Monday",
    ]
    
    for query in test_queries:
        result = detect_intent(query)
        print(f"\nQuery: {query}")
        print(f"Result: {result}")

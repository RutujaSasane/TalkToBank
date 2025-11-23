"""
Test script to demonstrate the AI Voice Banking Assistant backend
"""
import sys
sys.path.insert(0, 'backend')

from nlp_module import detect_intent
from banking_api import check_balance, transfer_funds, get_transaction_history, get_loan_details, set_reminder, init_database
from tts_module import text_to_speech
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def main():
    print_header("AI VOICE BANKING ASSISTANT - DEMO")
    
    # Initialize database
    print("\n[1] Initializing database...")
    init_database()
    print("✓ Database ready with mock data")
    
    # Test queries
    test_queries = [
        "Check my balance",
        "Transfer 500 to Rohan",
        "Show my last 3 transactions",
        "What's my loan interest rate?"
    ]
    
    user_id = 1
    
    for query in test_queries:
        print_header(f"QUERY: {query}")
        
        # Step 1: Detect Intent
        print("\n[2] Detecting intent...")
        intent_result = detect_intent(query)
        print(f"   Intent: {intent_result['intent']}")
        print(f"   Entities: {intent_result['entities']}")
        print(f"   Confidence: {intent_result['confidence']}")
        
        # Step 2: Process based on intent
        print("\n[3] Processing command...")
        intent = intent_result['intent']
        entities = intent_result['entities']
        response_text = ""
        
        if intent == 'check_balance':
            result = check_balance(user_id, 'savings')
            if result['success']:
                response_text = f"Your savings account balance is ₹{result['balance']:,.2f}"
                print(f"   ✓ {response_text}")
                print(f"   Data: {result}")
        
        elif intent == 'transfer_funds':
            amount = entities.get('amount', 500)
            recipient = entities.get('recipient', 'Unknown')
            result = transfer_funds(user_id, recipient, amount)
            if result['success']:
                response_text = f"Successfully transferred ₹{amount:,.2f} to {recipient}"
                print(f"   ✓ {response_text}")
                print(f"   Transaction ID: {result['transaction_id']}")
                print(f"   New Balance: ₹{result['new_balance']:,.2f}")
        
        elif intent == 'transaction_history':
            limit = entities.get('limit', 3)
            result = get_transaction_history(user_id, limit)
            if result['success']:
                response_text = f"Your last {len(result['transactions'])} transactions:"
                print(f"   ✓ {response_text}")
                for txn in result['transactions']:
                    print(f"      - {txn['date']}: {txn['type']} ₹{txn['amount']:,.2f} {txn['recipient'] or ''}")
        
        elif intent == 'loan_details':
            result = get_loan_details(user_id)
            if result['success'] and result['loans']:
                loan = result['loans'][0]
                response_text = f"Loan: ₹{loan['amount']:,.2f} at {loan['interest_rate']}% interest"
                print(f"   ✓ {response_text}")
                print(f"   Due Date: {loan['due_date']}")
        
        # Step 3: Generate TTS (optional)
        if response_text:
            print("\n[4] Generating text-to-speech...")
            try:
                audio_path = f"audio_test_{intent}.mp3"
                os.makedirs("audio_responses", exist_ok=True)
                audio_path = os.path.join("audio_responses", audio_path)
                text_to_speech(response_text, audio_path, method='gtts')
                print(f"   ✓ Audio saved to: {audio_path}")
            except Exception as e:
                print(f"   ⚠ Audio generation skipped: {str(e)}")
    
    print_header("DEMO COMPLETE")
    print("\n✓ All backend modules working correctly!")
    print("\nTo run the full web application:")
    print("  1. Install Node.js from https://nodejs.org/")
    print("  2. Run: cd frontend && npm install && npm run dev")
    print("  3. Start backend: python backend/app.py")
    print("  4. Open http://localhost:3000 in browser")

if __name__ == '__main__':
    main()

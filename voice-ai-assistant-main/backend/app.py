from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime
import logging

from nlp_module import detect_intent
from stt_module import speech_to_text
from tts_module import text_to_speech
from banking_api import (
    check_balance, 
    transfer_funds, 
    get_transaction_history,
    get_loan_details,
    set_reminder,
    get_all_accounts,
    get_cards,
    get_investments,
    get_payments_summary
)
from security_module import verify_voice_id, generate_otp, verify_otp
from knowledge_base import get_response as get_knowledge_response
from language_support import detect_language, get_response_template, normalize_hinglish_to_english
from conversation_context import get_conversation_context

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'audio_responses'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route('/api/stt', methods=['POST'])
def speech_to_text_endpoint():
    """Convert speech to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        
        # Save audio temporarily
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
        audio_file.save(audio_path)
        # Optional language parameter from client
        language = request.form.get('language') or None

        # Convert speech to text (pass language to STT backend if provided)
        text = speech_to_text(audio_path, language=language)
        
        # Clean up
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return jsonify({"text": text})
    
    except Exception as e:
        logger.error(f"STT Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_command():
    """Main endpoint to process user commands with multilingual and context support"""
    try:
        data = request.json
        user_text = data.get('text', '')
        user_id = data.get('user_id', 1)  # Default user for demo
        
        if not user_text:
            return jsonify({"error": "No text provided"}), 400
        
        logger.info(f"Processing command: {user_text}")
        
        # Get conversation context
        context = get_conversation_context(user_id)
        
        # Detect language (incoming) and allow response language override
        detected_lang = detect_language(user_text)
        context.language = detected_lang
        logger.info(f"Detected language: {detected_lang}")

        # Allow client to request a specific response language (force output language)
        response_lang = data.get('response_language') or detected_lang
        logger.info(f"Response language requested: {response_lang}")
        
        # Normalize text for processing (NLP patterns are in English)
        processed_text = user_text
        if detected_lang == 'hinglish':
            processed_text = normalize_hinglish_to_english(user_text)
            logger.info(f"Normalized Hinglish text: {processed_text}")
        elif detected_lang in ['hi', 'mr']:
            # For Hindi/Marathi, try to extract key English words or use translation
            # For now, pass as-is since patterns can match Devanagari script
            # The intent detection will work with the patterns we added
            processed_text = user_text
            logger.info(f"Processing {detected_lang} text: {processed_text}")
        
        # Detect intent and extract entities
        intent_result = detect_intent(processed_text)
        intent = intent_result['intent']
        entities = intent_result['entities']
        
        # Enhance entities from conversation context
        entities = context.enhance_entities_from_context(intent, entities)
        
        logger.info(f"Detected intent: {intent}, Entities: {entities}")
        
        # Check if clarification is needed
        needs_clarification, clarification_msg = context.needs_clarification(intent, entities)
        if needs_clarification:
            # Get localized clarification message using requested response language
            if response_lang != 'en':
                clarification_msg = get_response_template('clarification', response_lang) or clarification_msg
            
            # Add user message to context
            context.add_message('user', user_text, intent, entities)
            context.add_message('assistant', clarification_msg, intent, entities)
            
            # Generate audio response
            audio_filename = f"response_{datetime.now().timestamp()}.mp3"
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
            try:
                # Use appropriate language for TTS based on response language
                lang_code = 'hi' if response_lang == 'hi' else ('mr' if response_lang == 'mr' else 'en')
                text_to_speech(clarification_msg, audio_path, lang=lang_code)
            except:
                text_to_speech(clarification_msg, audio_path)  # Fallback to default
            
            return jsonify({
                "text": clarification_msg,
                "intent": intent,
                "needs_clarification": True,
                "audio_url": f"/api/audio/{audio_filename}",
                "data": {}
            })
        
        # Process based on intent
        response_text = ""
        data_payload = {}
        
        try:
            if intent == 'check_balance':
                account_type = entities.get('account_type', 'savings')
                result = check_balance(user_id, account_type)
                if result['success']:
                    # Use the requested response language for templates
                    template = get_response_template('balance', response_lang)
                    if template:
                        response_text = template.format(account_type=account_type, balance=result['balance'])
                    else:
                        response_text = f"Your {account_type} account balance is ₹{result['balance']:,.2f}."
                    data_payload = result
                else:
                    error_template = get_response_template('error', response_lang)
                    response_text = error_template or result.get('message', 'Unable to fetch balance.')
            
            elif intent == 'transfer_funds':
                amount = entities.get('amount')
                recipient = entities.get('recipient')
                
                if not amount or not recipient:
                    clarification_template = get_response_template('clarification', response_lang)
                    response_text = clarification_template or "Please specify the amount and recipient for the transfer."
                else:
                    result = transfer_funds(user_id, recipient, amount)
                    if result['success']:
                        template = get_response_template('transfer_success', response_lang)
                        if template:
                            response_text = template.format(amount=amount, recipient=recipient)
                        else:
                            response_text = f"Successfully transferred ₹{amount:,.2f} to {recipient}. Transaction ID: {result['transaction_id']}."
                        data_payload = result
                        context.clear_pending_entities()  # Clear after successful operation
                    else:
                        error_template = get_response_template('error', response_lang)
                        response_text = error_template or result.get('message', 'Transfer failed.')
            
            elif intent == 'transaction_history':
                limit = entities.get('limit', 5)
                result = get_transaction_history(user_id, limit)
                if result['success']:
                    transactions = result['transactions']
                    if transactions:
                        template = get_response_template('transactions', response_lang)
                        if template:
                            response_text = template.format(count=len(transactions))
                        else:
                            response_text = f"Here are your last {len(transactions)} transactions."
                        # Keep structured data for frontend table rendering
                        data_payload = result
                    else:
                        template = get_response_template('no_transactions', response_lang)
                        response_text = template or "You have no recent transactions."
                        data_payload = result
                else:
                    error_template = get_response_template('error', response_lang)
                    response_text = error_template or result.get('message', 'Unable to fetch transaction history.')
                    data_payload = {}
            
            elif intent == 'loan_details':
                result = get_loan_details(user_id)
                if result['success']:
                    loans = result['loans']
                    if loans:
                        loan = loans[0]  # Get first loan
                        response_text = f"Your loan amount is ₹{loan['amount']:,.2f} with an interest rate of {loan['interest_rate']}% per annum. Due date: {loan['due_date']}."
                    else:
                        response_text = "You have no active loans."
                    data_payload = result
                else:
                    error_template = get_response_template('error', response_lang)
                    response_text = error_template or result.get('message', 'Unable to fetch loan details.')
            
            elif intent == 'set_reminder':
                message = entities.get('message')
                due_date = entities.get('due_date')
                
                if not message:
                    clarification_template = get_response_template('clarification', detected_lang)
                    response_text = clarification_template or "Please specify what you'd like to be reminded about."
                else:
                    result = set_reminder(user_id, message, due_date)
                    if result['success']:
                        response_text = f"Reminder set: {message}"
                        if due_date:
                            response_text += f" on {due_date}"
                        data_payload = result
                    else:
                        error_template = get_response_template('error', response_lang)
                        response_text = error_template or result.get('message', 'Unable to set reminder.')
            
            else:
                # Check knowledge base for other banking queries
                kb_response = get_knowledge_response(intent, response_lang)
                if kb_response['success']:
                    response_text = kb_response['response']
                    data_payload = {'tips': kb_response['tips']}
                else:
                    response_text = kb_response['response']  # Default help message
            
            # Add messages to conversation context
            context.add_message('user', user_text, intent, entities)
            context.add_message('assistant', response_text, intent, entities)
            
        except Exception as e:
            logger.error(f"Error processing intent {intent}: {str(e)}")
            error_template = get_response_template('error', response_lang)
            response_text = error_template or f"Sorry, I encountered an error: {str(e)}. Please try again."
        
        # Generate audio response with appropriate language
        audio_filename = f"response_{datetime.now().timestamp()}.mp3"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        try:
            # Use appropriate language for TTS based on requested response language
            lang_code = 'hi' if response_lang == 'hi' else ('mr' if response_lang == 'mr' else 'en')
            text_to_speech(response_text, audio_path, lang=lang_code)
        except Exception as e:
            logger.warning(f"TTS error, using default: {str(e)}")
            text_to_speech(response_text, audio_path)  # Fallback to default
        
        return jsonify({
            "text": response_text,
            "intent": intent,
            "language": response_lang,
            "audio_url": f"/api/audio/{audio_filename}",
            "data": data_payload
        })
    
    except Exception as e:
        logger.error(f"Process Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """Serve audio files"""
    try:
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/mpeg')
        else:
            return jsonify({"error": "Audio file not found"}), 404
    except Exception as e:
        logger.error(f"Audio Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/verify_voice', methods=['POST'])
def verify_voice():
    """Verify user voice for authentication"""
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        user_id = request.form.get('user_id', 1)
        audio_file = request.files['audio']
        
        # Save audio temporarily
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'voice_verify.wav')
        audio_file.save(audio_path)
        
        # Verify voice
        result = verify_voice_id(user_id, audio_path)
        
        # Clean up
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Voice Verification Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate_otp', methods=['POST'])
def generate_otp_endpoint():
    """Generate OTP for transaction verification"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        
        result = generate_otp(user_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"OTP Generation Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/verify_otp', methods=['POST'])
def verify_otp_endpoint():
    """Verify OTP"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        otp = data.get('otp', '')
        
        result = verify_otp(user_id, otp)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"OTP Verification Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/user/<int:user_id>/summary', methods=['GET'])
def get_user_summary(user_id):
    """Get user account summary"""
    try:
        balance_result = check_balance(user_id, 'savings')
        loan_result = get_loan_details(user_id)
        transaction_result = get_transaction_history(user_id, 5)
        
        summary = {
            "user_id": user_id,
            "balance": balance_result.get('balance', 0) if balance_result['success'] else 0,
            "loans": loan_result.get('loans', []) if loan_result['success'] else [],
            "recent_transactions": transaction_result.get('transactions', []) if transaction_result['success'] else []
        }
        
        return jsonify({"success": True, "summary": summary})
    
    except Exception as e:
        logger.error(f"Summary Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/financial_advice', methods=['POST'])
def get_financial_advice_endpoint():
    """Get AI-powered financial advice"""
    try:
        data = request.json
        query = data.get('query', '')
        user_id = data.get('user_id', 1)
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        # Import financial advisor
        from financial_advisor import get_ai_financial_advice
        
        # Get user financial data
        balance_result = check_balance(user_id, 'savings')
        transaction_result = get_transaction_history(user_id, 10)
        loan_result = get_loan_details(user_id)
        
        context = {
            'balance': balance_result.get('balance', 0) if balance_result.get('success') else 0,
            'recent_transactions': transaction_result.get('transactions', []) if transaction_result.get('success') else [],
            'loans': loan_result.get('loans', []) if loan_result.get('success') else []
        }
        
        advice = get_ai_financial_advice(query, context)
        
        return jsonify({
            "success": True,
            "advice": advice,
            "query": query
        })
    
    except Exception as e:
        logger.error(f"Financial Advice Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/financial_health/<int:user_id>', methods=['GET'])
def get_financial_health_endpoint(user_id):
    """Get financial health score and recommendations"""
    try:
        from financial_advisor import calculate_financial_health_score, analyze_spending_patterns
        
        # Get user data
        balance_result = check_balance(user_id, 'savings')
        transaction_result = get_transaction_history(user_id, 30)
        loan_result = get_loan_details(user_id)
        
        balance = balance_result.get('balance', 0) if balance_result.get('success') else 0
        transactions = transaction_result.get('transactions', []) if transaction_result.get('success') else []
        loans = loan_result.get('loans', []) if loan_result.get('success') else []
        
        # Prepare user data for health score calculation
        user_data = {
            'balance': balance,
            'monthly_income': 40000,  # Mock value
            'loans': loans,
            'transactions': transactions
        }
        
        # Calculate health score
        health_data = calculate_financial_health_score(user_data)
        
        # Get spending patterns
        spending_data = analyze_spending_patterns(transactions)
        
        return jsonify({
            "success": True,
            "health": health_data,
            "spending": spending_data
        })
    
    except Exception as e:
        logger.error(f"Financial Health Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/accounts/<int:user_id>', methods=['GET'])
def get_accounts_endpoint(user_id):
    """Get all accounts for a user"""
    try:
        result = get_all_accounts(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Accounts Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/payments/<int:user_id>', methods=['GET'])
def get_payments_endpoint(user_id):
    """Get payments summary for a user"""
    try:
        result = get_payments_summary(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Payments Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/cards/<int:user_id>', methods=['GET'])
def get_cards_endpoint(user_id):
    """Get all cards for a user"""
    try:
        result = get_cards(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Cards Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/loans/<int:user_id>', methods=['GET'])
def get_loans_endpoint(user_id):
    """Get all loans for a user"""
    try:
        result = get_loan_details(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Loans Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/investments/<int:user_id>', methods=['GET'])
def get_investments_endpoint(user_id):
    """Get all investments for a user"""
    try:
        result = get_investments(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Investments Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload_document', methods=['POST'])
def upload_document_endpoint():
    """Upload and analyze document (bill, receipt, statement)"""
    try:
        if 'document' not in request.files:
            return jsonify({"error": "No document provided"}), 400
        
        document = request.files['document']
        user_id = request.form.get('user_id', 1)
        
        if document.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save document temporarily
        file_ext = document.filename.rsplit('.', 1)[1].lower() if '.' in document.filename else ''
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_doc_{user_id}.{file_ext}')
        document.save(temp_path)
        
        # Import document intelligence
        from document_intelligence import (
            extract_text_from_image,
            extract_text_from_pdf,
            analyze_bill,
            extract_actionable_insights
        )
        
        # Extract text based on file type
        if file_ext in ['jpg', 'jpeg', 'png']:
            text = extract_text_from_image(temp_path)
        elif file_ext == 'pdf':
            text = extract_text_from_pdf(temp_path)
        else:
            os.remove(temp_path)
            return jsonify({"error": "Unsupported file format"}), 400
        
        # Analyze document
        analysis = analyze_bill(text)
        insights = extract_actionable_insights(analysis)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "data": analysis,
            "insights": insights,
            "filename": document.filename
        })
    
    except Exception as e:
        logger.error(f"Document Upload Error: {str(e)}")
        # Clean up on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Initialize database on startup
    from banking_api import init_database
    init_database()
    
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)

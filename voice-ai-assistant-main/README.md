# TalkToBank — Voice AI Banking Assistant

This repository contains a voice-enabled AI assistant demo for banking-related tasks. It includes a Flask backend that provides STT/response/TTS endpoints and a single-file frontend UI that demonstrates voice input, multilingual settings, and chat-style responses.

---

## 🎯 **Project Overview**

## ✨ **Key Features**

- ✅ **Voice-to-Text (STT)** - Google Speech Recognition or OpenAI Whisper with multilingual support
- ✅ **NLP Intent + Entity Extraction** - Pattern-based and GPT-powered intent detection
- ✅ **Balance Check Operation** - Real-time account balance queries
- ✅ **Fund Transfer Operation** - Secure money transfers with validation
- ✅ **Transaction History View** - Tabular display of recent transactions
- ✅ **Loan/Interest/Credit Inquiry** - Comprehensive loan information
- ✅ **Text-to-Speech (TTS)** - Multilingual voice responses (gTTS/ElevenLabs)
- ✅ **Context-Aware Conversation** - Maintains conversation history for better understanding
- ✅ **Error Handling + Clarification Prompts** - Intelligent error recovery and user guidance
- ✅ **Mock Secure Authentication** - Voice ID and OTP verification
- ✅ **Reminder/Alert System** - Set and manage financial reminders
- ✅ **Multilingual Support** - English, Hindi, Marathi, and Hinglish
- ✅ **Clean Voice UI** - Modern interface with mic button, chat bubbles, audio playback
- ✅ **Backend API Integration** - SQLite database with mock banking data

---

## 📁 **Project Structure**

```
ai_voice_assistant/
│
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── nlp_module.py            # Intent detection & entity extraction
│   ├── stt_module.py            # Speech-to-text conversion (multilingual)
│   ├── tts_module.py            # Text-to-speech generation (multilingual)
│   ├── banking_api.py           # Banking operations & database
│   ├── security_module.py       # Voice verification & OTP
│   ├── language_support.py      # Multilingual support (EN/HI/MR/Hinglish)
│   ├── conversation_context.py  # Context-aware conversation management
│   ├── knowledge_base.py        # Banking knowledge base
│   ├── financial_advisor.py     # AI financial advice
│   ├── document_intelligence.py # Document OCR and analysis
│   ├── requirements.txt         # Python dependencies
│   └── database.db              # SQLite database (auto-generated)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceRecorder.js   # Voice input & text input
│   │   │   ├── ChatBubble.js      # Message display component
│   │   │   ├── Loader.js          # Loading indicator
│   │   │   └── AccountSummary.js  # Sidebar account overview
│   │   ├── App.js                 # Main React application
│   │   ├── api.js                 # API client functions
│   │   ├── main.jsx               # React entry point
│   │   └── styles.css             # Complete styling
│   ├── index.html                 # HTML template
│   ├── package.json               # Node dependencies
│   └── vite.config.js             # Vite configuration
│
└── README.md                      # This file
```

---

## ⚙️ **Tech Stack**

| Component          | Technology                          |
|--------------------|-------------------------------------|
| **Frontend**       | React.js 18, Vite                   |
| **Backend**        | Python 3.8+, Flask                  |
| **NLP**            | OpenAI GPT / Pattern Matching       |
| **Speech-to-Text** | Whisper API / Google Speech API     |
| **Text-to-Speech** | gTTS / ElevenLabs                   |
| **Database**       | SQLite                              |
| **Authentication** | Voice ID (mock) / OTP               |
| **Deployment**     | Render (backend) + Vercel (frontend)|

---

## 🚀 **Quick Start**

### **Prerequisites**

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### **1. Clone the Repository**

```bash
cd ai_voice_assistant
```

### **2. Backend Setup**

#### **Install Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

#### **Configure Environment Variables**

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Optional - for better NLP and STT
OPENAI_API_KEY=your_openai_api_key_here

# Optional - for premium TTS
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional - for encryption
ENCRYPTION_KEY=your_encryption_key_here
```

> **Note:** The application works without API keys using free alternatives:
> - Pattern-based NLP (no OpenAI needed)
> - Google Speech Recognition (free)
> - gTTS (free)

#### **Initialize Database**

The database will be auto-created on first run, but you can test it:

```bash
python banking_api.py
```

#### **Run Backend Server**

```bash
python app.py
```

Server will start at `http://localhost:5001`

### **3. Frontend Setup**

#### **Install Dependencies**

```bash
cd ../frontend
npm install
```

#### **Configure API URL (Optional)**

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:5001
```

#### **Run Development Server**

```bash
npm run dev
```

Frontend is a single HTML file - just open `index.html` in your browser, or use a simple HTTP server:
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server
```
Then open `http://localhost:8000` in your browser.

---

## 🎤 **How to Use**

### **Comprehensive Banking Knowledge Base**

This assistant can answer **hundreds of banking and financial queries** across **20+ categories**:

#### **1. Account Management**
- Check balance, transaction history, statements
- Minimum balance requirements
- Account opening/closing procedures
- Update mobile/email/address

**Example Queries:**
- "What's my current balance?"
- "Show my last 10 transactions"
- "How do I open a savings account?"
- "What's the minimum balance for metro branches?"

#### **2. Fund Transfers & Payments**
- Transfer funds between accounts
- NEFT, RTGS, IMPS details
- UPI and digital payments
- Bill payments (electricity, water, mobile)

**Example Queries:**
- "Transfer 500 to Rohan"
- "How does RTGS work?"
- "What's the UPI transaction limit?"
- "How to pay electricity bill?"

#### **3. Cards (Credit & Debit)**
- Credit card limits and payments
- Debit/ATM card services
- Card blocking and replacement
- PIN change procedures

**Example Queries:**
- "What's my credit card limit?"
- "How to block lost card?"
- "Find nearest ATM"
- "What's the minimum credit card payment?"

#### **4. Loans & EMI**
- Home, personal, car, education loans
- Interest rates
- EMI calculations
- Loan prepayment

**Example Queries:**
- "What's my loan balance?"
- "Current home loan interest rates?"
- "When is my EMI due?"

#### **5. Investments & Deposits**
- Fixed deposits (FD)
- Recurring deposits (RD)
- Mutual funds
- Investment advice

**Example Queries:**
- "What's the FD interest rate?"
- "How to open recurring deposit?"
- "Tell me about mutual funds"

#### **6. Tax & Documents**
- TDS information
- Form 16, Form 26AS
- Interest certificates
- Tax saving options

**Example Queries:**
- "How to get Form 26AS?"
- "What's TDS on fixed deposits?"
- "Tax saving investment options?"

#### **7. Insurance**
- Life and health insurance
- Premium payments
- Claim procedures

**Example Queries:**
- "How much life insurance do I need?"
- "How to file insurance claim?"

#### **8. Cheque Services**
- Cheque book requests
- Stop cheque payments
- Cheque bounce procedures

**Example Queries:**
- "How to request cheque book?"
- "Stop payment on cheque"

#### **9. Branch & Customer Service**
- Branch locations and timings
- Customer care contacts
- Service requests

**Example Queries:**
- "Nearest branch location?"
- "Bank customer care number?"
- "Branch working hours?"

#### **10. Foreign Exchange**
- Currency exchange rates
- Travel cards
- International remittance

**Example Queries:**
- "Current USD exchange rate?"
- "How to get forex card?"

#### **11. Financial Planning**
- Budgeting tips
- Savings strategies
- Retirement planning
- Investment advice

**Example Queries:**
- "How to create a budget?"
- "Retirement planning tips?"
- "Best investment strategy?"

#### **12. Complaints & Disputes**
- File complaints
- Dispute transactions
- Fraud reporting
- Banking Ombudsman

**Example Queries:**
- "How to file complaint?"
- "Report unauthorized transaction"
- "Dispute a charge"

### **Supported Voice Commands (Core Transactions)**

| Intent               | Example Commands                                      |
|----------------------|-------------------------------------------------------|
| **Check Balance**    | "Check my balance", "What's my account balance?"      |
| **Transfer Funds**   | "Transfer 500 to Rohan", "Send ₹1000 to Priya"       |
| **Transaction History** | "Show my last 5 transactions", "Recent payments"   |
| **Loan Details**     | "What's my loan interest rate?", "Loan details"       |
| **Set Reminder**     | "Remind me to pay EMI next Monday"                    |

### **Using the Application**

1. **Voice Input**: Click the 🎤 microphone button, speak your command, then click ⏹️ to stop
2. **Text Input**: Type your command in the text box and press Enter or click 📤
3. **Audio Response**: The assistant will respond with both text and voice

---

## 🗄️ **Database Schema**

### **Users Table**
- `user_id` (PRIMARY KEY)
- `name`
- `email`
- `voice_id` (for voice authentication)

### **Accounts Table**
- `account_id` (PRIMARY KEY)
- `user_id` (FOREIGN KEY)
- `account_type` (savings/current)
- `balance`

### **Transactions Table**
- `txn_id` (PRIMARY KEY)
- `account_id` (FOREIGN KEY)
- `amount`
- `type` (credit/debit)
- `recipient`
- `date`

### **Loans Table**
- `loan_id` (PRIMARY KEY)
- `user_id` (FOREIGN KEY)
- `amount`
- `interest_rate`
- `due_date`

### **Reminders Table**
- `reminder_id` (PRIMARY KEY)
- `user_id` (FOREIGN KEY)
- `message`
- `due_date`

---

## 🔌 **API Endpoints**

### **Backend API Routes**

| Endpoint                    | Method | Description                    |
|-----------------------------|--------|--------------------------------|
| `/health`                   | GET    | Health check                   |
| `/api/stt`                  | POST   | Speech to text conversion      |
| `/api/process`              | POST   | Process user command           |
| `/api/audio/<filename>`     | GET    | Serve TTS audio file           |
| `/api/verify_voice`         | POST   | Voice authentication           |
| `/api/generate_otp`         | POST   | Generate OTP                   |
| `/api/verify_otp`           | POST   | Verify OTP                     |
| `/api/user/<id>/summary`    | GET    | Get account summary            |

### **Example API Request**

```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Check my balance", "user_id": 1}'
```

**Response:**
```json
{
  "text": "Your savings account balance is ₹25,430.50.",
  "intent": "check_balance",
  "audio_url": "/api/audio/response_1234567890.mp3",
  "data": {
    "success": true,
    "balance": 25430.50,
    "account_type": "savings"
  }
}
```

---

## 🌐 **Deployment**

### **Backend Deployment (Render)**

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add environment variables:
   - `OPENAI_API_KEY`
   - `ELEVENLABS_API_KEY`
5. Deploy

### **Frontend Deployment (Vercel)**

1. Install Vercel CLI: `npm install -g vercel`
2. Run: `vercel` in the `frontend` directory
3. Set environment variable:
   - `VITE_API_BASE_URL=https://your-render-app.onrender.com`
4. Deploy

---

## 🧪 **Testing**

### **Test Backend Modules**

```bash
cd backend

# Test NLP module
python nlp_module.py

# Test Banking API
python banking_api.py

# Test Security module
python security_module.py
```

### **Test API Endpoints**

```bash
# Health check
curl http://localhost:5000/health

# Process command
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Check my balance", "user_id": 1}'
```

---

## 🔐 **Security Features**

1. **Voice Biometric Authentication** (mock implementation)
   - Stores voice hash for user verification
   - Can be enhanced with real voice recognition libraries

2. **OTP Verification**
   - Time-limited OTPs (5-minute expiry)
   - One-time use only

3. **Data Encryption**
   - Uses Fernet symmetric encryption for sensitive data
   - Configurable encryption key

4. **Secure API Communication**
   - CORS enabled for frontend-backend communication
   - Input validation and error handling

---

## 🎨 **Features**

### **Frontend**
- ✅ Real-time voice recording and transcription
- ✅ Text and voice input options
- ✅ Dark/Light mode toggle
- ✅ Account summary sidebar
- ✅ Transaction history display
- ✅ Responsive design for mobile/desktop
- ✅ Audio playback of responses

### **Backend**
- ✅ Intent detection with entity extraction
- ✅ Multiple STT providers (Whisper/Google)
- ✅ Multiple TTS providers (gTTS/ElevenLabs)
- ✅ SQLite database with mock data
- ✅ RESTful API architecture
- ✅ Comprehensive error handling
- ✅ Logging and debugging

---

## 🌍 **Multilingual Support**

TalkToBank supports **4 languages**:

- **English**: "Check my balance", "Transfer 500 to Rohan"
- **Hindi**: "मेरा बैलेंस बताओ", "रोहन को 500 रुपये भेजें"
- **Marathi**: "तुमचे शिल्लक दाखवा", "रोहनला 500 रुपये पाठवा"
- **Hinglish**: "Mere balance kya hai", "Rohan ko 500 transfer kar do"

The system automatically detects the language and responds in the same language.

## 🧠 **Context-Aware Conversation**

TalkToBank maintains conversation context to provide better assistance:

- **Conversation History**: Remembers previous messages in the session
- **Entity Enhancement**: Fills missing information from context
- **Clarification Prompts**: Asks for missing details when needed
- **Multi-turn Conversations**: Handles follow-up questions naturally

**Example:**
```
User: "Transfer 500"
Assistant: "Who would you like to transfer money to?"
User: "To Rohan"
Assistant: "Successfully transferred ₹500 to Rohan."
```

## 🚧 **Future Enhancements**

- [ ] **Real voice biometric verification** using resemblyzer/speechbrain
- [ ] **Sentiment analysis** for tone adaptation
- [ ] **Financial insights** and spending analytics
- [ ] **Transaction visualization** with charts
- [ ] **SMS/Email OTP delivery**
- [ ] **Multi-factor authentication**
- [ ] **Transaction limits and fraud detection**
- [ ] **Integration with real banking APIs**
- [ ] **Voice activity detection** for hands-free mode

---

## 🐛 **Troubleshooting**

### **Microphone not working**
- Ensure browser has microphone permissions
- Use HTTPS in production (required for MediaRecorder API)
- Test with the text input as alternative

### **Speech recognition fails**
- Check internet connection (Google Speech API requires internet)
- Verify OPENAI_API_KEY if using Whisper
- Speak clearly and in a quiet environment

### **Backend errors**
- Check Python version (3.8+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check logs in console for detailed error messages

### **CORS errors**
- Ensure Flask-CORS is installed
- Verify backend URL in frontend `.env` file
- Check that backend is running on correct port

---

## 📝 **License**

This project is created for educational and demonstration purposes.

---

## 👥 **Contributors**

Built as a complete AI Voice Banking Assistant demonstration project.

---

## 📧 **Contact & Support**

For questions or issues:
- Check the GitHub issues page
- Review the troubleshooting section
- Test individual modules independently

---

## 🙏 **Acknowledgments**

- OpenAI for GPT and Whisper APIs
- Google for Speech Recognition
- ElevenLabs for premium TTS
- Flask and React communities

---

**Happy Banking! 🏦💰**

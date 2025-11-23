"""
Banking Knowledge Base - Comprehensive responses for all banking/financial queries
"""

BANKING_KNOWLEDGE = {
    # Greetings and General Help
    'greeting': {
        'response': """Hello! 👋 Welcome to **TalkToBank Digital Assistant**.

I'm your personal banking assistant, here to help you with:

💳 **Account Services**: Balance checks, statements, transactions
💰 **Payments & Transfers**: Send money, pay bills, manage beneficiaries
🏦 **Loans & Credit**: EMI details, interest rates, loan applications
📈 **Investments**: FD, RD, mutual funds, financial planning
🔒 **Security**: Card blocking, fraud reporting, OTP verification
📞 **Support**: Branch locations, customer care, service requests

**How can I assist you today?**

You can ask questions like:
• "Check my balance"
• "What are FD interest rates?"
• "How do I create UPI ID?"
• "Transfer money to someone"
""",
        'quick_tips': [
            'Use voice or text input for hands-free banking',
            'Upload documents for instant analysis',
            'Get financial health scores and spending insights'
        ]
    },
    
    'help': {
        'response': """**📚 What I Can Help You With:**

**🔹 Banking Operations:**
• Check account balance and transaction history
• Transfer money to contacts
• Pay bills (electricity, water, mobile, etc.)
• Request account statements

**🔹 Cards & Payments:**
• Credit/debit card information
• Card blocking and replacement
• UPI setup and digital payments
• ATM locations

**🔹 Loans & Investments:**
• Loan details and interest rates
• Fixed deposits and recurring deposits
• Mutual funds and investment advice
• EMI calculations

**🔹 Information Services:**
• Interest rates for various products
• Tax information (TDS, forms)
• Branch locations and timings
• Foreign exchange and forex cards

**🔹 Support Services:**
• File complaints and disputes
• Report fraud or unauthorized transactions
• Update contact details
• Cheque book requests

**🔹 Financial Planning:**
• Budgeting tips and savings plans
• Retirement planning
• Investment strategies
• Financial health assessment

**Try asking:**
"What's my balance?", "Tell me about FD rates", "How to block my card?"
""",
        'quick_tips': [
            'Be specific in your queries for faster responses',
            'You can interrupt anytime with a new question',
            'Use the quick action buttons for common tasks'
        ]
    },
    
    'thank_you': {
        'response': """You're welcome! 😊

I'm always here to help with your banking needs.

**Need anything else?** Feel free to ask about:
• Account services and transactions
• Loans, cards, and investments
• Financial planning and advice
• Any banking queries

**Quick Actions:**
• Check Balance
• View Transactions
• Transfer Money
• Get Financial Advice

Have a great day! 🌟
""",
        'quick_tips': [
            'Save our customer care: 1800-XXX-XXXX',
            'Download our mobile app for 24/7 access',
            'Enable biometric login for faster access'
        ]
    },
    
    # Credit Card Information
    'credit_card_info': {
        'response': """**Credit Card Information:**
        
• **Check Credit Card Balance**: Log into your account or use mobile app to view outstanding balance
• **Credit Limit**: Your spending limit is set based on your credit score and income
• **Minimum Payment**: Typically 5% of outstanding balance or ₹100 (whichever is higher)
• **Payment Due Date**: Usually 20-25 days from statement generation
• **Interest Rate**: Ranges from 2.5% to 3.5% per month (30-42% annually)
• **Rewards Points**: Earn points on every purchase, redeemable for vouchers or cashback

**Pro Tip**: Pay full amount by due date to avoid interest charges.""",
        'quick_tips': [
            'Set up auto-pay for minimum amount to avoid late fees',
            'Pay full balance to maintain good credit score',
            'Check for unauthorized transactions regularly'
        ]
    },
    
    # Investment Information
    'investment_info': {
        'response': """**Investment Options:**

**Fixed Deposit (FD):**
• Interest Rate: 6.5% - 7.5% per annum (based on tenure)
• Tenure: 7 days to 10 years
• Tax: TDS applicable if interest > ₹40,000/year
• Premature withdrawal allowed with penalty

**Recurring Deposit (RD):**
• Interest Rate: Similar to FD rates
• Minimum Monthly: ₹100 onwards
• Flexible tenure: 6 months to 10 years

**Mutual Funds:**
• Equity funds: Higher returns, higher risk
• Debt funds: Moderate returns, lower risk
• SIP: Start with ₹500/month

**Pro Tip**: Diversify investments across FD, RD, and mutual funds for balanced portfolio.""",
        'quick_tips': [
            'Start SIP early for wealth creation',
            'Senior citizens get 0.5% extra interest on FD',
            'Use FD for tax saving under 80C (5-year lock-in)'
        ]
    },
    
    # Account Services
    'account_services': {
        'response': """**Account Services:**

**Opening New Account:**
• Savings Account: Min. balance ₹1,000-₹10,000
• Current Account: For business, no interest
• Salary Account: Zero balance account
• Documents: PAN, Aadhaar, Photo, Address proof

**Account Types:**
• Regular Savings: 3-4% interest
• Senior Citizen: 0.5% extra interest
• Women's Savings: Special benefits
• Kids Account: For minors with guardian

**Update Details:**
• Mobile/Email: Visit branch or update online
• Address: Submit address proof
• Nominee: Can be updated anytime

**Close Account:**
• Visit branch with passbook and cheque book
• Clear all dues and dues
• Get account closure confirmation""",
        'quick_tips': [
            'Keep KYC updated to avoid account freeze',
            'Add nominee for hassle-free inheritance',
            'Opt for paperless statements to go green'
        ]
    },
    
    # Card Services (Debit/ATM)
    'card_services': {
        'response': """**Debit/ATM Card Services:**

**Request New Card:**
• Visit branch or request via mobile app
• Delivery in 7-10 working days
• Charges: ₹100-₹200 (varies by bank)

**Block Lost/Stolen Card:**
• Call customer care immediately: 1800-XXX-XXXX
• Report via mobile app or internet banking
• Request replacement card

**Change PIN:**
• Visit any ATM and select 'PIN Change'
• Or change via mobile banking app
• Never share PIN with anyone

**ATM Locations:**
• Use bank's mobile app to find nearest ATM
• Free transactions at own bank ATMs
• 5 free transactions/month at other bank ATMs

**Withdrawal Limits:**
• Per day: ₹25,000 - ₹50,000
• Per transaction: ₹10,000 - ₹20,000""",
        'quick_tips': [
            'Enable international usage only when traveling abroad',
            'Set transaction limits via mobile app for safety',
            'Use contactless payment for faster checkout'
        ]
    },
    
    # Cheque Services
    'cheque_services': {
        'response': """**Cheque Services:**

**Request Cheque Book:**
• Via mobile app or internet banking
• Visit branch or ATM
• Delivery in 3-5 working days
• Usually free (25-50 leaves)

**Cheque Status:**
• Check via mobile app or passbook
• Call customer care for status
• Typical clearance: 1-3 days

**Stop Cheque Payment:**
• Report via mobile app immediately
• Charges: ₹50-₹100 per cheque
• Provide cheque number and amount

**Cheque Bounce:**
• Penalty: ₹500-₹750
• Criminal case if dishonored (Section 138)
• Maintain sufficient balance
• Inform payee immediately

**Cheque Writing Tips:**
• Write clearly in capital letters
• No corrections or overwriting
• Write amount in words and figures
• Sign as per bank records""",
        'quick_tips': [
            'Keep cheque book safely to prevent fraud',
            'Inform bank if cheque book is lost',
            'Cross cheques for safety (Account Payee)'
        ]
    },
    
    # Interest Rates
    'interest_rates': {
        'response': """**Current Interest Rates (Indicative):**

**Savings Account:**
• Regular: 3.00% - 4.00% per annum
• Senior Citizen: 3.50% - 4.50% per annum

**Fixed Deposit:**
• 7 days - 45 days: 4.50% - 5.50%
• 46 days - 6 months: 5.50% - 6.50%
• 6 months - 1 year: 6.00% - 7.00%
• 1 year - 5 years: 6.50% - 7.50%
• 5 years - 10 years: 7.00% - 7.75%

**Loans:**
• Home Loan: 8.40% - 9.50%
• Personal Loan: 10.50% - 16.00%
• Car Loan: 8.70% - 10.50%
• Education Loan: 8.50% - 11.50%

**Credit Card:**
• Interest on outstanding: 30% - 42% annually

*Rates are subject to change. Check with your bank for latest rates.""",
        'quick_tips': [
            'Compare rates across banks before taking loan',
            'Senior citizens get 0.5% extra on FD',
            'Prepay loans when possible to save interest'
        ]
    },
    
    # Tax Information
    'tax_info': {
        'response': """**Tax Information:**

**TDS (Tax Deducted at Source):**
• 10% TDS on interest if > ₹40,000/year (Savings + FD)
• Senior citizens: ₹50,000 limit
• Submit Form 15G/15H to avoid TDS (if income below taxable limit)

**Form 16:**
• Issued by employer for salary income
• Contains salary, TDS details
• Required for ITR filing

**Form 26AS:**
• Tax credit statement
• Shows all TDS deducted on your PAN
• Download from Income Tax portal

**Interest Certificate:**
• Request from bank for ITR filing
• Shows interest earned on savings and FD
• Available online or at branch

**Tax Saving Instruments:**
• PPF: Up to ₹1.5 lakh under 80C
• ELSS: Equity mutual funds with 3-year lock-in
• Tax Saver FD: 5-year lock-in, up to ₹1.5 lakh under 80C
• Home Loan: ₹2 lakh under 24(b) for interest""",
        'quick_tips': [
            'Download Form 26AS before ITR filing',
            'Submit Form 15G/15H before April to avoid TDS',
            'Keep interest certificates for all accounts'
        ]
    },
    
    # Insurance
    'insurance_info': {
        'response': """**Insurance Services:**

**Life Insurance:**
• Term Plan: Pure protection, low premium
• Endowment: Savings + Insurance
• ULIP: Market-linked returns
• Coverage: 10-15x annual income recommended

**Health Insurance:**
• Mediclaim: Hospitalization coverage
• Family Floater: Covers entire family
• Critical Illness: Lump sum on diagnosis
• Minimum: ₹5 lakh coverage recommended

**Premium Payment:**
• Pay via net banking or mobile app
• Set up auto-debit for hassle-free payment
• Grace period: 30 days for non-life, 15 days for life

**Claim Process:**
• Intimate insurer within 24 hours
• Submit documents (bills, discharge summary)
• Cashless or reimbursement options
• Settlement in 15-30 days

**Bank Insurance Products:**
• Available at competitive rates
• Easy processing
• Online purchase option""",
        'quick_tips': [
            'Buy term insurance early for lower premium',
            'Disclose pre-existing conditions to avoid claim rejection',
            'Review and increase coverage every 5 years'
        ]
    },
    
    # UPI and Digital Payments
    'digital_payment': {
        'response': """**UPI & Digital Payment:**

**UPI ID Creation:**
• Download bank's mobile app
• Link bank account
• Create UPI ID: yourname@bankname
• Set UPI PIN using debit card

**Features:**
• Instant money transfer 24/7
• Scan QR code for payment
• Split bills with friends
• Pay bills and recharge

**Transaction Limits:**
• Per transaction: ₹1 lakh
• Daily limit: Varies by bank (usually ₹1 lakh)

**Safety Tips:**
• Never share UPI PIN
• Verify recipient before sending money
• Use genuine apps (PhonePe, Google Pay, Paytm)
• Enable two-factor authentication

**QR Code Payments:**
• Scan merchant QR
• Enter amount and UPI PIN
• Instant confirmation
• No charges for customers

**Popular Apps:**
• Bank's own UPI app
• PhonePe, Google Pay, Paytm
• BHIM (Government app)""",
        'quick_tips': [
            'Check transaction history regularly',
            'Report unauthorized transactions within 3 days',
            'Use UPI for instant refunds (faster than cards)'
        ]
    },
    
    # NEFT/RTGS/IMPS
    'bank_transfer': {
        'response': """**Fund Transfer Options:**

**NEFT (National Electronic Funds Transfer):**
• Timing: 24x7 (including holidays)
• Settlement: Within 2-3 hours
• Charges: ₹2.5 - ₹25 (based on amount)
• Ideal for: Regular transfers

**RTGS (Real Time Gross Settlement):**
• Minimum: ₹2 lakh
• Timing: 7 AM to 6 PM (Monday-Friday), 7 AM to 1 PM (Saturday)
• Settlement: Immediate (within 30 minutes)
• Charges: ₹25 - ₹55
• Ideal for: Large value transfers

**IMPS (Immediate Payment Service):**
• Timing: 24x7
• Settlement: Instant (within seconds)
• Limit: ₹5 lakh per day
• Charges: ₹5 - ₹15
• Ideal for: Urgent transfers

**Required Details:**
• Beneficiary name
• Account number
• IFSC code
• Bank name and branch

**Add Beneficiary:**
• Via net banking or mobile app
• Wait for activation (instant to 30 min)
• Verify before first transfer""",
        'quick_tips': [
            'Use IMPS for instant urgent transfers',
            'Add beneficiary in advance to save time',
            'Double-check account number and IFSC code'
        ]
    },
    
    # Bill Payments
    'bill_payment': {
        'response': """**Bill Payment Services:**

**Available Bills:**
• Electricity, Water, Gas
• Mobile, DTH, Broadband
• Credit Card bills
• Insurance premiums
• Loan EMIs

**Payment Methods:**
• Mobile banking app
• Internet banking
• UPI apps
• ATM
• Branch visit

**Auto-Pay Setup:**
• Set up standing instruction
• Bills paid automatically on due date
• Never miss payment
• Can be cancelled anytime

**Payment Confirmation:**
• Instant SMS/email receipt
• Save for reference
• Reflects in bill immediately

**Rewards:**
• Cashback on bill payments
• Reward points on credit card payments
• Special offers on mobile recharge

**Due Date Reminders:**
• Enable SMS/email alerts
• Set calendar reminders
• Use mobile app notifications""",
        'quick_tips': [
            'Set up auto-pay for recurring bills',
            'Keep utility account numbers saved',
            'Pay bills 2-3 days before due date'
        ]
    },
    
    # Statement Requests
    'statement_request': {
        'response': """**Account Statement:**

**Online/E-Statement:**
• Download from internet banking
• Via mobile app (instant)
• Email request for statement
• Free of cost

**Physical Statement:**
• Request at branch
• Mailed to registered address
• Charges may apply

**Statement Period:**
• Last 30 days: Free
• 3-6 months: Usually free
• Beyond 6 months: ₹50-₹100

**Available Formats:**
• PDF (password protected)
• Excel/CSV for analysis
• Physical printout

**Information Included:**
• All credits and debits
• Opening and closing balance
• Date, description, reference number
• Interest credited
• Charges debited

**Frequency:**
• Monthly e-statements (automatic)
• Quarterly physical statements
• Request anytime for specific period""",
        'quick_tips': [
            'Opt for e-statements to go paperless',
            'Download statements regularly for records',
            'Keep statements for at least 3 years'
        ]
    },
    
    # Financial Advice
    'financial_advice': {
        'response': """**Financial Planning Tips:**

**Budgeting (50-30-20 Rule):**
• 50% - Needs (rent, food, utilities)
• 30% - Wants (entertainment, dining)
• 20% - Savings & Investments

**Emergency Fund:**
• Save 6-12 months of expenses
• Keep in liquid funds (savings account, liquid mutual funds)
• Don't invest emergency fund in stocks

**Investment Strategy:**
• Start early (power of compounding)
• Diversify across assets
• SIP in mutual funds (₹500/month)
• PPF for tax-free returns
• Gold (5-10% of portfolio)

**Debt Management:**
• Pay high-interest debt first (credit cards)
• Avoid EMIs beyond 50% of income
• Prepay loans when possible

**Retirement Planning:**
• Start at 25-30 years age
• Build corpus of 25-30x annual expenses
• Mix of EPF, NPS, PPF, mutual funds

**Tax Planning:**
• Utilize ₹1.5 lakh under 80C
• HRA, home loan benefits
• Health insurance premiums (80D)

**Insurance:**
• Term insurance: 10-15x annual income
• Health insurance: ₹5-10 lakh minimum""",
        'quick_tips': [
            'Review financial goals every year',
            "Don't time the market, stay invested",
            'Increase investment by 10% every year'
        ]
    },
    
    # Balance Inquiry
    'balance_inquiry': {
        'response': """**Account Balance Information:**

**Minimum Balance:**
• Metro branches: ₹5,000 - ₹10,000
• Urban branches: ₹3,000 - ₹5,000
• Semi-urban: ₹2,000 - ₹3,000
• Rural: ₹1,000 - ₹2,000
• Penalty: ₹500-₹750 for non-maintenance

**Average Monthly Balance (AMB):**
• Calculated as: Sum of daily closing balance ÷ Days in month
• Not same as minimum balance
• Can go below some days if average is maintained

**Available Balance:**
• Amount you can withdraw immediately
• May differ from book balance
• Doesn't include uncleared cheques

**Total Balance:**
• Includes all deposits
• May include uncleared instruments
• Check cleared balance before transactions

**Check Balance:**
• Missed call: Give missed call to bank number
• SMS: Send BAL to bank number
• Mobile app: Real-time balance
• ATM: Check without withdrawal
• Passbook: Update at branch or ATM""",
        'quick_tips': [
            'Maintain AMB to avoid charges',
            'Check available balance before writing cheque',
            'Salary accounts usually have zero balance requirement'
        ]
    },
    
    # Branch Information
    'branch_info': {
        'response': """**Branch & Customer Service:**

**Find Branch:**
• Use mobile app's branch locator
• Search on bank's website
• Google Maps
• Call customer care

**Branch Timing:**
• Monday-Friday: 10:00 AM - 4:00 PM
• Saturday: 10:00 AM - 1:00 PM
• Closed on Sundays and national holidays
• Some branches have extended hours

**Services at Branch:**
• Account opening/closure
• Deposit/withdrawal (cash/cheque)
• Demand draft, pay orders
• Locker facilities
• Loan applications
• Passbook update
• Cheque book request

**Customer Care:**
• Toll-free: 1800-XXX-XXXX
• 24x7 availability
• For blocking card: Immediate action
• For complaints: Escalation matrix

**Email Support:**
• customercare@bank.com
• Response in 24-48 hours

**Online Chat:**
• Available on website and mobile app
• Instant responses for basic queries""",
        'quick_tips': [
            'Visit branch early morning to avoid crowd',
            'Book appointment online for faster service',
            'Use home branch for important work'
        ]
    },
    
    # Forex/Currency Exchange
    'forex_info': {
        'response': """**Foreign Exchange Services:**

**Currency Exchange:**
• 50+ currencies available
• Exchange at branch (with documents)
• Better rates for customers
• Prior intimation for large amounts

**Travel Card:**
• Prepaid forex card
• Multi-currency option
• Safer than carrying cash
• Reload anytime online
• Widely accepted worldwide

**Forex Rates:**
• Updated daily
• Check on bank website
• Interbank rate + markup
• Better rates for bulk exchange

**Documents Required:**
• Valid passport
• Visa (for some countries)
• Travel tickets
• PAN card

**Remittance:**
• Send money abroad (up to $250,000/year)
• Purpose: Education, medical, travel
• SWIFT transfer
• Processing: 2-3 days

**Forex Card Benefits:**
• Lock exchange rates
• Chip & PIN security
• 24x7 customer support
• Emergency cash assistance abroad""",
        'quick_tips': [
            'Buy forex 2-3 days in advance',
            'Keep some cash + majority on card',
            'Inform bank before international travel'
        ]
    },
    
    # Complaints and Disputes
    'complaint_dispute': {
        'response': """**Complaints & Dispute Resolution:**

**Register Complaint:**
• Mobile app / Internet banking
• Customer care (call/email)
• Visit branch
• Banking Ombudsman (if not resolved)

**Complaint Types:**
• Unauthorized transaction
• Wrong debit/credit
• Poor service
• Delayed processing
• Mis-selling of products

**Resolution Timeline:**
• T+0: Lodge complaint immediately
• T+7 days: First response from bank
• T+30 days: Final resolution
• Escalate to Banking Ombudsman after 30 days

**Unauthorized Transaction:**
• Report within 3 days for zero liability
• 4-7 days: Liability up to ₹10,000
• After 7 days: Liability as per bank policy
• Block card/account immediately

**Dispute Transaction:**
• Provide transaction details
• Supporting documents
• Merchant details (if applicable)
• Bank investigates (7-30 days)

**Fraud Reporting:**
• Call customer care immediately
• File FIR at police station
• Inform bank in writing
• Change passwords/PINs

**Banking Ombudsman:**
• Free service by RBI
• For unresolved complaints
• File within 1 year of complaint
• Decision binding on bank

**Escalation Matrix:**
• Branch Manager
• Regional Manager
• Grievance Redressal Officer
• Banking Ombudsman""",
        'quick_tips': [
            'Keep complaint reference number safe',
            'Report fraud within 3 days for zero liability',
            'Document all communication with bank'
        ]
    }
}


# Multilingual knowledge base responses
MULTILINGUAL_RESPONSES = {
    'hi': {
        'default_help': "मैं आपकी विभिन्न बैंकिंग जांच में मदद कर सकता हूं। पूछने का प्रयास करें:\n" +
                       "• खाता शिल्लक और लेनदेन\n" +
                       "• क्रेडिट/डेबिट कार्ड\n" +
                       "• ऋण और EMI\n" +
                       "• सावधि जमा और निवेश\n" +
                       "• UPI और डिजिटल भुगतान\n" +
                       "• बिल भुगतान\n" +
                       "• कर जानकारी\n" +
                       "• शाखा स्थान\n" +
                       "• और बहुत कुछ!",
    },
    'mr': {
        'default_help': "मी तुम्हाला विविध बँकिंग प्रश्नांमध्ये मदत करू शकतो. विचारा:\n" +
                       "• खाते शिल्लक आणि व्यवहार\n" +
                       "• क्रेडिट/डेबिट कार्ड\n" +
                       "• कर्ज आणि EMI\n" +
                       "• मुदत ठेव आणि गुंतवणूक\n" +
                       "• UPI आणि डिजिटल पेमेंट\n" +
                       "• बिल पेमेंट\n" +
                       "• कर माहिती\n" +
                       "• शाखा स्थान\n" +
                       "• आणि बरेच काही!",
    }
}


def get_response(intent: str, lang: str = 'en') -> dict:
    """Get response for detected intent with language support"""
    if intent in BANKING_KNOWLEDGE:
        response = BANKING_KNOWLEDGE[intent]['response']
        tips = BANKING_KNOWLEDGE[intent].get('quick_tips', [])
        
        # For now, return English response for all languages
        # In future, can add full translations
        # If language is Hindi or Marathi, we'll use the templates from language_support
        return {
            'success': True,
            'response': response,
            'tips': tips
        }
    else:
        # Default help message
        if lang == 'hi' and 'default_help' in MULTILINGUAL_RESPONSES['hi']:
            default_response = MULTILINGUAL_RESPONSES['hi']['default_help']
        elif lang == 'mr' and 'default_help' in MULTILINGUAL_RESPONSES['mr']:
            default_response = MULTILINGUAL_RESPONSES['mr']['default_help']
        else:
            default_response = ("I can help you with various banking queries. Try asking about:\n" +
                             "• Account balance and transactions\n" +
                             "• Credit/debit cards\n" +
                             "• Loans and EMIs\n" +
                             "• Fixed deposits and investments\n" +
                             "• UPI and digital payments\n" +
                             "• Bill payments\n" +
                             "• Tax information\n" +
                             "• Branch locations\n" +
                             "• And much more!")
        
        return {
            'success': False,
            'response': default_response,
            'tips': []
        }

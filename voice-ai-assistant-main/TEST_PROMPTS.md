# 🧪 TalkToBank - Comprehensive Test Prompts Guide

This document provides a complete list of test prompts to verify all features of the TalkToBank application.

---

## 📋 Table of Contents
1. [Core Banking Operations](#1-core-banking-operations)
2. [Voice Input Testing](#2-voice-input-testing)
3. [Multilingual Support](#3-multilingual-support)
4. [Document Upload & OCR](#4-document-upload--ocr)
5. [Financial Advice & Analytics](#5-financial-advice--analytics)
6. [Navigation & UI Sections](#6-navigation--ui-sections)
7. [Knowledge Base Queries](#7-knowledge-base-queries)
8. [Context & Follow-up Questions](#8-context--follow-up-questions)
9. [Error Handling & Edge Cases](#9-error-handling--edge-cases)

---

## 1. Core Banking Operations

### ✅ Balance Checks
```
- "Check my balance"
- "What's my account balance?"
- "Show me my savings account balance"
- "How much money do I have?"
- "Current balance"
- "Balance in my current account"
```

### 💸 Fund Transfers
```
- "Transfer 500 to Rohan"
- "Send ₹1000 to Priya"
- "Transfer money to John"
- "Send 2500 rupees to my friend"
- "I want to transfer 5000 to Sarah"
```

### 📜 Transaction History
```
- "Show my last 5 transactions"
- "Recent payments"
- "Transaction history"
- "What are my last 10 transactions?"
- "Show me all transactions this month"
- "Recent activity"
```

### 🏦 Loan Details
```
- "What's my loan interest rate?"
- "Loan details"
- "Show me my loan information"
- "What's my loan balance?"
- "When is my loan due?"
```

### ⏰ Reminders
```
- "Remind me to pay EMI next Monday"
- "Set a reminder for bill payment on 15th"
- "Remind me about loan payment"
```

---

## 2. Voice Input Testing

### 🎤 Voice Commands (Click mic button and speak)
```
1. "Check my balance"
2. "Transfer 1000 to Rohan"
3. "Show my last 5 transactions"
4. "What's my loan interest rate?"
5. "How do I open a savings account?"
```

**Test Scenarios:**
- ✅ Start recording, speak clearly, stop recording
- ✅ Test with background noise
- ✅ Test with different speaking speeds
- ✅ Test stopping mid-sentence
- ✅ Test multiple voice commands in sequence

---

## 3. Multilingual Support

### 🇮🇳 Hindi (हिंदी)
```
- "मेरा बैलेंस क्या है?"
- "रोहन को 500 रुपये भेजो"
- "मेरे पिछले 5 लेनदेन दिखाओ"
- "मेरा लोन कितना है?"
- "बचत खाता कैसे खोलें?"
```

### 🇮🇳 Marathi (मराठी)
```
- "माझी शिल्लक किती आहे?"
- "रोहनला 500 रुपये पाठवा"
- "माझ्या शेवटच्या 5 व्यवहार दाखवा"
- "माझे कर्ज किती आहे?"
```

### 🇮🇳 Hinglish (Mixed)
```
- "Mera balance kya hai?"
- "Rohan ko 500 rupees bhejo"
- "Mere last 5 transactions dikhao"
- "Savings account kaise kholen?"
```

**Test Steps:**
1. Go to Settings (⚙️)
2. Select language (English/Hindi/Marathi/Hinglish)
3. Try the prompts above
4. Verify responses are in selected language

---

## 4. Document Upload & OCR

### 📄 Document Testing
1. **Click "Upload Document" button**
2. **Test with different file types:**
   - PDF bills (electricity, water, gas)
   - JPG/PNG images of receipts
   - Bank statements (PDF)
   - Invoice images

**Expected Behavior:**
- ✅ Document uploads successfully
- ✅ OCR extracts text/amounts
- ✅ Shows extracted information
- ✅ Provides insights about the document

---

## 5. Financial Advice & Analytics

### 💡 Financial Advice Button
1. **Click "Financial Advice" button**
2. **Try these prompts:**
   ```
   - "How can I save more money?"
   - "Should I invest in mutual funds?"
   - "How do I reduce debt?"
   - "What's the best investment strategy?"
   - "How to create a budget?"
   - "Retirement planning tips"
   ```

### 📊 Health Score Button
1. **Click "Health Report" button**
2. **Verify:**
   - ✅ Shows financial health score (0-100)
   - ✅ Displays health level (Good/Fair/Poor)
   - ✅ Provides recommendations
   - ✅ Shows breakdown of factors

### 📈 Spending Analysis Button
1. **Click "Spending Analysis" button**
2. **Verify:**
   - ✅ Shows total spending
   - ✅ Displays top spending category
   - ✅ Breakdown by category
   - ✅ Percentage distribution

---

## 6. Navigation & UI Sections

### 🧭 Navigation Menu Testing
Click each menu item and verify:

1. **Chat** - Main chat interface
   - ✅ Chat messages display correctly
   - ✅ Input field works
   - ✅ Voice button functional

2. **Accounts**
   - ✅ Shows all accounts
   - ✅ Displays balances
   - ✅ Account types shown correctly

3. **Payments**
   - ✅ Monthly spending displayed
   - ✅ Transaction count shown
   - ✅ Recent transactions table

4. **Cards**
   - ✅ All cards listed
   - ✅ Card numbers displayed
   - ✅ Limits and expiry dates shown

5. **Loans**
   - ✅ Active loans displayed
   - ✅ Interest rates shown
   - ✅ Due dates visible

6. **Investments**
   - ✅ Total investment amount
   - ✅ Individual investments listed
   - ✅ Interest rates and maturity dates

---

## 7. Knowledge Base Queries

### 💳 Credit Card Information
```
- "What's my credit card limit?"
- "How to block lost card?"
- "What's the minimum credit card payment?"
- "Credit card interest rate"
- "When is my credit card payment due?"
```

### 💰 Investment Information
```
- "What's the FD interest rate?"
- "How to open recurring deposit?"
- "Tell me about mutual funds"
- "Fixed deposit rates"
- "RD interest rates"
```

### 🏛️ Account Services
```
- "How do I open a savings account?"
- "What's the minimum balance for metro branches?"
- "How to close my account?"
- "Update my mobile number"
- "Change account address"
```

### 🏧 Card Services
```
- "Find nearest ATM"
- "How to change PIN?"
- "Block my debit card"
- "Request new card"
- "ATM withdrawal limit"
```

### 📝 Cheque Services
```
- "How to request cheque book?"
- "Stop payment on cheque"
- "Cheque bounce charges"
- "Cheque book charges"
```

### 💵 Interest Rates
```
- "Savings account interest rate"
- "Current FD rates"
- "Loan interest rates"
- "Home loan interest rate"
```

### 📑 Tax Information
```
- "How to get Form 26AS?"
- "What's TDS on fixed deposits?"
- "Tax saving investment options?"
- "Form 16 download"
- "Interest certificate"
```

### 🛡️ Insurance
```
- "How much life insurance do I need?"
- "How to file insurance claim?"
- "Health insurance premium"
```

### 💳 Digital Payments
```
- "How to set up UPI?"
- "UPI transaction limit"
- "QR code payment"
- "Mobile banking setup"
```

### 🏦 Bank Transfers
```
- "How does RTGS work?"
- "NEFT charges"
- "IMPS transfer limit"
- "How to add beneficiary?"
- "IFSC code lookup"
```

### 💡 Bill Payments
```
- "How to pay electricity bill?"
- "Water bill payment"
- "Mobile recharge"
- "DTH recharge"
- "Auto-pay setup"
```

### 📄 Statements
```
- "Download e-statement"
- "Request statement"
- "Statement for last 3 months"
```

### 🏢 Branch & Customer Service
```
- "Nearest branch location?"
- "Bank customer care number?"
- "Branch working hours?"
- "ATM locations near me"
```

### 💱 Foreign Exchange
```
- "Current USD exchange rate?"
- "How to get forex card?"
- "International remittance"
```

### 📊 Financial Planning
```
- "How to create a budget?"
- "Retirement planning tips?"
- "Best investment strategy?"
- "Savings tips"
```

### ⚠️ Complaints & Disputes
```
- "How to file complaint?"
- "Report unauthorized transaction"
- "Dispute a charge"
- "Banking Ombudsman"
```

---

## 8. Context & Follow-up Questions

### 🔄 Context Testing (Multi-turn Conversations)
```
**Test Sequence 1:**
1. "Transfer 1000 to Rohan"
2. "Send the same amount to him" (should use Rohan from context)
3. "What's my balance now?"

**Test Sequence 2:**
1. "Check my balance"
2. "Transfer 500 to Priya"
3. "Show my transactions"
4. "What's my balance?" (should reflect the transfer)

**Test Sequence 3:**
1. "I want to transfer money"
2. System asks: "How much and to whom?"
3. "500 to John"
4. System processes transfer

**Test Sequence 4:**
1. "Show my savings account"
2. "What's the balance?"
3. "Transfer 200 from it"
```

---

## 9. Error Handling & Edge Cases

### ❌ Invalid Inputs
```
- "Transfer money" (no amount/recipient)
- "Check balance" (should work)
- "Transfer 999999999 to someone" (insufficient balance)
- "Show transactions from 2050" (invalid date)
- "" (empty message)
```

### 🔒 Security Testing
```
- Test OTP verification (if implemented)
- Test voice ID verification
- Test unauthorized access attempts
```

### 📱 Responsive Design
```
- Test on different screen sizes
- Test landscape/portrait orientation
- Test sidebar collapse on mobile
- Test chat interface on mobile
```

### ⚡ Performance Testing
```
- Test with slow internet connection
- Test multiple rapid requests
- Test large transaction history
- Test document upload with large files
```

---

## 🎯 Quick Test Checklist

### ✅ Must-Test Features (Priority 1)
- [ ] Balance check (text + voice)
- [ ] Fund transfer (text + voice)
- [ ] Transaction history
- [ ] Voice input recording
- [ ] Document upload
- [ ] Financial advice button
- [ ] Health score button
- [ ] Language switching (Settings)
- [ ] Navigation between sections

### ✅ Important Features (Priority 2)
- [ ] Loan details
- [ ] Reminder setting
- [ ] Spending analysis
- [ ] Multilingual responses (Hindi/Marathi)
- [ ] Context follow-up questions
- [ ] Knowledge base queries

### ✅ Nice-to-Have Tests (Priority 3)
- [ ] All navigation sections
- [ ] Error handling
- [ ] Responsive design
- [ ] Performance under load

---

## 📝 Testing Tips

1. **Start Simple**: Begin with basic balance checks and transfers
2. **Test Voice**: Use the microphone button for voice commands
3. **Try Multilingual**: Switch languages in Settings and test
4. **Upload Documents**: Test with real bills/receipts
5. **Check Context**: Have multi-turn conversations
6. **Explore Sections**: Click through all navigation items
7. **Test Buttons**: Use all action buttons (Upload, Advice, Health, Analysis)
8. **Verify Responses**: Check that responses are accurate and formatted well

---

## 🐛 Common Issues to Watch For

- ❌ Voice input not working (check mic permissions)
- ❌ Backend not responding (check if server is running on port 5001)
- ❌ Language not switching (check Settings modal)
- ❌ Document upload failing (check file size/format)
- ❌ Balance not updating after transfer
- ❌ Transactions not displaying in table format
- ❌ Audio playback not working

---

## 📞 Support

If you encounter issues:
1. Check browser console for errors (F12)
2. Verify backend server is running
3. Check network tab for API calls
4. Review server logs in terminal

---

**Happy Testing! 🚀**


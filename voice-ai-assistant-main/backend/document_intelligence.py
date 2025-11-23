"""
Document Intelligence Module
Upload and analyze financial documents (bills, receipts, bank statements)
"""
import os
import re
import logging
from typing import Dict, Any, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Try to import OCR libraries
try:
    from PIL import Image
    import pytesseract
    # Set tesseract path for Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("PIL or pytesseract not available. OCR features disabled.")

# Try to import PDF processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("PyPDF2 not available. PDF processing disabled.")


def extract_text_from_image(image_path: str) -> str:
    """Extract text from image using OCR"""
    if not OCR_AVAILABLE:
        return "OCR not available. Install pytesseract and Tesseract-OCR."
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"OCR error: {str(e)}")
        return f"Error extracting text: {str(e)}"


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF"""
    if not PDF_AVAILABLE:
        return "PDF processing not available. Install PyPDF2."
    
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        return f"Error extracting PDF: {str(e)}"


def analyze_bill(text: str) -> Dict[str, Any]:
    """
    Analyze bill/invoice text and extract key information
    """
    result = {
        'type': 'bill',
        'total_amount': None,
        'bill_date': None,
        'vendor': None,
        'items': [],
        'category': 'Bills & Utilities'
    }
    
    # Extract total amount
    amount_patterns = [
        r'total[:\s]+₹?\s*([\d,]+\.?\d*)',
        r'amount[:\s]+₹?\s*([\d,]+\.?\d*)',
        r'₹\s*([\d,]+\.?\d*)',
        r'rs\.?\s*([\d,]+\.?\d*)',
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '')
            try:
                result['total_amount'] = float(amount_str)
                break
            except ValueError:
                pass
    
    # Extract date
    date_patterns = [
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',
        r'\b(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4})\b',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['bill_date'] = match.group(1)
            break
    
    # Identify vendor/merchant
    text_lines = text.strip().split('\n')
    if text_lines:
        # Usually first non-empty line is vendor name
        for line in text_lines[:5]:
            if line.strip() and len(line.strip()) > 3:
                result['vendor'] = line.strip()[:50]
                break
    
    # Categorize bill
    text_lower = text.lower()
    if any(word in text_lower for word in ['electricity', 'power', 'energy']):
        result['category'] = 'Electricity Bill'
    elif any(word in text_lower for word in ['water', 'sewage']):
        result['category'] = 'Water Bill'
    elif any(word in text_lower for word in ['internet', 'broadband', 'wifi']):
        result['category'] = 'Internet Bill'
    elif any(word in text_lower for word in ['mobile', 'phone', 'telecom']):
        result['category'] = 'Mobile Bill'
    elif any(word in text_lower for word in ['gas', 'cylinder']):
        result['category'] = 'Gas Bill'
    
    return result


def analyze_receipt(text: str) -> Dict[str, Any]:
    """
    Analyze receipt and extract purchase details
    """
    result = {
        'type': 'receipt',
        'total_amount': None,
        'date': None,
        'merchant': None,
        'items': [],
        'category': 'Shopping'
    }
    
    # Extract amount (similar to bill)
    amount_patterns = [
        r'total[:\s]+₹?\s*([\d,]+\.?\d*)',
        r'grand\s+total[:\s]+₹?\s*([\d,]+\.?\d*)',
        r'₹\s*([\d,]+\.?\d*)',
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '')
            try:
                result['total_amount'] = float(amount_str)
                break
            except ValueError:
                pass
    
    # Extract line items (product names and prices)
    item_pattern = r'(.+?)\s+₹?\s*([\d,]+\.?\d*)'
    matches = re.findall(item_pattern, text, re.MULTILINE)
    
    for item_name, price_str in matches[:10]:  # Limit to 10 items
        try:
            price = float(price_str.replace(',', ''))
            if 0 < price < 100000:  # Reasonable price range
                result['items'].append({
                    'name': item_name.strip()[:50],
                    'price': price
                })
        except ValueError:
            pass
    
    # Categorize
    text_lower = text.lower()
    if any(word in text_lower for word in ['restaurant', 'cafe', 'hotel', 'food']):
        result['category'] = 'Food & Dining'
    elif any(word in text_lower for word in ['pharmacy', 'medical', 'hospital']):
        result['category'] = 'Healthcare'
    elif any(word in text_lower for word in ['fuel', 'petrol', 'diesel']):
        result['category'] = 'Transportation'
    
    return result


def analyze_bank_statement(text: str) -> Dict[str, Any]:
    """
    Analyze bank statement and extract transactions
    """
    result = {
        'type': 'bank_statement',
        'total_credits': 0,
        'total_debits': 0,
        'transactions': [],
        'period': None
    }
    
    # Extract transactions
    # Pattern: Date, Description, Debit/Credit amount
    transaction_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\s+(.+?)\s+([\d,]+\.?\d*)\s*([CD]|debit|credit)?'
    
    matches = re.findall(transaction_pattern, text, re.IGNORECASE)
    
    for date, description, amount_str, txn_type in matches[:50]:  # Limit to 50 transactions
        try:
            amount = float(amount_str.replace(',', ''))
            
            # Determine if credit or debit
            is_credit = any(word in txn_type.lower() for word in ['c', 'credit'])
            
            result['transactions'].append({
                'date': date,
                'description': description.strip()[:100],
                'amount': amount,
                'type': 'credit' if is_credit else 'debit'
            })
            
            if is_credit:
                result['total_credits'] += amount
            else:
                result['total_debits'] += amount
                
        except ValueError:
            pass
    
    result['net_balance_change'] = result['total_credits'] - result['total_debits']
    
    return result


def process_document(file_path: str, file_type: str) -> Dict[str, Any]:
    """
    Main function to process any financial document
    
    Args:
        file_path: Path to the document
        file_type: 'image', 'pdf', or auto-detect from extension
    
    Returns:
        Analyzed document data
    """
    result = {
        'success': False,
        'message': '',
        'data': None
    }
    
    try:
        # Extract text based on file type
        if file_type in ['image', 'jpg', 'jpeg', 'png']:
            text = extract_text_from_image(file_path)
        elif file_type == 'pdf':
            text = extract_text_from_pdf(file_path)
        else:
            # Auto-detect from extension
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                text = extract_text_from_image(file_path)
            elif ext == '.pdf':
                text = extract_text_from_pdf(file_path)
            else:
                result['message'] = f"Unsupported file type: {ext}"
                return result
        
        if not text or len(text.strip()) < 10:
            result['message'] = "Could not extract meaningful text from document"
            return result
        
        # Determine document type and analyze
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['invoice', 'bill no', 'bill date', 'electricity', 'water', 'gas']):
            result['data'] = analyze_bill(text)
        elif any(word in text_lower for word in ['receipt', 'items purchased', 'qty', 'total amount']):
            result['data'] = analyze_receipt(text)
        elif any(word in text_lower for word in ['bank statement', 'account statement', 'opening balance', 'closing balance']):
            result['data'] = analyze_bank_statement(text)
        else:
            # Generic analysis
            result['data'] = {
                'type': 'document',
                'text_preview': text[:500],
                'full_text': text
            }
        
        result['success'] = True
        result['message'] = 'Document processed successfully'
        
    except Exception as e:
        logger.error(f"Document processing error: {str(e)}")
        result['message'] = f"Error processing document: {str(e)}"
    
    return result


def generate_expense_summary(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary from multiple uploaded documents
    """
    total_expenses = 0
    by_category = {}
    all_items = []
    
    for doc in documents:
        if doc.get('type') in ['bill', 'receipt']:
            amount = doc.get('total_amount', 0) or 0
            category = doc.get('category', 'Other')
            
            total_expenses += amount
            by_category[category] = by_category.get(category, 0) + amount
            
            if doc.get('items'):
                all_items.extend(doc['items'])
    
    return {
        'total_expenses': round(total_expenses, 2),
        'by_category': by_category,
        'document_count': len(documents),
        'top_expense': max(by_category.items(), key=lambda x: x[1]) if by_category else None
    }


def extract_actionable_insights(doc_data: Dict[str, Any]) -> List[str]:
    """
    Generate actionable insights from document analysis
    """
    insights = []
    
    if doc_data.get('type') == 'bill':
        amount = doc_data.get('total_amount')
        category = doc_data.get('category', '')
        
        if amount and amount > 5000 and 'Electricity' in category:
            insights.append("⚡ High electricity bill detected. Consider using energy-efficient appliances.")
        
        if amount and 'Internet' in category:
            insights.append("📱 Review your internet plan - you might find better deals with competitors.")
    
    elif doc_data.get('type') == 'receipt':
        items = doc_data.get('items', [])
        total = doc_data.get('total_amount', 0)
        
        if total > 10000:
            insights.append("💰 Large purchase detected. Ensure it's within your monthly budget.")
        
        if len(items) > 20:
            insights.append("🛒 Many items purchased. Track if these are necessities or impulse buys.")
    
    elif doc_data.get('type') == 'bank_statement':
        total_debits = doc_data.get('total_debits', 0)
        total_credits = doc_data.get('total_credits', 0)
        
        if total_debits > total_credits:
            insights.append("⚠️ You're spending more than you're earning. Review and reduce expenses.")
        else:
            insights.append("✅ Great job! You're saving money this period.")
    
    if not insights:
        insights.append("📊 Document uploaded successfully. Keep tracking your expenses regularly!")
    
    return insights


if __name__ == '__main__':
    print("=== Document Intelligence Module ===\n")
    print("Features:")
    print("- OCR Available:", OCR_AVAILABLE)
    print("- PDF Processing Available:", PDF_AVAILABLE)
    print("\nThis module can analyze:")
    print("  • Bills (electricity, water, internet, mobile)")
    print("  • Receipts (shopping, dining, fuel)")
    print("  • Bank statements")
    print("  • Any financial document with text")

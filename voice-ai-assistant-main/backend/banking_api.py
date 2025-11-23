import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import uuid

logger = logging.getLogger(__name__)

DB_PATH = 'database.db'


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database with schema and mock data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            voice_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            txn_id TEXT PRIMARY KEY,
            account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            recipient TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (account_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            interest_rate REAL NOT NULL,
            due_date DATE NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            card_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            card_type TEXT NOT NULL,
            card_number TEXT NOT NULL,
            card_holder_name TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            cvv TEXT,
            limit_amount REAL,
            available_limit REAL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            investment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            investment_type TEXT NOT NULL,
            amount REAL NOT NULL,
            interest_rate REAL,
            maturity_date DATE,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otps (
            otp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            otp TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Insert mock data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        logger.info("Inserting mock data...")
        
        # Insert users
        cursor.execute('''
            INSERT INTO users (name, email, voice_id)
            VALUES ('Demo User', 'demo@example.com', 'voice_hash_123')
        ''')
        
        cursor.execute('''
            INSERT INTO users (name, email, voice_id)
            VALUES ('Rohan Kumar', 'rohan@example.com', 'voice_hash_456')
        ''')
        
        # Insert accounts
        cursor.execute('''
            INSERT INTO accounts (user_id, account_type, balance)
            VALUES (1, 'savings', 25430.50)
        ''')
        
        cursor.execute('''
            INSERT INTO accounts (user_id, account_type, balance)
            VALUES (1, 'current', 15000.00)
        ''')
        
        cursor.execute('''
            INSERT INTO accounts (user_id, account_type, balance)
            VALUES (2, 'savings', 50000.00)
        ''')
        
        # Insert transactions
        transactions_data = [
            (str(uuid.uuid4()), 1, -2500.00, 'debit', 'Amazon', '2025-11-05 10:30:00'),
            (str(uuid.uuid4()), 1, 15000.00, 'credit', None, '2025-11-01 09:00:00'),
            (str(uuid.uuid4()), 1, -500.00, 'debit', 'Rohan Kumar', '2025-10-28 14:20:00'),
            (str(uuid.uuid4()), 1, -1200.00, 'debit', 'Electricity Bill', '2025-10-25 16:45:00'),
            (str(uuid.uuid4()), 1, -350.00, 'debit', 'Netflix', '2025-10-22 08:15:00'),
        ]
        
        cursor.executemany('''
            INSERT INTO transactions (txn_id, account_id, amount, type, recipient, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', transactions_data)
        
        # Insert loans
        due_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO loans (user_id, amount, interest_rate, due_date)
            VALUES (1, 500000.00, 8.5, ?)
        ''', (due_date,))
        
        # Insert cards
        cards_data = [
            (1, 'debit', '**** **** **** 1234', 'Demo User', '12/26', '123', 0, 0, 'active'),
            (1, 'credit', '**** **** **** 5678', 'Demo User', '09/27', '456', 100000.00, 75000.00, 'active'),
        ]
        cursor.executemany('''
            INSERT INTO cards (user_id, card_type, card_number, card_holder_name, expiry_date, cvv, limit_amount, available_limit, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', cards_data)
        
        # Insert investments
        investments_data = [
            (1, 'Fixed Deposit', 500000.00, 7.5, (datetime.now() + timedelta(days=1095)).strftime('%Y-%m-%d'), 'active'),
            (1, 'Recurring Deposit', 10000.00, 6.8, (datetime.now() + timedelta(days=730)).strftime('%Y-%m-%d'), 'active'),
            (1, 'Mutual Fund', 250000.00, 12.0, None, 'active'),
        ]
        cursor.executemany('''
            INSERT INTO investments (user_id, investment_type, amount, interest_rate, maturity_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', investments_data)
        
        logger.info("Mock data inserted successfully")
    
    conn.commit()
    conn.close()
    logger.info("Database initialized")


def check_balance(user_id: int, account_type: str = 'savings') -> Dict[str, Any]:
    """Check account balance"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT balance FROM accounts
            WHERE user_id = ? AND account_type = ?
        ''', (user_id, account_type))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'success': True,
                'balance': result['balance'],
                'account_type': account_type
            }
        else:
            return {
                'success': False,
                'message': f'No {account_type} account found'
            }
    
    except Exception as e:
        logger.error(f"Balance check error: {str(e)}")
        return {'success': False, 'message': str(e)}


def transfer_funds(user_id: int, recipient: str, amount: float) -> Dict[str, Any]:
    """Transfer funds to recipient"""
    try:
        if amount <= 0:
            return {'success': False, 'message': 'Invalid amount'}
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check balance
        cursor.execute('''
            SELECT account_id, balance FROM accounts
            WHERE user_id = ? AND account_type = 'savings'
        ''', (user_id,))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return {'success': False, 'message': 'Account not found'}
        
        account_id = result['account_id']
        balance = result['balance']
        
        if balance < amount:
            conn.close()
            return {'success': False, 'message': 'Insufficient balance'}
        
        # Update balance
        new_balance = balance - amount
        cursor.execute('''
            UPDATE accounts SET balance = ?
            WHERE account_id = ?
        ''', (new_balance, account_id))
        
        # Record transaction
        txn_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO transactions (txn_id, account_id, amount, type, recipient)
            VALUES (?, ?, ?, 'debit', ?)
        ''', (txn_id, account_id, -amount, recipient))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'transaction_id': txn_id,
            'amount': amount,
            'recipient': recipient,
            'new_balance': new_balance
        }
    
    except Exception as e:
        logger.error(f"Transfer error: {str(e)}")
        return {'success': False, 'message': str(e)}


def get_transaction_history(user_id: int, limit: int = 5) -> Dict[str, Any]:
    """Get transaction history"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.txn_id, t.amount, t.type, t.recipient, t.date
            FROM transactions t
            JOIN accounts a ON t.account_id = a.account_id
            WHERE a.user_id = ?
            ORDER BY t.date DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        transactions = []
        for row in results:
            transactions.append({
                'txn_id': row['txn_id'],
                'amount': abs(row['amount']),
                'type': row['type'],
                'recipient': row['recipient'],
                'date': row['date']
            })
        
        return {
            'success': True,
            'transactions': transactions
        }
    
    except Exception as e:
        logger.error(f"Transaction history error: {str(e)}")
        return {'success': False, 'message': str(e)}


def get_loan_details(user_id: int) -> Dict[str, Any]:
    """Get loan details"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT loan_id, amount, interest_rate, due_date, status
            FROM loans
            WHERE user_id = ? AND status = 'active'
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        loans = []
        for row in results:
            loans.append({
                'loan_id': row['loan_id'],
                'amount': row['amount'],
                'interest_rate': row['interest_rate'],
                'due_date': row['due_date'],
                'status': row['status']
            })
        
        return {
            'success': True,
            'loans': loans
        }
    
    except Exception as e:
        logger.error(f"Loan details error: {str(e)}")
        return {'success': False, 'message': str(e)}


def get_all_accounts(user_id: int) -> Dict[str, Any]:
    """Get all accounts for a user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_id, account_type, balance, created_at
            FROM accounts
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        accounts = []
        total_balance = 0
        for row in results:
            balance = row['balance']
            total_balance += balance
            accounts.append({
                'account_id': row['account_id'],
                'account_type': row['account_type'],
                'balance': balance,
                'created_at': row['created_at']
            })
        
        return {
            'success': True,
            'accounts': accounts,
            'total_balance': total_balance
        }
    
    except Exception as e:
        logger.error(f"Get accounts error: {str(e)}")
        return {'success': False, 'message': str(e)}


def get_cards(user_id: int) -> Dict[str, Any]:
    """Get all cards for a user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT card_id, card_type, card_number, card_holder_name, expiry_date, 
                   limit_amount, available_limit, status
            FROM cards
            WHERE user_id = ? AND status = 'active'
            ORDER BY created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        cards = []
        for row in results:
            cards.append({
                'card_id': row['card_id'],
                'card_type': row['card_type'],
                'card_number': row['card_number'],
                'card_holder_name': row['card_holder_name'],
                'expiry_date': row['expiry_date'],
                'limit_amount': row['limit_amount'],
                'available_limit': row['available_limit'],
                'status': row['status']
            })
        
        return {
            'success': True,
            'cards': cards
        }
    
    except Exception as e:
        logger.error(f"Get cards error: {str(e)}")
        return {'success': False, 'message': str(e)}


def get_investments(user_id: int) -> Dict[str, Any]:
    """Get all investments for a user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT investment_id, investment_type, amount, interest_rate, maturity_date, status
            FROM investments
            WHERE user_id = ? AND status = 'active'
            ORDER BY created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        investments = []
        total_investment = 0
        for row in results:
            amount = row['amount']
            total_investment += amount
            investments.append({
                'investment_id': row['investment_id'],
                'investment_type': row['investment_type'],
                'amount': amount,
                'interest_rate': row['interest_rate'],
                'maturity_date': row['maturity_date'],
                'status': row['status']
            })
        
        return {
            'success': True,
            'investments': investments,
            'total_investment': total_investment
        }
    
    except Exception as e:
        logger.error(f"Get investments error: {str(e)}")
        return {'success': False, 'message': str(e)}


def get_payments_summary(user_id: int) -> Dict[str, Any]:
    """Get payments summary (recent transactions, bills, etc.)"""
    try:
        # Get recent transactions
        transaction_result = get_transaction_history(user_id, 10)
        
        # Calculate monthly spending
        conn = get_db_connection()
        cursor = conn.cursor()
        
        current_month_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT SUM(ABS(amount)) as total_spent
            FROM transactions t
            JOIN accounts a ON t.account_id = a.account_id
            WHERE a.user_id = ? AND t.type = 'debit' AND t.date >= ?
        ''', (user_id, current_month_start))
        
        result = cursor.fetchone()
        monthly_spending = result['total_spent'] if result['total_spent'] else 0
        conn.close()
        
        return {
            'success': True,
            'recent_transactions': transaction_result.get('transactions', []) if transaction_result.get('success') else [],
            'monthly_spending': monthly_spending,
            'transaction_count': len(transaction_result.get('transactions', [])) if transaction_result.get('success') else 0
        }
    
    except Exception as e:
        logger.error(f"Get payments summary error: {str(e)}")
        return {'success': False, 'message': str(e)}


def set_reminder(user_id: int, message: str, due_date: str = None) -> Dict[str, Any]:
    """Set a reminder"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reminders (user_id, message, due_date)
            VALUES (?, ?, ?)
        ''', (user_id, message, due_date))
        
        reminder_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'reminder_id': reminder_id,
            'message': message,
            'due_date': due_date
        }
    
    except Exception as e:
        logger.error(f"Set reminder error: {str(e)}")
        return {'success': False, 'message': str(e)}


if __name__ == '__main__':
    # Initialize database and test
    init_database()
    print("Database initialized successfully")
    
    # Test operations
    print("\n--- Testing Banking API ---")
    
    # Test balance check
    balance = check_balance(1, 'savings')
    print(f"Balance: {balance}")
    
    # Test transaction history
    history = get_transaction_history(1, 3)
    print(f"Transaction History: {history}")
    
    # Test loan details
    loans = get_loan_details(1)
    print(f"Loans: {loans}")

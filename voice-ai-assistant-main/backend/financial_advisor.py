"""
Advanced AI Financial Advisor Module
Provides intelligent financial analysis, recommendations, and insights
"""
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

# Try to import OpenAI for advanced features
try:
    import openai
    OPENAI_AVAILABLE = True
    openai.api_key = os.getenv('OPENAI_API_KEY', '')
except ImportError:
    OPENAI_AVAILABLE = False


def calculate_financial_health_score(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate a comprehensive financial health score (0-100)
    Based on multiple factors: balance, spending, savings, debt
    """
    score = 50  # Base score
    factors = {}
    
    balance = user_data.get('balance', 0)
    monthly_income = user_data.get('monthly_income', 30000)  # Estimated
    loans = user_data.get('loans', [])
    transactions = user_data.get('transactions', [])
    
    # Factor 1: Balance-to-Income Ratio (0-25 points)
    balance_ratio = balance / monthly_income if monthly_income > 0 else 0
    if balance_ratio >= 2:
        balance_score = 25
    elif balance_ratio >= 1:
        balance_score = 20
    elif balance_ratio >= 0.5:
        balance_score = 15
    elif balance_ratio >= 0.2:
        balance_score = 10
    else:
        balance_score = 5
    
    factors['balance_health'] = balance_score
    score += balance_score
    
    # Factor 2: Debt Management (0-25 points)
    total_debt = sum(loan.get('amount', 0) for loan in loans)
    debt_ratio = total_debt / monthly_income if monthly_income > 0 else 0
    
    if debt_ratio == 0:
        debt_score = 25
    elif debt_ratio < 2:
        debt_score = 20
    elif debt_ratio < 4:
        debt_score = 15
    elif debt_ratio < 6:
        debt_score = 10
    else:
        debt_score = 5
    
    factors['debt_management'] = debt_score
    score += debt_score
    
    # Factor 3: Spending Habits (0-25 points)
    recent_debits = [t for t in transactions if t.get('type') == 'debit']
    if recent_debits:
        avg_spending = sum(abs(t.get('amount', 0)) for t in recent_debits) / len(recent_debits)
        spending_ratio = avg_spending / (monthly_income / 30)  # Daily spending vs daily income
        
        if spending_ratio < 0.3:
            spending_score = 25
        elif spending_ratio < 0.5:
            spending_score = 20
        elif spending_ratio < 0.7:
            spending_score = 15
        elif spending_ratio < 0.9:
            spending_score = 10
        else:
            spending_score = 5
    else:
        spending_score = 15
    
    factors['spending_habits'] = spending_score
    score += spending_score
    
    # Normalize to 0-100
    score = min(100, max(0, score))
    
    # Determine health level
    if score >= 80:
        health_level = "Excellent"
        color = "green"
    elif score >= 60:
        health_level = "Good"
        color = "lightgreen"
    elif score >= 40:
        health_level = "Fair"
        color = "orange"
    else:
        health_level = "Needs Improvement"
        color = "red"
    
    return {
        'score': round(score, 1),
        'health_level': health_level,
        'color': color,
        'factors': factors,
        'recommendations': generate_health_recommendations(score, factors)
    }


def generate_health_recommendations(score: float, factors: Dict[str, int]) -> List[str]:
    """Generate personalized recommendations based on health score"""
    recommendations = []
    
    if factors.get('balance_health', 0) < 15:
        recommendations.append("💰 Build an emergency fund equal to 3-6 months of expenses")
    
    if factors.get('debt_management', 0) < 15:
        recommendations.append("📉 Focus on reducing high-interest debt first")
    
    if factors.get('spending_habits', 0) < 15:
        recommendations.append("📊 Track your expenses and create a monthly budget")
    
    if score >= 80:
        recommendations.append("🎯 Consider investing in mutual funds or SIPs for wealth growth")
        recommendations.append("📈 You're doing great! Consider diversifying investments")
    elif score >= 60:
        recommendations.append("💡 Increase your savings rate by 10% this month")
    else:
        recommendations.append("🚨 Review all subscriptions and cut unnecessary expenses")
        recommendations.append("💼 Look for ways to increase your income")
    
    return recommendations


def analyze_spending_patterns(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze spending patterns and categorize expenses"""
    
    # Categorize transactions
    categories = {
        'Food & Dining': ['restaurant', 'food', 'zomato', 'swiggy', 'cafe'],
        'Shopping': ['amazon', 'flipkart', 'mall', 'store', 'shopping'],
        'Entertainment': ['netflix', 'spotify', 'prime', 'movie', 'game'],
        'Bills & Utilities': ['electricity', 'water', 'gas', 'internet', 'phone'],
        'Transportation': ['uber', 'ola', 'fuel', 'petrol', 'metro'],
        'Healthcare': ['hospital', 'pharmacy', 'doctor', 'medical'],
        'Other': []
    }
    
    spending_by_category = {cat: 0 for cat in categories.keys()}
    
    for txn in transactions:
        if txn.get('type') != 'debit':
            continue
        
        amount = abs(txn.get('amount', 0))
        recipient = (txn.get('recipient') or '').lower()
        
        categorized = False
        for category, keywords in categories.items():
            if any(keyword in recipient for keyword in keywords):
                spending_by_category[category] += amount
                categorized = True
                break
        
        if not categorized:
            spending_by_category['Other'] += amount
    
    # Calculate percentages
    total_spending = sum(spending_by_category.values())
    spending_percentages = {}
    
    if total_spending > 0:
        spending_percentages = {
            cat: round((amt / total_spending) * 100, 1)
            for cat, amt in spending_by_category.items()
            if amt > 0
        }
    
    # Find top spending category
    top_category = max(spending_by_category.items(), key=lambda x: x[1])
    
    return {
        'by_category': spending_by_category,
        'percentages': spending_percentages,
        'total_spending': total_spending,
        'top_category': {
            'name': top_category[0],
            'amount': top_category[1]
        }
    }


def predict_future_balance(current_balance: float, transactions: List[Dict[str, Any]], days: int = 30) -> Dict[str, Any]:
    """Predict future balance based on spending patterns"""
    
    if not transactions:
        return {
            'predicted_balance': current_balance,
            'confidence': 'low',
            'trend': 'stable'
        }
    
    # Calculate average daily income and expenses
    daily_income = 0
    daily_expenses = 0
    
    for txn in transactions:
        amount = txn.get('amount', 0)
        if amount > 0:
            daily_income += amount / len(transactions)
        else:
            daily_expenses += abs(amount) / len(transactions)
    
    # Predict balance
    net_daily = daily_income - daily_expenses
    predicted_balance = current_balance + (net_daily * days)
    
    # Determine trend
    if net_daily > 0:
        trend = 'increasing'
    elif net_daily < 0:
        trend = 'decreasing'
    else:
        trend = 'stable'
    
    # Confidence based on transaction history
    confidence = 'high' if len(transactions) >= 10 else 'medium' if len(transactions) >= 5 else 'low'
    
    return {
        'predicted_balance': round(predicted_balance, 2),
        'current_balance': current_balance,
        'net_daily_change': round(net_daily, 2),
        'prediction_days': days,
        'trend': trend,
        'confidence': confidence
    }


def generate_savings_plan(current_balance: float, monthly_income: float, goal_amount: float, months: int = 12) -> Dict[str, Any]:
    """Generate a savings plan to reach a financial goal"""
    
    required_monthly = goal_amount / months
    savings_rate = (required_monthly / monthly_income) * 100 if monthly_income > 0 else 0
    
    # Check if goal is achievable
    achievable = savings_rate <= 50  # Shouldn't save more than 50% typically
    
    milestones = []
    for month in range(1, months + 1):
        milestone_amount = (goal_amount / months) * month
        milestones.append({
            'month': month,
            'target': round(milestone_amount, 2),
            'monthly_save': round(required_monthly, 2)
        })
    
    return {
        'goal_amount': goal_amount,
        'months': months,
        'required_monthly': round(required_monthly, 2),
        'savings_rate_percentage': round(savings_rate, 1),
        'achievable': achievable,
        'milestones': milestones[:3],  # First 3 milestones
        'recommendation': f"Save ₹{required_monthly:,.0f} per month ({savings_rate:.1f}% of income)" if achievable else "Goal may be too aggressive. Consider extending timeline or reducing amount."
    }


def get_ai_financial_advice(query: str, user_data: Dict[str, Any]) -> str:
    """
    Use AI to provide personalized financial advice
    Falls back to rule-based if OpenAI not available
    """
    
    if OPENAI_AVAILABLE and openai.api_key:
        try:
            # Create context from user data
            context = f"""
User Financial Context:
- Current Balance: ₹{user_data.get('balance', 0):,.2f}
- Monthly Income (estimated): ₹{user_data.get('monthly_income', 30000):,.2f}
- Active Loans: {len(user_data.get('loans', []))}
- Recent Transactions: {len(user_data.get('transactions', []))}

User Query: {query}

Provide practical, actionable financial advice in 2-3 sentences. Be specific and helpful.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert financial advisor providing personalized advice."},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"AI advice error: {str(e)}")
    
    # Fallback to rule-based advice
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['save', 'saving', 'savings']):
        return "Start by following the 50-30-20 rule: 50% for needs, 30% for wants, and 20% for savings. Automate your savings by setting up a recurring transfer right after your salary is credited."
    
    elif any(word in query_lower for word in ['invest', 'investment', 'investing']):
        return "Consider starting with low-risk options like Fixed Deposits or Recurring Deposits. Once comfortable, explore mutual funds through SIPs (Systematic Investment Plans) - start small with ₹500-1000 monthly."
    
    elif any(word in query_lower for word in ['loan', 'debt', 'emi']):
        return "Prioritize paying off high-interest debts first (credit cards, personal loans). Try to pay more than the minimum EMI when possible to reduce overall interest. Avoid taking new loans while clearing existing ones."
    
    elif any(word in query_lower for word in ['budget', 'expense', 'spending']):
        return "Track all expenses for a month to understand spending patterns. Use the envelope system: allocate specific amounts for categories like food, transport, entertainment. Cut one unnecessary subscription this month."
    
    elif any(word in query_lower for word in ['emergency', 'fund']):
        return "Build an emergency fund covering 3-6 months of expenses. Keep it in a liquid savings account or liquid mutual fund. Start with ₹10,000 and add ₹2,000 monthly until you reach your goal."
    
    elif any(word in query_lower for word in ['tax', 'taxes']):
        return "Maximize tax savings under Section 80C (PPF, ELSS, Life Insurance up to ₹1.5L). Consider NPS for additional ₹50K deduction under 80CCD. Claim HRA if paying rent. Maintain medical insurance for Section 80D benefits."
    
    else:
        return "For personalized advice, I recommend: 1) Track your expenses regularly, 2) Create a realistic budget, 3) Build an emergency fund, 4) Start investing early even with small amounts. Would you like specific advice on any of these topics?"


if __name__ == '__main__':
    # Test the module
    print("=== Testing Financial Advisor Module ===\n")
    
    test_data = {
        'balance': 25430.50,
        'monthly_income': 35000,
        'loans': [{'amount': 500000, 'interest_rate': 8.5}],
        'transactions': [
            {'amount': -2500, 'type': 'debit', 'recipient': 'Amazon'},
            {'amount': 15000, 'type': 'credit', 'recipient': 'Salary'},
            {'amount': -500, 'type': 'debit', 'recipient': 'Rohan Kumar'},
        ]
    }
    
    # Test 1: Financial Health Score
    health = calculate_financial_health_score(test_data)
    print(f"Financial Health Score: {health['score']}/100 ({health['health_level']})")
    print(f"Recommendations: {health['recommendations']}\n")
    
    # Test 2: Spending Analysis
    patterns = analyze_spending_patterns(test_data['transactions'])
    print(f"Spending Analysis: {patterns}\n")
    
    # Test 3: Balance Prediction
    prediction = predict_future_balance(test_data['balance'], test_data['transactions'])
    print(f"30-Day Prediction: ₹{prediction['predicted_balance']:,.2f} ({prediction['trend']})\n")
    
    # Test 4: Savings Plan
    plan = generate_savings_plan(test_data['balance'], test_data['monthly_income'], 100000, 12)
    print(f"Savings Plan: {plan['recommendation']}")

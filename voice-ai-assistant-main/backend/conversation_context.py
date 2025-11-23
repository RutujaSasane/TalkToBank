"""
Conversation Context Management
Tracks conversation history for context-aware responses
"""
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# In-memory conversation storage (in production, use Redis or database)
conversation_sessions = {}


class ConversationContext:
    """Manages conversation context for a user session"""
    
    def __init__(self, user_id: int, max_history: int = 10):
        self.user_id = user_id
        self.max_history = max_history
        self.messages: List[Dict[str, Any]] = []
        self.current_intent: Optional[str] = None
        self.pending_entities: Dict[str, Any] = {}
        self.language: str = 'en'
    
    def add_message(self, role: str, text: str, intent: Optional[str] = None, entities: Optional[Dict] = None):
        """Add a message to conversation history"""
        message = {
            'role': role,  # 'user' or 'assistant'
            'text': text,
            'intent': intent,
            'entities': entities or {},
            'timestamp': datetime.now().isoformat()
        }
        self.messages.append(message)
        
        # Keep only last max_history messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        
        if intent:
            self.current_intent = intent
        if entities:
            self.pending_entities.update(entities)
    
    def get_recent_context(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get recent conversation context"""
        return self.messages[-limit:] if len(self.messages) > limit else self.messages
    
    def get_pending_entities(self) -> Dict[str, Any]:
        """Get entities that are pending from previous messages"""
        return self.pending_entities.copy()
    
    def clear_pending_entities(self):
        """Clear pending entities after successful operation"""
        self.pending_entities = {}
    
    def needs_clarification(self, intent: str, entities: Dict[str, Any]) -> tuple:
        """
        Check if clarification is needed based on intent and entities
        Returns: (needs_clarification, clarification_message)
        """
        if intent == 'transfer_funds':
            if not entities.get('amount'):
                return True, "How much would you like to transfer?"
            if not entities.get('recipient'):
                return True, "Who would you like to transfer money to?"
        
        elif intent == 'set_reminder':
            if not entities.get('message'):
                return True, "What would you like to be reminded about?"
        
        elif intent == 'transaction_history':
            # This is optional, so no clarification needed
            pass
        
        return False, None
    
    def enhance_entities_from_context(self, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance entities using conversation context
        """
        enhanced = entities.copy()
        
        # If amount is missing but mentioned in recent context
        if intent == 'transfer_funds' and not enhanced.get('amount'):
            for msg in reversed(self.messages[-3:]):
                if msg.get('entities', {}).get('amount'):
                    enhanced['amount'] = msg['entities']['amount']
                    break
        
        # If recipient is missing but mentioned in recent context
        if intent == 'transfer_funds' and not enhanced.get('recipient'):
            for msg in reversed(self.messages[-3:]):
                if msg.get('entities', {}).get('recipient'):
                    enhanced['recipient'] = msg['entities']['recipient']
                    break
        
        return enhanced
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary"""
        return {
            'user_id': self.user_id,
            'messages': self.messages,
            'current_intent': self.current_intent,
            'pending_entities': self.pending_entities,
            'language': self.language
        }


def get_conversation_context(user_id: int) -> ConversationContext:
    """Get or create conversation context for user"""
    if user_id not in conversation_sessions:
        conversation_sessions[user_id] = ConversationContext(user_id)
    return conversation_sessions[user_id]


def clear_conversation_context(user_id: int):
    """Clear conversation context for user"""
    if user_id in conversation_sessions:
        del conversation_sessions[user_id]


def cleanup_old_sessions(max_age_hours: int = 24):
    """Clean up old conversation sessions"""
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    to_remove = []
    
    for user_id, context in conversation_sessions.items():
        if context.messages:
            last_message_time = datetime.fromisoformat(context.messages[-1]['timestamp'])
            if last_message_time < cutoff:
                to_remove.append(user_id)
    
    for user_id in to_remove:
        del conversation_sessions[user_id]
        logger.info(f"Cleaned up old session for user {user_id}")


if __name__ == '__main__':
    # Test conversation context
    context = ConversationContext(user_id=1)
    
    context.add_message('user', 'check my balance', 'check_balance', {})
    context.add_message('assistant', 'Your balance is ₹25,430.50', 'check_balance', {})
    
    context.add_message('user', 'transfer 500', 'transfer_funds', {'amount': 500})
    needs_clar, msg = context.needs_clarification('transfer_funds', {'amount': 500})
    print(f"Needs clarification: {needs_clar}, Message: {msg}")
    
    context.add_message('user', 'to Rohan', 'transfer_funds', {'recipient': 'Rohan'})
    enhanced = context.enhance_entities_from_context('transfer_funds', {'recipient': 'Rohan'})
    print(f"Enhanced entities: {enhanced}")


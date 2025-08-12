from typing import Dict, Any, List
from tools.llm_manager import get_llm_response
from prompts.email_prompts import get_sms_generation_prompt

def generate_sms(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any],
    num_sms: int,
    tone: str
) -> List[Dict[str, Any]]:
    """
    Generate SMS content for marketing campaign
    
    Args:
        brand_analysis: Brand analysis data
        campaign_plan: Campaign plan with strategy and structure
        num_sms: Number of SMS messages to generate
        tone: SMS tone/voice
    
    Returns:
        List of SMS objects with message content and metadata
    """
    
    sms_messages = []
    sms_sequence = campaign_plan.get("sms_sequence", [])
    
    for i in range(num_sms):
        # Get SMS plan for this sequence
        sms_plan = sms_sequence[i] if i < len(sms_sequence) else {
            "sms_number": i + 1,
            "purpose": "Follow-up",
            "focus": "Continued engagement"
        }
        
        # Generate individual SMS
        sms = generate_single_sms(
            brand_analysis=brand_analysis,
            campaign_plan=campaign_plan,
            sms_plan=sms_plan,
            tone=tone,
            sequence_number=i + 1
        )
        
        sms_messages.append(sms)
    
    return sms_messages

def generate_single_sms(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any],
    sms_plan: Dict[str, Any],
    tone: str,
    sequence_number: int
) -> Dict[str, Any]:
    """Generate a single SMS message"""
    
    # Build SMS generation prompt
    sms_prompt = get_sms_generation_prompt(
        brand_analysis=brand_analysis,
        campaign_plan=campaign_plan,
        sms_plan=sms_plan,
        tone=tone,
        sequence_number=sequence_number
    )
    
    # Get SMS content from LLM
    sms_response = get_llm_response(
        prompt=sms_prompt,
        system_message="You are an expert SMS marketing copywriter. Create concise, compelling SMS messages that drive action within character limits."
    )
    
    # Parse SMS response
    sms = parse_sms_response(sms_response, sms_plan, sequence_number)
    
    return sms

def parse_sms_response(sms_text: str, sms_plan: Dict[str, Any], sequence_number: int) -> Dict[str, Any]:
    """Parse LLM response into structured SMS format"""
    
    # Extract the main SMS message
    message = extract_sms_message(sms_text)
    
    # Ensure message is within SMS character limits
    message = optimize_sms_length(message)
    
    sms = {
        "sequence_number": sequence_number,
        "purpose": sms_plan.get("purpose", "Engagement"),
        "focus": sms_plan.get("focus", "General"),
        "message": message,
        "character_count": len(message),
        "link_included": check_for_link(message),
        "extract_sms" :extract_sms_message(message),
        "personalization": extract_sms_personalization(message),
        "timing": get_sms_timing(sms_plan),
        "compliance": check_sms_compliance(message),
        "full_response": sms_text
    }
    
    return sms

# def extract_sms_message(sms_text: str) -> str:
#     """Extract the main SMS message from LLM response"""
    
#     lines = sms_text.split('\n')
    
#     # Look for SMS message indicators
#     for line in lines:
#         line_clean = line.strip()
#         if line_clean.lower().startswith('sms:'):
#             return line_clean.split(':', 1)[1].strip()
#         elif line_clean.lower().startswith('message:'):
#             return line_clean.split(':', 1)[1].strip()
#         elif '**SMS:**' in line:
#             return line.split('**SMS:**')[1].split('**')[0].strip()
    
#     # Find the longest line that looks like an SMS message
#     potential_messages = []
#     for line in lines:
#         line_clean = line.strip()
#         if line_clean and len(line_clean) > 20 and len(line_clean) < 160:
#             # Remove any markdown formatting
#             clean_line = line_clean.replace('**', '').replace('*', '')
#             potential_messages.append(clean_line)
    
#     if potential_messages:
#         return potential_messages[0]
    
#     # Default message if nothing found
#     return "Special offer just for you! Don't miss out. Text STOP to opt out."

def extract_sms_message(text: str) -> str:
    """
    Extract SMS message content following the 'SMS:' prefix.
    Returns the message without the 'SMS:' part.
    """
    for line in text.split('\n'):
        line = line.strip()
        if line.lower().startswith('sms:'):
            return line.split(':', 1)[1].strip()
    return ""  # Return empty if not found






def optimize_sms_length(message: str) -> str:
    """Optimize SMS message length for best delivery"""
    
    # Standard SMS limit is 160 characters
    # We aim for 140 to leave room for personalization and links
    max_length = 140
    
    if len(message) <= max_length:
        return message
    
    # Try to shorten without losing meaning
    shortened = message
    
    # Remove extra spaces
    shortened = ' '.join(shortened.split())
    
    # Replace common long words with shorter alternatives
    replacements = {
        'because': 'bc',
        'you are': "you're",
        'cannot': "can't",
        'will not': "won't",
        'do not': "don't",
        'and': '&',
        'discount': 'deal',
        'limited time': 'limited',
        'exclusive': 'special'
    }
    
    for long_word, short_word in replacements.items():
        shortened = shortened.replace(long_word, short_word)
        if len(shortened) <= max_length:
            break
    
    # If still too long, truncate and add ...
    if len(shortened) > max_length:
        shortened = shortened[:max_length-3] + "..."
    
    return shortened

def check_for_link(message: str) -> bool:
    """Check if SMS contains a link"""
    link_indicators = ['http', 'www.', '.com', 'link', 'click here']
    return any(indicator in message.lower() for indicator in link_indicators)

def extract_sms_personalization(message: str) -> List[str]:
    """Extract personalization tags from SMS"""
    
    personalization_tags = []
    
    # Common SMS personalization patterns
    patterns = [
        "{{name}}", "{{first_name}}", "{{last_name}}",
        "{{product}}", "{{discount}}", "{{code}}",
        "{{brand}}", "{{offer}}"
    ]
    
    for pattern in patterns:
        if pattern in message.lower():
            personalization_tags.append(pattern)
    
    return personalization_tags

def get_sms_timing(sms_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Get timing information for SMS"""
    
    timing = {
        "sequence_position": sms_plan.get("sms_number", 1),
        "send_after_hours": get_sms_delay(sms_plan.get("sms_number", 1)),
        "best_send_time": "2:00 PM",  # SMS typically perform better in afternoon
        "optimal_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
        "time_zone_consideration": True
    }
    
    return timing

def get_sms_delay(sms_number: int) -> int:
    """Get send delay in hours for SMS based on sequence position"""
    
    # SMS delays are typically shorter than email delays
    delays = {
        1: 2,      # 2 hours after trigger
        2: 48,     # 2 days
        3: 168,    # 1 week
        4: 336,    # 2 weeks
        5: 504,    # 3 weeks
    }
    
    return delays.get(sms_number, 168 * sms_number)

def check_sms_compliance(message: str) -> Dict[str, Any]:
    """Check SMS compliance requirements"""
    
    compliance = {
        "opt_out_included": check_opt_out(message),
        "brand_identified": True,  # Assume brand is identified in context
        "no_spam_words": check_spam_words(message),
        "character_compliant": len(message) <= 160,
        "time_restriction_noted": True
    }
    
    return compliance

def check_opt_out(message: str) -> bool:
    """Check if SMS includes opt-out instructions"""
    opt_out_phrases = ['text stop', 'reply stop', 'stop to opt', 'unsubscribe']
    return any(phrase in message.lower() for phrase in opt_out_phrases)

def check_spam_words(message: str) -> bool:
    """Check for common SMS spam words"""
    spam_words = [
        'free money', 'guaranteed', 'no obligation', 'risk free',
        'act now', 'limited time', 'urgent', 'winner', 'congratulations'
    ]
    
    message_lower = message.lower()
    spam_count = sum(1 for word in spam_words if word in message_lower)
    
    # Return True if spam words are minimal (less than 20% of message)
    return spam_count < 2

def add_sms_shortcodes(sms: Dict[str, Any], brand_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Add SMS shortcode functionality"""
    
    # Add keyword response options
    sms["keywords"] = {
        "YES": "Opt-in confirmation",
        "STOP": "Opt-out from messages",
        "HELP": "Customer service information",
        "INFO": "Product information"
    }
    
    # Add response tracking
    sms["tracking"] = {
        "open_tracking": False,  # SMS doesn't support open tracking
        "click_tracking": True,   # If links are included
        "response_tracking": True,
        "conversion_tracking": True
    }
    
    return sms

def create_sms_variants(base_sms: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create A/B test variants of SMS"""
    
    variants = [base_sms]
    
    original_message = base_sms["message"]
    
    # Create urgency variant
    urgency_message = add_urgency_to_sms(original_message)
    if urgency_message != original_message:
        urgency_variant = base_sms.copy()
        urgency_variant["message"] = urgency_message
        urgency_variant["variant"] = "urgency"
        variants.append(urgency_variant)
    
    # Create emoji variant
    emoji_message = add_emojis_to_sms(original_message)
    if emoji_message != original_message:
        emoji_variant = base_sms.copy()
        emoji_variant["message"] = emoji_message
        emoji_variant["variant"] = "emoji"
        variants.append(emoji_variant)
    
    return variants

def add_urgency_to_sms(message: str) -> str:
    """Add urgency elements to SMS message"""
    urgency_phrases = ["Limited time!", "Hurry!", "Today only!", "Don't miss out!"]
    
    # Add urgency if not already present
    if not any(phrase.lower() in message.lower() for phrase in urgency_phrases):
        return f"{urgency_phrases[0]} {message}"
    
    return message

def add_emojis_to_sms(message: str) -> str:
    """Add relevant emojis to SMS message"""
    
    # Simple emoji mapping
    emoji_map = {
        'sale': '🔥',
        'discount': '💸',
        'new': '✨',
        'free': '🎁',
        'limited': '⏰',
        'exclusive': '⭐'
    }
    
    message_lower = message.lower()
    for word, emoji in emoji_map.items():
        if word in message_lower and emoji not in message:
            # Add emoji at the beginning
            return f"{emoji} {message}"
    
    return message

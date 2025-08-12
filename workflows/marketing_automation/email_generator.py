from typing import Dict, Any, List
from tools.llm_manager import get_llm_response
from prompts.email_prompts import get_email_generation_prompt

def generate_emails(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any],
    num_emails: int,
    tone: str
) -> List[Dict[str, Any]]:
    """
    Generate complete email content for marketing campaign
    
    Args:
        brand_analysis: Brand analysis data
        campaign_plan: Campaign plan with strategy and structure
        num_emails: Number of emails to generate
        tone: Email tone/voice
    
    Returns:
        List of complete email objects with subject, body, CTA, etc.
    """
    
    emails = []
    email_sequence = campaign_plan.get("email_sequence", [])
    
    for i in range(num_emails):
        # Get email plan for this sequence
        email_plan = email_sequence[i] if i < len(email_sequence) else {
            "email_number": i + 1,
            "purpose": "Follow-up",
            "focus": "Continued engagement"
        }
        
        # Generate individual email
        email = generate_single_email(
            brand_analysis=brand_analysis,
            campaign_plan=campaign_plan,
            email_plan=email_plan,
            tone=tone,
            sequence_number=i + 1
        )
        
        emails.append(email)
    
    return emails

def generate_single_email(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any],
    email_plan: Dict[str, Any],
    tone: str,
    sequence_number: int
) -> Dict[str, Any]:
    """Generate a single email in the sequence"""
    
    # Build email generation prompt
    email_prompt = get_email_generation_prompt(
        brand_analysis=brand_analysis,
        campaign_plan=campaign_plan,
        email_plan=email_plan,
        tone=tone,
        sequence_number=sequence_number
    )
    
    # Get email content from LLM
    email_response = get_llm_response(
        prompt=email_prompt,
        system_message="You are an expert email copywriter specializing in conversion-focused marketing emails. Create compelling, engaging email content."
    )
    
    # Parse email response into structured format
    email = parse_email_response(email_response, email_plan, sequence_number)
    
    return email

def parse_email_response(email_text: str, email_plan: Dict[str, Any], sequence_number: int) -> Dict[str, Any]:
    """Parse LLM response into structured email format"""
    
    email = {
        "sequence_number": sequence_number,
        "purpose": email_plan.get("purpose", "Engagement"),
        "focus": email_plan.get("focus", "General"),
        "subject": extract_subject_line(email_text),
        "preview_text": extract_preview_text(email_text),
        "body": extract_email_body(email_text),
        "cta": extract_call_to_action(email_text),
        "personalization": extract_personalization_tags(email_text),
        "timing": get_email_timing(email_plan),
        "full_content": email_text
    }
    
    return email

def extract_subject_line(email_text: str) -> str:
    """Extract subject line from email content"""
    
    lines = email_text.split('\n')
    
    # Look for subject line indicators
    for line in lines:
        line_clean = line.strip()
        if line_clean.lower().startswith('subject:'):
            return line_clean.split(':', 1)[1].strip()
        elif line_clean.lower().startswith('subject line:'):
            return line_clean.split(':', 1)[1].strip()
        elif '**Subject:**' in line:
            return line.split('**Subject:**')[1].split('**')[0].strip()
        elif 'Subject:' in line and len(line.strip()) < 100:
            return line.split('Subject:')[1].strip()
    
    # Look for first line that could be a subject
    for line in lines[:5]:
        line_clean = line.strip()
        if line_clean and len(line_clean) < 80 and not line_clean.startswith('#'):
            return line_clean
    
    return "Don't miss out - special offer inside!"

def extract_preview_text(email_text: str) -> str:
    """Extract preview text from email content"""
    
    lines = email_text.split('\n')
    
    # Look for preview text indicators
    for line in lines:
        line_clean = line.strip()
        if line_clean.lower().startswith('preview:'):
            return line_clean.split(':', 1)[1].strip()
        elif '**Preview:**' in line:
            return line.split('**Preview:**')[1].split('**')[0].strip()
    
    # Extract first sentence of body as preview
    body = extract_email_body(email_text)
    if body:
        sentences = body.split('.')
        if sentences:
            preview = sentences[0].strip()
            return preview[:90] + "..." if len(preview) > 90 else preview
    
    return "Important message inside - don't miss this!"

def extract_email_body(email_text: str) -> str:
    """Extract main email body content"""
    
    # Remove first line if it starts with 'here'
    lines = email_text.split('\n')
    if lines and lines[0].strip().lower().startswith("here"):
        lines = lines[1:]
    
    body_lines = []
    
    # Skip headers and find body content
    for line in lines:
        line_clean = line.strip()
        
        # Skip subject, preview, and other header elements
        if any(header in line_clean.lower() for header in ['subject:', 'preview:', 'from:', 'to:']):
            continue
        
        # Skip markdown headers
        if line_clean.startswith('#'):
            continue
        
        # Skip CTA sections
        if any(cta in line_clean.lower() for cta in ['cta:', 'call to action:', 'button:']):
            break
        
        # Collect body content
        if line_clean:
            body_lines.append(line_clean)
    
    # Join body lines and clean up
    body = '\n\n'.join(body_lines)
    
    # Remove any remaining markdown formatting
    body = body.replace('**', '').replace('*', '')
    
    return body.strip()

def extract_call_to_action(email_text: str) -> Dict[str, str]:
    """Extract call-to-action from email content"""
    
    lines = email_text.split('\n')
    
    # Look for CTA indicators
    for line in lines:
        line_clean = line.strip()
        if line_clean.lower().startswith('cta:'):
            cta_text = line_clean.split(':', 1)[1].strip()
            return {"text": cta_text, "url": "[DYNAMIC_URL]"}
        elif '**CTA:**' in line:
            cta_text = line.split('**CTA:**')[1].split('**')[0].strip()
            return {"text": cta_text, "url": "[DYNAMIC_URL]"}
        elif 'call to action:' in line.lower():
            cta_text = line.lower().split('call to action:')[1].strip()
            return {"text": cta_text, "url": "[DYNAMIC_URL]"}
    
    # Look for button-like text in the email
    cta_patterns = [
        "shop now", "buy now", "get started", "learn more", "claim offer",
        "download", "sign up", "subscribe", "view product", "complete purchase"
    ]
    
    for line in lines:
        line_lower = line.lower()
        for pattern in cta_patterns:
            if pattern in line_lower:
                return {"text": pattern.title(), "url": "[DYNAMIC_URL]"}
    
    return {"text": "Shop Now", "url": "[DYNAMIC_URL]"}

def extract_personalization_tags(email_text: str) -> List[str]:
    """Extract personalization tags from email content"""
    
    personalization_tags = []
    
    # Common personalization patterns
    patterns = [
        "{{first_name}}", "{{name}}", "{{customer_name}}",
        "{{product_name}}", "{{brand_name}}", "{{location}}",
        "{{cart_items}}", "{{last_purchase}}", "{{savings}}"
    ]
    
    for pattern in patterns:
        if pattern in email_text.lower():
            personalization_tags.append(pattern)
    
    # Add default personalization
    if not personalization_tags:
        personalization_tags = ["{{first_name}}", "{{product_name}}"]
    
    return personalization_tags

def get_email_timing(email_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Get timing information for email"""
    
    timing = {
        "sequence_position": email_plan.get("email_number", 1),
        "send_after_hours": get_send_delay(email_plan.get("email_number", 1)),
        "best_send_time": "10:00 AM",
        "optimal_days": ["Tuesday", "Wednesday", "Thursday"]
    }
    
    return timing

def get_send_delay(email_number: int) -> int:
    """Get send delay in hours based on email sequence position"""
    
    # Standard delays for email sequences
    delays = {
        1: 1,      # 1 hour after trigger
        2: 24,     # 1 day
        3: 72,     # 3 days
        4: 168,    # 1 week
        5: 336,    # 2 weeks
    }
    
    return delays.get(email_number, 168 * email_number)  # Default to weekly after email 5

def add_dynamic_content_blocks(email: Dict[str, Any], brand_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Add dynamic content blocks to email"""
    
    # Add product recommendations
    email["product_recommendations"] = {
        "enabled": True,
        "max_products": 3,
        "logic": "related_to_cart" if "cart" in email["purpose"].lower() else "bestsellers"
    }
    
    # Add social proof
    email["social_proof"] = {
        "customer_reviews": True,
        "purchase_count": True,
        "star_rating": True
    }
    
    # Add urgency elements
    if "urgency" in email["focus"].lower() or email["sequence_number"] >= 3:
        email["urgency"] = {
            "countdown_timer": True,
            "stock_level": True,
            "limited_time": True
        }
    
    return email

def optimize_email_for_mobile(email: Dict[str, Any]) -> Dict[str, Any]:
    """Optimize email content for mobile devices"""
    
    # Ensure subject line is mobile-friendly
    if len(email["subject"]) > 40:
        email["mobile_subject"] = email["subject"][:37] + "..."
    else:
        email["mobile_subject"] = email["subject"]
    
    # Add mobile-specific formatting
    email["mobile_optimized"] = True
    email["responsive_design"] = True
    
    return email

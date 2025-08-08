from typing import Dict, Any

def get_email_generation_prompt(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any],
    email_plan: Dict[str, Any],
    tone: str,
    sequence_number: int
) -> str:
    """
    Generate comprehensive prompt for email content creation
    
    Args:
        brand_analysis: Brand analysis data
        campaign_plan: Campaign strategy and plan
        email_plan: Specific email plan details
        tone: Email tone/voice
        sequence_number: Position in email sequence
    
    Returns:
        Detailed prompt for email generation
    """
    
    brand_name = brand_analysis.get("brand_name", "Brand")
    brand_description = brand_analysis.get("description", "")
    products = brand_analysis.get("products", [])
    target_audience = campaign_plan.get("target_audience", "customers")
    campaign_type = campaign_plan.get("campaign_type", "Marketing")
    email_purpose = email_plan.get("purpose", "Engagement")
    email_focus = email_plan.get("focus", "General")
    
    prompt = f"""
    Create a high-converting email for {brand_name}'s {campaign_type.lower()} campaign.
    
    BRAND CONTEXT:
    - Brand: {brand_name}
    - Description: {brand_description}
    - Products/Services: {', '.join(products[:3])}
    - Target Audience: {target_audience}
    - Brand Tone: {tone}
    
    EMAIL DETAILS:
    - Email #{sequence_number} in sequence
    - Purpose: {email_purpose}
    - Focus: {email_focus}
    - Campaign Type: {campaign_type}
    
    REQUIREMENTS:
    1. Subject Line: Create a compelling subject line (40-50 characters)
    2. Preview Text: Write preview text that complements the subject (90-120 characters)
    3. Email Body: Write engaging body content (150-300 words)
    4. Call-to-Action: Include a clear, compelling CTA
    5. Personalization: Use {{{{first_name}}}} and other relevant tokens
    
    EMAIL STRUCTURE:
    - Hook: Start with attention-grabbing opening
    - Value: Clearly communicate value proposition
    - Urgency: Create appropriate urgency for action
    - Social Proof: Include trust elements if relevant
    - CTA: Clear, action-oriented call-to-action
    
    TONE GUIDELINES:
    - {tone}: Maintain {tone.lower()} tone throughout
    - Conversational: Write as if speaking to a friend
    - Benefit-focused: Emphasize customer benefits
    - Scannable: Use short paragraphs and bullet points
    
    CAMPAIGN-SPECIFIC NOTES:
    {get_campaign_specific_guidance(campaign_type, sequence_number)}
    
    OUTPUT FORMAT:
    Subject: [Subject line here]
    Preview: [Preview text here]
    
    Dear {{{{first_name}}}},
    
    [Email body content here]
    
    [Call-to-action]
    
    Best regards,
    The {brand_name} Team
    
    Create an email that drives {email_focus.lower()} and encourages action.
    """
    
    return prompt

def get_sms_generation_prompt(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any],
    sms_plan: Dict[str, Any],
    tone: str,
    sequence_number: int
) -> str:
    """
    Generate prompt for SMS content creation
    
    Args:
        brand_analysis: Brand analysis data
        campaign_plan: Campaign strategy and plan
        sms_plan: Specific SMS plan details
        tone: SMS tone/voice
        sequence_number: Position in SMS sequence
    
    Returns:
        Detailed prompt for SMS generation
    """
    
    brand_name = brand_analysis.get("brand_name", "Brand")
    products = brand_analysis.get("products", [])
    target_audience = campaign_plan.get("target_audience", "customers")
    campaign_type = campaign_plan.get("campaign_type", "Marketing")
    sms_purpose = sms_plan.get("purpose", "Engagement")
    sms_focus = sms_plan.get("focus", "General")
    
    prompt = f"""
    Create a high-converting SMS message for {brand_name}'s {campaign_type.lower()} campaign.
    
    BRAND CONTEXT:
    - Brand: {brand_name}
    - Products/Services: {', '.join(products[:2])}
    - Target Audience: {target_audience}
    - Brand Tone: {tone}
    
    SMS DETAILS:
    - SMS #{sequence_number} in sequence
    - Purpose: {sms_purpose}
    - Focus: {sms_focus}
    - Campaign Type: {campaign_type}
    
    SMS REQUIREMENTS:
    - Character Limit: 140 characters (including spaces)
    - Include opt-out: "Text STOP to opt out"
    - Personalization: Use {{{{name}}}} if appropriate
    - Clear CTA: Include actionable next step
    - Urgency: Create appropriate urgency
    
    TONE GUIDELINES:
    - {tone}: Maintain {tone.lower()} tone
    - Concise: Every word must count
    - Direct: Get straight to the point
    - Friendly: Sound human and approachable
    
    SMS BEST PRACTICES:
    - Start with hook or benefit
    - Use emojis sparingly (1-2 max)
    - Include clear value proposition
    - End with strong call-to-action
    - Ensure mobile-friendly language
    
    CAMPAIGN-SPECIFIC GUIDANCE:
    {get_sms_campaign_guidance(campaign_type, sequence_number)}
    
    OUTPUT FORMAT:
    SMS: [Your SMS message here - max 140 characters]
    
    Character Count: [Actual count]
    
    Create an SMS that drives immediate {sms_focus.lower()} and action.
    """
    
    return prompt

def get_campaign_specific_guidance(campaign_type: str, sequence_number: int) -> str:
    """Get campaign-specific guidance for email content"""
    
    guidance_map = {
        "Cart Abandonment": {
            1: "Gentle reminder about items left in cart. Focus on convenience and easy completion.",
            2: "Reinforce product value and benefits. Address potential objections.",
            3: "Create urgency with limited-time offer or stock scarcity.",
            4: "Social proof and testimonials. Show others love the product.",
            5: "Final attempt with strong incentive and last chance messaging."
        },
        "Welcome Series": {
            1: "Warm welcome and brand introduction. Set expectations for future communications.",
            2: "Provide value immediately. Share useful tips or resources.",
            3: "Showcase key products/services. Focus on popular or bestselling items.",
            4: "Build community and encourage engagement. Social media, reviews, etc.",
            5: "Special welcome offer to encourage first purchase."
        },
        "Post-Purchase": {
            1: "Thank you and order confirmation. Build excitement for delivery.",
            2: "Usage tips and how-to guides. Maximize product value.",
            3: "Request review and user-generated content. Build social proof.",
            4: "Cross-sell complementary products based on purchase.",
            5: "Reorder reminder with loyalty discount."
        },
        "Win-Back": {
            1: "We miss you message. Acknowledge absence and express desire to reconnect.",
            2: "Special offer to return. Incentivize re-engagement.",
            3: "Showcase new products or improvements made since last interaction.",
            4: "Exclusive VIP treatment offer. Make them feel special.",
            5: "Final goodbye with last chance offer."
        }
    }
    
    campaign_guidance = guidance_map.get(campaign_type, {})
    specific_guidance = campaign_guidance.get(sequence_number, "Focus on value delivery and clear call-to-action.")
    
    return specific_guidance

def get_sms_campaign_guidance(campaign_type: str, sequence_number: int) -> str:
    """Get campaign-specific guidance for SMS content"""
    
    sms_guidance_map = {
        "Cart Abandonment": {
            1: "Quick reminder with easy completion link. 'Your items are waiting!'",
            2: "Urgency + incentive. 'Limited stock + 10% off to complete order'",
            3: "Final notice with scarcity. 'Last chance before items sell out'"
        },
        "Welcome Series": {
            1: "Welcome + immediate value. 'Welcome! Here's your instant access link'",
            2: "Engagement + offer. 'Enjoying the app? Get 20% off your first order'"
        },
        "Post-Purchase": {
            1: "Thank you + tracking. 'Order confirmed! Track shipment: [link]'",
            2: "Delivery notification + next steps. 'Package delivered! Start here: [link]'"
        },
        "Win-Back": {
            1: "We miss you + incentive. 'Come back! 30% off waiting for you'",
            2: "Exclusive offer. 'VIP deal just for you - 50% off today only'"
        }
    }
    
    campaign_guidance = sms_guidance_map.get(campaign_type, {})
    specific_guidance = campaign_guidance.get(sequence_number, "Create urgency and drive immediate action.")
    
    return specific_guidance

def get_email_subject_line_variations(
    base_subject: str,
    campaign_type: str,
    sequence_number: int
) -> list:
    """Generate subject line variations for A/B testing"""
    
    variations = [base_subject]
    
    # Add urgency variations
    if sequence_number >= 3:
        urgency_words = ["Urgent", "Last Chance", "Expires Soon", "Final Notice"]
        for word in urgency_words:
            variations.append(f"{word}: {base_subject}")
    
    # Add question variations
    if "?" not in base_subject:
        question_starters = ["Did you forget?", "Still interested?", "Ready to"]
        for starter in question_starters:
            variations.append(f"{starter} {base_subject.lower()}")
    
    # Add personal variations
    personal_variations = [
        f"{{{{first_name}}}}, {base_subject.lower()}",
        f"Personal message for {{{{first_name}}}}",
        f"{{{{first_name}}}}, this is important"
    ]
    variations.extend(personal_variations)
    
    return variations[:5]  # Return top 5 variations

def get_email_personalization_tokens() -> Dict[str, str]:
    """Get available personalization tokens and their descriptions"""
    
    return {
        "{{first_name}}": "Customer's first name",
        "{{last_name}}": "Customer's last name", 
        "{{email}}": "Customer's email address",
        "{{company}}": "Customer's company name",
        "{{city}}": "Customer's city",
        "{{state}}": "Customer's state",
        "{{country}}": "Customer's country",
        "{{product_name}}": "Name of product in cart/purchased",
        "{{product_price}}": "Price of product",
        "{{cart_total}}": "Total cart value",
        "{{order_number}}": "Order number",
        "{{discount_code}}": "Personalized discount code",
        "{{days_since_purchase}}": "Days since last purchase",
        "{{loyalty_points}}": "Customer's loyalty points",
        "{{referral_link}}": "Personal referral link"
    }

def get_email_compliance_guidelines() -> list:
    """Get email compliance guidelines"""
    
    return [
        "Include clear unsubscribe link in footer",
        "Add physical business address",
        "Use clear 'From' name and email address", 
        "Avoid spam trigger words in subject lines",
        "Include plain text version of email",
        "Honor unsubscribe requests within 10 days",
        "Don't use deceptive subject lines",
        "Include company identification",
        "Respect sending frequency preferences",
        "Ensure mobile-responsive design"
    ]

def get_email_timing_recommendations() -> Dict[str, Any]:
    """Get email timing recommendations"""
    
    return {
        "best_days": ["Tuesday", "Wednesday", "Thursday"],
        "best_times": ["10:00 AM", "2:00 PM", "8:00 PM"],
        "avoid_days": ["Monday", "Friday", "Sunday"],
        "avoid_times": ["Before 8:00 AM", "After 10:00 PM"],
        "timezone_considerations": "Send based on recipient's timezone",
        "frequency_limits": {
            "daily": "No more than 1 promotional email",
            "weekly": "2-3 emails maximum",
            "monthly": "8-12 emails maximum"
        },
        "sequence_delays": {
            "welcome": "Immediate, then 1 day, 3 days, 1 week",
            "cart_abandonment": "1 hour, 24 hours, 3 days, 1 week",
            "post_purchase": "1 hour, 1 day, 1 week, 1 month"
        }
    }

def create_email_template_structure(email_type: str) -> Dict[str, str]:
    """Create email template structure based on type"""
    
    templates = {
        "promotional": {
            "header": "Brand logo and navigation",
            "hero": "Eye-catching hero image with main message",
            "content": "Product showcase with benefits and features",
            "social_proof": "Customer testimonials or reviews",
            "cta": "Primary call-to-action button",
            "footer": "Unsubscribe, address, social links"
        },
        "transactional": {
            "header": "Simple brand header",
            "confirmation": "Order/action confirmation details",
            "details": "Specific transaction information",
            "next_steps": "What happens next and when",
            "support": "Customer support contact info",
            "footer": "Legal requirements and contact info"
        },
        "newsletter": {
            "header": "Newsletter branding and date",
            "intro": "Personal message from sender",
            "content_blocks": "Multiple content sections",
            "featured": "Featured product or article",
            "community": "Social media and community highlights",
            "footer": "Archive link, preferences, unsubscribe"
        }
    }
    
    return templates.get(email_type, templates["promotional"])

def get_mobile_optimization_tips() -> list:
    """Get mobile email optimization tips"""
    
    return [
        "Use single column layout",
        "Keep subject lines under 40 characters",
        "Use large, tappable CTA buttons (44px minimum)",
        "Optimize images for small screens",
        "Use larger font sizes (14px minimum)",
        "Keep email width under 600px",
        "Use plenty of white space",
        "Test on multiple devices and email clients",
        "Ensure fast loading times",
        "Use progressive enhancement for advanced features"
    ]

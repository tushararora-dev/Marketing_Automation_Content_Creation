from typing import Dict, Any, List
from tools.llm_manager import get_llm_response
from prompts.brand_analysis_prompts import get_campaign_planning_prompt

def plan_campaign(
    brand_analysis: Dict[str, Any],
    campaign_type: str,
    custom_prompt: str,
    num_emails: int,
    num_sms: int,
    target_audience: str,
    tone: str
) -> Dict[str, Any]:
    """
    Plan a comprehensive marketing campaign based on brand analysis
    
    Args:
        brand_analysis: Analysis of the brand from website
        campaign_type: Type of campaign (cart abandonment, welcome, etc.)
        custom_prompt: Custom instructions
        num_emails: Number of emails to plan
        num_sms: Number of SMS messages to plan
        target_audience: Target audience description
        tone: Campaign tone
    
    Returns:
        Comprehensive campaign plan with strategy and structure
    """
    
    # Build campaign planning prompt
    planning_prompt = get_campaign_planning_prompt(
        brand_analysis=brand_analysis,
        campaign_type=campaign_type,
        custom_prompt=custom_prompt,
        num_emails=num_emails,
        num_sms=num_sms,
        target_audience=target_audience,
        tone=tone
    )
    
    # Get campaign plan from LLM
    plan_response = get_llm_response(
        prompt=planning_prompt,
        system_message="You are an expert marketing strategist specializing in automated campaign planning. Create detailed, actionable campaign plans."
    )
    
    # Parse and structure the campaign plan
    campaign_plan = parse_campaign_plan(plan_response, campaign_type, num_emails, num_sms)
    
    return campaign_plan

def parse_campaign_plan(plan_text: str, campaign_type: str, num_emails: int, num_sms: int) -> Dict[str, Any]:
    """Parse the LLM response into a structured campaign plan"""
    
    # Extract key components from the plan
    campaign_plan = {
        "campaign_type": campaign_type,
        "objective": extract_campaign_objective(plan_text),
        "strategy": extract_campaign_strategy(plan_text),
        "timeline": generate_campaign_timeline(campaign_type, num_emails, num_sms),
        "email_sequence": extract_email_sequence_plan(plan_text, num_emails),
        "sms_sequence": extract_sms_sequence_plan(plan_text, num_sms),
        "triggers": extract_campaign_triggers(plan_text, campaign_type),
        "success_metrics": extract_success_metrics(plan_text),
        "personalization": extract_personalization_strategy(plan_text),
        "full_plan": plan_text
    }
    
    return campaign_plan

def extract_campaign_objective(plan_text: str) -> str:
    """Extract the main campaign objective"""
    # Look for objective keywords in the plan
    objective_keywords = ["objective", "goal", "aim", "purpose"]
    
    lines = plan_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in objective_keywords):
            if ':' in line:
                return line.split(':', 1)[1].strip()
    
    # Default objective based on common campaign types
    return "Increase customer engagement and drive conversions"

def extract_campaign_strategy(plan_text: str) -> str:
    """Extract the overall campaign strategy"""
    # Look for strategy-related content
    strategy_keywords = ["strategy", "approach", "method", "tactic"]
    
    lines = plan_text.split('\n')
    strategy_lines = []
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in strategy_keywords):
            # Collect this line and next few lines as strategy
            strategy_lines.extend(lines[i:i+3])
            break
    
    if strategy_lines:
        return ' '.join(strategy_lines).strip()
    
    return "Multi-touch engagement strategy focusing on value delivery and conversion optimization"

def generate_campaign_timeline(campaign_type: str, num_emails: int, num_sms: int) -> List[Dict[str, Any]]:
    """Generate a timeline for the campaign"""
    
    timeline = []
    
    # Define timing patterns based on campaign type
    timing_patterns = {
        "Cart Abandonment": [
            {"hours": 1, "type": "email"},
            {"hours": 24, "type": "email"},
            {"hours": 48, "type": "sms"},
            {"hours": 72, "type": "email"},
            {"hours": 168, "type": "email"}  # 1 week
        ],
        "Welcome Series": [
            {"hours": 0, "type": "email"},
            {"hours": 24, "type": "email"},
            {"hours": 72, "type": "email"},
            {"hours": 168, "type": "email"},
            {"hours": 336, "type": "email"}  # 2 weeks
        ],
        "Post-Purchase": [
            {"hours": 1, "type": "email"},
            {"hours": 24, "type": "email"},
            {"hours": 168, "type": "email"},  # 1 week
            {"hours": 504, "type": "email"},  # 3 weeks
            {"hours": 720, "type": "sms"}   # 30 days
        ],
        "Win-Back": [
            {"hours": 0, "type": "email"},
            {"hours": 72, "type": "email"},
            {"hours": 168, "type": "sms"},
            {"hours": 336, "type": "email"},
            {"hours": 504, "type": "email"}
        ]
    }
    
    # Get pattern for campaign type or use default
    pattern = timing_patterns.get(campaign_type, timing_patterns["Cart Abandonment"])
    
    # Build timeline based on requested email/SMS counts
    email_count = 0
    sms_count = 0
    
    for item in pattern:
        if item["type"] == "email" and email_count < num_emails:
            timeline.append({
                "sequence": email_count + 1,
                "type": "email",
                "trigger_hours": item["hours"],
                "trigger_description": f"Send email {email_count + 1} after {item['hours']} hours"
            })
            email_count += 1
        elif item["type"] == "sms" and sms_count < num_sms:
            timeline.append({
                "sequence": sms_count + 1,
                "type": "sms",
                "trigger_hours": item["hours"],
                "trigger_description": f"Send SMS {sms_count + 1} after {item['hours']} hours"
            })
            sms_count += 1
    
    return timeline

def extract_email_sequence_plan(plan_text: str, num_emails: int) -> List[Dict[str, str]]:
    """Extract email sequence structure from plan"""
    
    email_plan = []
    
    # Default email sequence based on best practices
    default_sequences = {
        "Cart Abandonment": [
            {"purpose": "Gentle reminder", "focus": "Complete your purchase"},
            {"purpose": "Value reinforcement", "focus": "Product benefits"},
            {"purpose": "Urgency creation", "focus": "Limited time offer"},
            {"purpose": "Social proof", "focus": "Customer reviews"},
            {"purpose": "Final attempt", "focus": "Last chance offer"}
        ],
        "Welcome Series": [
            {"purpose": "Welcome message", "focus": "Thank you and brand introduction"},
            {"purpose": "Value delivery", "focus": "How to get started"},
            {"purpose": "Product education", "focus": "Feature highlights"},
            {"purpose": "Community building", "focus": "Join our community"},
            {"purpose": "First purchase", "focus": "Special welcome offer"}
        ],
        "Post-Purchase": [
            {"purpose": "Order confirmation", "focus": "Thank you and order details"},
            {"purpose": "Usage tips", "focus": "How to use your product"},
            {"purpose": "Review request", "focus": "Share your experience"},
            {"purpose": "Cross-sell", "focus": "Complementary products"},
            {"purpose": "Reorder reminder", "focus": "Time to restock"}
        ]
    }
    
    # Try to extract from plan text or use defaults
    campaign_type = "Cart Abandonment"  # Default
    if "welcome" in plan_text.lower():
        campaign_type = "Welcome Series"
    elif "post-purchase" in plan_text.lower():
        campaign_type = "Post-Purchase"
    
    default_seq = default_sequences.get(campaign_type, default_sequences["Cart Abandonment"])
    
    for i in range(num_emails):
        if i < len(default_seq):
            email_plan.append({
                "email_number": i + 1,
                "purpose": default_seq[i]["purpose"],
                "focus": default_seq[i]["focus"],
                "key_message": f"Email {i + 1}: {default_seq[i]['focus']}"
            })
        else:
            email_plan.append({
                "email_number": i + 1,
                "purpose": "Follow-up",
                "focus": "Continued engagement",
                "key_message": f"Email {i + 1}: Additional follow-up"
            })
    
    return email_plan

def extract_sms_sequence_plan(plan_text: str, num_sms: int) -> List[Dict[str, str]]:
    """Extract SMS sequence structure from plan"""
    
    sms_plan = []
    
    # Default SMS purposes
    sms_purposes = [
        {"purpose": "Urgent reminder", "focus": "Quick action needed"},
        {"purpose": "Special offer", "focus": "Exclusive mobile discount"},
        {"purpose": "Time-sensitive", "focus": "Limited time alert"},
        {"purpose": "Re-engagement", "focus": "We miss you"},
        {"purpose": "Final notice", "focus": "Last opportunity"}
    ]
    
    for i in range(num_sms):
        if i < len(sms_purposes):
            sms_plan.append({
                "sms_number": i + 1,
                "purpose": sms_purposes[i]["purpose"],
                "focus": sms_purposes[i]["focus"],
                "key_message": f"SMS {i + 1}: {sms_purposes[i]['focus']}"
            })
        else:
            sms_plan.append({
                "sms_number": i + 1,
                "purpose": "Additional follow-up",
                "focus": "Continued engagement",
                "key_message": f"SMS {i + 1}: Additional follow-up"
            })
    
    return sms_plan

def extract_campaign_triggers(plan_text: str, campaign_type: str) -> Dict[str, Any]:
    """Extract campaign trigger conditions"""
    
    triggers = {
        "start_trigger": get_start_trigger(campaign_type),
        "conditions": get_trigger_conditions(campaign_type),
        "exclusions": get_trigger_exclusions(campaign_type)
    }
    
    return triggers

def get_start_trigger(campaign_type: str) -> str:
    """Get the start trigger for different campaign types"""
    
    triggers = {
        "Cart Abandonment": "User adds items to cart but doesn't complete purchase within 1 hour",
        "Welcome Series": "User completes signup or first purchase",
        "Post-Purchase": "User completes a purchase",
        "Win-Back": "User has been inactive for 30+ days",
        "Custom": "Custom trigger defined by user"
    }
    
    return triggers.get(campaign_type, "Custom trigger condition")

def get_trigger_conditions(campaign_type: str) -> List[str]:
    """Get trigger conditions for campaign types"""
    
    conditions = {
        "Cart Abandonment": [
            "Cart value > $0",
            "User has email address",
            "User hasn't completed purchase",
            "User isn't in other active campaigns"
        ],
        "Welcome Series": [
            "User has completed signup",
            "User has email address",
            "User isn't in other welcome campaigns"
        ],
        "Post-Purchase": [
            "Purchase completed successfully",
            "User opted in for marketing emails",
            "Order total > $0"
        ],
        "Win-Back": [
            "User last active > 30 days ago",
            "User has made at least one previous purchase",
            "User hasn't opted out"
        ]
    }
    
    return conditions.get(campaign_type, ["Custom conditions apply"])

def get_trigger_exclusions(campaign_type: str) -> List[str]:
    """Get exclusion conditions for campaign types"""
    
    exclusions = [
        "User has opted out of marketing emails",
        "User has hard bounced email address",
        "User is in suppression list",
        "User has completed target action in last 24 hours"
    ]
    
    return exclusions

def extract_success_metrics(plan_text: str) -> List[str]:
    """Extract success metrics from campaign plan"""
    
    default_metrics = [
        "Open rate > 25%",
        "Click-through rate > 3%",
        "Conversion rate > 2%",
        "Revenue per email > $1",
        "Unsubscribe rate < 0.5%"
    ]
    
    return default_metrics

def extract_personalization_strategy(plan_text: str) -> Dict[str, Any]:
    """Extract personalization strategy from plan"""
    
    personalization = {
        "name_personalization": True,
        "product_recommendations": True,
        "behavioral_triggers": True,
        "dynamic_content": [
            "Product images based on cart items",
            "Personalized subject lines",
            "Location-based offers",
            "Purchase history references"
        ],
        "segmentation": [
            "First-time visitors",
            "Returning customers",
            "High-value customers",
            "Inactive users"
        ]
    }
    
    return personalization

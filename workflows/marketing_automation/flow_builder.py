from typing import Dict, Any, List
import json
from datetime import datetime, timedelta

def build_campaign_flow(
    campaign_plan: Dict[str, Any],
    emails: List[Dict[str, Any]],
    sms: List[Dict[str, Any]],
    visuals: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Build the complete campaign flow structure for export to marketing platforms
    
    Args:
        campaign_plan: Campaign strategy and plan
        emails: Generated email content
        sms: Generated SMS content
        visuals: Generated visual assets
    
    Returns:
        Complete campaign flow ready for platform deployment
    """
    
    # Build main flow structure
    campaign_flow = {
        "flow_id": generate_flow_id(campaign_plan),
        "flow_name": generate_flow_name(campaign_plan),
        "flow_type": campaign_plan.get("campaign_type", "Custom"),
        "created_at": datetime.now().isoformat(),
        "status": "draft",
        "triggers": build_flow_triggers(campaign_plan),
        "sequence": build_message_sequence(emails, sms, campaign_plan),
        "segmentation": build_flow_segmentation(campaign_plan),
        "personalization": build_personalization_rules(campaign_plan, emails, sms),
        "timing": build_timing_rules(campaign_plan, emails, sms),
        "assets": organize_flow_assets(visuals, emails, sms),
        "analytics": setup_flow_analytics(campaign_plan),
        "export_formats": generate_export_formats(campaign_plan, emails, sms, visuals)
    }
    
    return campaign_flow

def generate_flow_id(campaign_plan: Dict[str, Any]) -> str:
    """Generate unique flow identifier"""
    campaign_type = campaign_plan.get("campaign_type", "custom").lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{campaign_type}_flow_{timestamp}"

def generate_flow_name(campaign_plan: Dict[str, Any]) -> str:
    """Generate human-readable flow name"""
    campaign_type = campaign_plan.get("campaign_type", "Custom")
    brand_name = campaign_plan.get("brand_name", "Brand")
    return f"{brand_name} - {campaign_type} Campaign"

def build_flow_triggers(campaign_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Build trigger configuration for the flow"""
    
    triggers = campaign_plan.get("triggers", {})
    
    flow_triggers = {
        "entry_trigger": {
            "type": get_trigger_type(campaign_plan.get("campaign_type", "")),
            "conditions": triggers.get("conditions", []),
            "description": triggers.get("start_trigger", "Custom trigger"),
            "delay": "0 minutes"
        },
        "exit_triggers": [
            {
                "type": "goal_achieved",
                "condition": "user_converts",
                "action": "remove_from_flow"
            },
            {
                "type": "user_action",
                "condition": "unsubscribe",
                "action": "remove_from_flow"
            },
            {
                "type": "time_limit",
                "condition": "30_days_elapsed",
                "action": "complete_flow"
            }
        ],
        "exclusions": triggers.get("exclusions", [])
    }
    
    return flow_triggers

def get_trigger_type(campaign_type: str) -> str:
    """Get trigger type based on campaign type"""
    
    trigger_types = {
        "Cart Abandonment": "cart_abandonment",
        "Welcome Series": "user_signup",
        "Post-Purchase": "purchase_completed",
        "Win-Back": "user_inactive",
        "Custom": "custom_event"
    }
    
    return trigger_types.get(campaign_type, "custom_event")

def build_message_sequence(
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]], 
    campaign_plan: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Build the complete message sequence with timing"""
    
    sequence = []
    timeline = campaign_plan.get("timeline", [])
    
    # Combine emails and SMS into chronological sequence
    all_messages = []
    
    # Add emails
    for email in emails:
        timing = email.get("timing", {})
        all_messages.append({
            "type": "email",
            "content": email,
            "delay_hours": timing.get("send_after_hours", 24),
            "sequence_number": email.get("sequence_number", 1)
        })
    
    # Add SMS
    for sms_msg in sms:
        timing = sms_msg.get("timing", {})
        all_messages.append({
            "type": "sms",
            "content": sms_msg,
            "delay_hours": timing.get("send_after_hours", 48),
            "sequence_number": sms_msg.get("sequence_number", 1)
        })
    
    # Sort by delay hours
    all_messages.sort(key=lambda x: x["delay_hours"])
    
    # Build sequence with proper flow structure
    for i, message in enumerate(all_messages):
        sequence_item = {
            "step_id": f"step_{i+1}",
            "step_type": message["type"],
            "step_name": f"{message['type'].title()} {message['sequence_number']}",
            "delay": {
                "type": "time_delay",
                "value": message["delay_hours"],
                "unit": "hours"
            },
            "content": build_message_content_block(message["content"], message["type"]),
            "conditions": build_message_conditions(message["content"], message["type"]),
            "next_step": f"step_{i+2}" if i < len(all_messages) - 1 else "end_flow"
        }
        
        sequence.append(sequence_item)
    
    return sequence

def build_message_content_block(content: Dict[str, Any], message_type: str) -> Dict[str, Any]:
    """Build content block for message in flow"""
    
    if message_type == "email":
        return {
            "subject": content.get("subject", ""),
            "preview_text": content.get("preview_text", ""),
            "body_html": format_email_for_platform(content),
            "body_text": extract_text_version(content.get("body", "")),
            "sender_name": "{{brand_name}}",
            "sender_email": "{{brand_email}}",
            "reply_to": "{{support_email}}",
            "personalization": content.get("personalization", []),
            "cta": content.get("cta", {}),
            "tracking": {
                "opens": True,
                "clicks": True,
                "conversions": True
            }
        }
    
    elif message_type == "sms":
        return {
            "message": content.get("message", ""),
            "sender_id": "{{brand_shortcode}}",
            "personalization": content.get("personalization", []),
            "compliance": content.get("compliance", {}),
            "tracking": {
                "delivery": True,
                "responses": True,
                "conversions": True
            }
        }
    
    return {}

def format_email_for_platform(email: Dict[str, Any]) -> str:
    """Format email content for platform deployment"""
    
    # Basic HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{email.get('subject', 'Email')}</title>
    </head>
    <body style="margin: 0; padding: 20px; font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto;">
            <!-- Header -->
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{{brand_logo}}" alt="{{brand_name}}" style="max-height: 80px;">
            </div>
            
            <!-- Body Content -->
            <div style="line-height: 1.6; color: #333;">
                {format_email_body(email.get('body', ''))}
            </div>
            
            <!-- CTA -->
            {format_email_cta(email.get('cta', {}))}
            
            <!-- Footer -->
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; font-size: 12px; color: #666;">
                <p>{{unsubscribe_link}}</p>
                <p>{{company_address}}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def format_email_body(body: str) -> str:
    """Format email body text for HTML"""
    # Convert line breaks to HTML
    formatted_body = body.replace('\n', '<br>')
    
    # Wrap in paragraphs
    paragraphs = formatted_body.split('<br><br>')
    html_paragraphs = [f"<p>{p}</p>" for p in paragraphs if p.strip()]
    
    return ''.join(html_paragraphs)

def format_email_cta(cta: Dict[str, str]) -> str:
    """Format CTA button for HTML"""
    if not cta or not cta.get("text"):
        return ""
    
    return f"""
    <div style="text-align: center; margin: 30px 0;">
        <a href="{cta.get('url', '#')}" 
           style="display: inline-block; padding: 15px 30px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
            {cta.get('text', 'Click Here')}
        </a>
    </div>
    """

def extract_text_version(html_body: str) -> str:
    """Extract plain text version from HTML body"""
    # Simple HTML to text conversion
    text = html_body.replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n\n')
    # Remove other HTML tags (basic approach)
    import re
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def build_message_conditions(content: Dict[str, Any], message_type: str) -> List[Dict[str, Any]]:
    """Build conditions for message delivery"""
    
    conditions = [
        {
            "type": "not_completed_goal",
            "description": "User hasn't converted yet"
        },
        {
            "type": "subscribed",
            "description": "User is subscribed to marketing messages"
        }
    ]
    
    if message_type == "sms":
        conditions.append({
            "type": "sms_consent",
            "description": "User has consented to SMS marketing"
        })
    
    return conditions

def build_flow_segmentation(campaign_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Build segmentation rules for the flow"""
    
    segmentation = {
        "target_segments": [
            {
                "name": "Primary Target",
                "description": campaign_plan.get("target_audience", "General customers"),
                "conditions": build_segment_conditions(campaign_plan)
            }
        ],
        "exclusion_segments": [
            {
                "name": "Recent Converters",
                "description": "Users who converted in last 7 days",
                "conditions": ["converted_in_last_7_days"]
            },
            {
                "name": "Suppressed Users",
                "description": "Users on suppression list",
                "conditions": ["in_suppression_list"]
            }
        ],
        "dynamic_segmentation": True
    }
    
    return segmentation

def build_segment_conditions(campaign_plan: Dict[str, Any]) -> List[str]:
    """Build conditions for target segments"""
    
    conditions = ["email_address_exists"]
    
    campaign_type = campaign_plan.get("campaign_type", "")
    
    if "Cart Abandonment" in campaign_type:
        conditions.extend([
            "has_cart_items",
            "cart_value_greater_than_0",
            "not_purchased_in_last_hour"
        ])
    elif "Welcome" in campaign_type:
        conditions.extend([
            "signed_up_in_last_24_hours",
            "not_in_other_welcome_flows"
        ])
    elif "Post-Purchase" in campaign_type:
        conditions.extend([
            "purchased_in_last_hour",
            "order_total_greater_than_0"
        ])
    elif "Win-Back" in campaign_type:
        conditions.extend([
            "last_active_30_days_ago",
            "previous_purchase_exists"
        ])
    
    return conditions

def build_personalization_rules(
    campaign_plan: Dict[str, Any], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Build personalization rules for the flow"""
    
    # Collect all personalization tags used
    all_tags = set()
    
    for email in emails:
        all_tags.update(email.get("personalization", []))
    
    for sms_msg in sms:
        all_tags.update(sms_msg.get("personalization", []))
    
    personalization = {
        "enabled": True,
        "tags_used": list(all_tags),
        "fallback_values": {
            "{{first_name}}": "there",
            "{{name}}": "valued customer",
            "{{product_name}}": "our product",
            "{{brand_name}}": "our brand"
        },
        "dynamic_content": {
            "product_recommendations": True,
            "location_based": True,
            "behavioral_triggers": True
        },
        "testing": {
            "a_b_testing": True,
            "personalization_lift_tracking": True
        }
    }
    
    return personalization

def build_timing_rules(
    campaign_plan: Dict[str, Any], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Build timing and frequency rules"""
    
    timing = {
        "send_time_optimization": True,
        "timezone_delivery": True,
        "frequency_capping": {
            "max_emails_per_day": 2,
            "max_sms_per_week": 3,
            "respect_quiet_hours": True
        },
        "optimal_send_times": {
            "email": {
                "weekdays": "10:00 AM, 2:00 PM",
                "weekends": "11:00 AM"
            },
            "sms": {
                "weekdays": "2:00 PM, 6:00 PM",
                "weekends": "12:00 PM"
            }
        },
        "delay_rules": extract_delay_rules(emails, sms)
    }
    
    return timing

def extract_delay_rules(emails: List[Dict[str, Any]], sms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract delay rules from message timing"""
    
    rules = []
    
    for email in emails:
        timing = email.get("timing", {})
        rules.append({
            "message_type": "email",
            "sequence_number": email.get("sequence_number", 1),
            "delay_hours": timing.get("send_after_hours", 24),
            "description": f"Send email {email.get('sequence_number', 1)} after {timing.get('send_after_hours', 24)} hours"
        })
    
    for sms_msg in sms:
        timing = sms_msg.get("timing", {})
        rules.append({
            "message_type": "sms",
            "sequence_number": sms_msg.get("sequence_number", 1),
            "delay_hours": timing.get("send_after_hours", 48),
            "description": f"Send SMS {sms_msg.get('sequence_number', 1)} after {timing.get('send_after_hours', 48)} hours"
        })
    
    return rules

def organize_flow_assets(
    visuals: List[Dict[str, Any]], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Organize all assets for the flow"""
    
    assets = {
        "visual_assets": {
            "email_headers": [v for v in visuals if v.get("type") == "email_header"],
            "product_images": [v for v in visuals if v.get("type") == "product_showcase"],
            "social_proof": [v for v in visuals if v.get("type") == "social_proof"],
            "cta_buttons": [v for v in visuals if v.get("type") == "cta_button"],
            "trust_badges": [v for v in visuals if v.get("type") == "trust_badges"]
        },
        "content_assets": {
            "email_templates": len(emails),
            "sms_templates": len(sms),
            "personalization_tags": extract_all_personalization_tags(emails, sms)
        },
        "export_ready": True,
        "asset_count": len(visuals) + len(emails) + len(sms)
    }
    
    return assets

def extract_all_personalization_tags(emails: List[Dict[str, Any]], sms: List[Dict[str, Any]]) -> List[str]:
    """Extract all unique personalization tags"""
    
    tags = set()
    
    for email in emails:
        tags.update(email.get("personalization", []))
    
    for sms_msg in sms:
        tags.update(sms_msg.get("personalization", []))
    
    return sorted(list(tags))

def setup_flow_analytics(campaign_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Setup analytics and tracking for the flow"""
    
    analytics = {
        "tracking_enabled": True,
        "kpis": [
            "open_rate",
            "click_through_rate",
            "conversion_rate",
            "revenue_per_email",
            "unsubscribe_rate"
        ],
        "goals": [
            {
                "name": "Primary Conversion",
                "description": "Complete purchase",
                "value": "purchase_completed"
            },
            {
                "name": "Engagement",
                "description": "Click email CTA",
                "value": "email_click"
            }
        ],
        "attribution": {
            "window": "7_days",
            "model": "last_click"
        },
        "reporting": {
            "frequency": "daily",
            "stakeholders": ["marketing_team", "management"]
        }
    }
    
    return analytics

def generate_export_formats(
    campaign_plan: Dict[str, Any], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]], 
    visuals: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate export formats for different platforms"""
    
    export_formats = {
        "klaviyo": generate_klaviyo_export(campaign_plan, emails, sms, visuals),
        "mailchimp": generate_mailchimp_export(campaign_plan, emails, sms),
        "hubspot": generate_hubspot_export(campaign_plan, emails, sms),
        "generic_csv": generate_csv_export(emails, sms),
        "json": generate_json_export(campaign_plan, emails, sms, visuals)
    }
    
    return export_formats

def generate_klaviyo_export(
    campaign_plan: Dict[str, Any], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]], 
    visuals: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate Klaviyo-specific export format"""
    
    klaviyo_flow = {
        "flow_name": generate_flow_name(campaign_plan),
        "trigger_filters": build_klaviyo_triggers(campaign_plan),
        "flow_filters": build_klaviyo_filters(campaign_plan),
        "messages": [],
        "settings": {
            "smart_sending": True,
            "quiet_hours": {"start": "22:00", "end": "08:00"}
        }
    }
    
    # Add emails as flow messages
    for email in emails:
        klaviyo_flow["messages"].append({
            "type": "email",
            "name": f"Email {email.get('sequence_number', 1)}",
            "delay": email.get("timing", {}).get("send_after_hours", 24),
            "delay_unit": "hours",
            "subject": email.get("subject", ""),
            "preview_text": email.get("preview_text", ""),
            "body": format_email_for_platform(email),
            "from_email": "{{ organization.from_email }}",
            "from_name": "{{ organization.from_name }}"
        })
    
    # Add SMS messages
    for sms_msg in sms:
        klaviyo_flow["messages"].append({
            "type": "sms",
            "name": f"SMS {sms_msg.get('sequence_number', 1)}",
            "delay": sms_msg.get("timing", {}).get("send_after_hours", 48),
            "delay_unit": "hours",
            "body": sms_msg.get("message", ""),
            "media_url": None
        })
    
    return klaviyo_flow

def build_klaviyo_triggers(campaign_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Klaviyo trigger filters"""
    
    campaign_type = campaign_plan.get("campaign_type", "")
    
    if "Cart Abandonment" in campaign_type:
        return [
            {
                "type": "event",
                "event": "Started Checkout",
                "constraint": {
                    "and": [
                        {"field": "$value", "operator": "greater than", "value": 0}
                    ]
                }
            }
        ]
    elif "Welcome" in campaign_type:
        return [
            {
                "type": "list",
                "list_id": "welcome_list"
            }
        ]
    elif "Post-Purchase" in campaign_type:
        return [
            {
                "type": "event",
                "event": "Placed Order",
                "constraint": {
                    "and": [
                        {"field": "$value", "operator": "greater than", "value": 0}
                    ]
                }
            }
        ]
    
    return []

def build_klaviyo_filters(campaign_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Klaviyo flow filters"""
    
    return [
        {
            "type": "property",
            "property": "email",
            "operator": "is set"
        },
        {
            "type": "property", 
            "property": "can_receive_email_marketing",
            "operator": "equals",
            "value": True
        }
    ]

def generate_mailchimp_export(
    campaign_plan: Dict[str, Any], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate Mailchimp automation export"""
    
    return {
        "automation_name": generate_flow_name(campaign_plan),
        "trigger_type": "audience",
        "emails": [
            {
                "delay": email.get("timing", {}).get("send_after_hours", 24),
                "delay_unit": "hours",
                "subject": email.get("subject", ""),
                "content": format_email_for_platform(email)
            }
            for email in emails
        ]
    }

def generate_hubspot_export(
    campaign_plan: Dict[str, Any], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate HubSpot workflow export"""
    
    return {
        "workflow_name": generate_flow_name(campaign_plan),
        "enrollment_triggers": [
            {
                "type": "contact_property_change",
                "property": "lifecycle_stage"
            }
        ],
        "actions": [
            {
                "type": "send_email",
                "delay": email.get("timing", {}).get("send_after_hours", 24),
                "email_subject": email.get("subject", ""),
                "email_body": email.get("body", "")
            }
            for email in emails
        ]
    }

def generate_csv_export(emails: List[Dict[str, Any]], sms: List[Dict[str, Any]]) -> str:
    """Generate CSV export of all messages"""
    
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow([
        "Type", "Sequence", "Subject/Message", "Body", "Delay Hours", "Purpose"
    ])
    
    # Write emails
    for email in emails:
        writer.writerow([
            "Email",
            email.get("sequence_number", 1),
            email.get("subject", ""),
            email.get("body", "")[:100] + "...",
            email.get("timing", {}).get("send_after_hours", 24),
            email.get("purpose", "")
        ])
    
    # Write SMS
    for sms_msg in sms:
        writer.writerow([
            "SMS",
            sms_msg.get("sequence_number", 1),
            sms_msg.get("message", ""),
            "",
            sms_msg.get("timing", {}).get("send_after_hours", 48),
            sms_msg.get("purpose", "")
        ])
    
    return output.getvalue()

def generate_json_export(
    campaign_plan: Dict[str, Any], 
    emails: List[Dict[str, Any]], 
    sms: List[Dict[str, Any]], 
    visuals: List[Dict[str, Any]]
) -> str:
    """Generate complete JSON export"""
    
    export_data = {
        "campaign_plan": campaign_plan,
        "emails": emails,
        "sms": sms,
        "visuals": visuals,
        "export_timestamp": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    return json.dumps(export_data, indent=2)

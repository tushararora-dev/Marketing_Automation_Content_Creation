import json
import csv
import io
from typing import Dict, Any, List
from datetime import datetime

def export_to_klaviyo(
    campaign_data: Dict[str, Any],
    export_format: str = "json"
) -> Dict[str, Any]:
    """
    Export campaign data to Klaviyo-compatible format
    
    Args:
        campaign_data: Complete campaign data with emails, SMS, etc.
        export_format: Format for export (json, csv)
    
    Returns:
        Klaviyo-formatted export data
    """
    
    klaviyo_export = {
        "flow_data": create_klaviyo_flow(campaign_data),
        "email_templates": create_klaviyo_email_templates(campaign_data.get("emails", [])),
        "sms_templates": create_klaviyo_sms_templates(campaign_data.get("sms", [])),
        "segments": create_klaviyo_segments(campaign_data),
        "export_info": {
            "created_at": datetime.now().isoformat(),
            "format": export_format,
            "version": "1.0"
        }
    }
    
    if export_format == "csv":
        klaviyo_export["csv_files"] = generate_csv_exports(campaign_data)
    
    return klaviyo_export

def create_klaviyo_flow(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create Klaviyo flow structure"""
    
    campaign_type = campaign_data.get("campaign_type", "Custom")
    brand_name = campaign_data.get("brand_name", "Brand")
    
    flow = {
        "name": f"{brand_name} - {campaign_type} Flow",
        "status": "Draft",
        "trigger_filters": create_klaviyo_triggers(campaign_data),
        "flow_filters": create_klaviyo_flow_filters(campaign_data),
        "actions": create_klaviyo_actions(campaign_data),
        "settings": {
            "smart_sending": True,
            "quiet_hours": {
                "enabled": True,
                "start_time": "22:00",
                "end_time": "08:00",
                "timezone": "UTC"
            },
            "frequency_capping": {
                "enabled": True,
                "max_emails_per_day": 2,
                "max_emails_per_week": 7
            }
        }
    }
    
    return flow

def create_klaviyo_triggers(campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create Klaviyo trigger filters based on campaign type"""
    
    campaign_type = campaign_data.get("campaign_type", "Custom")
    
    trigger_mapping = {
        "Cart Abandonment": [
            {
                "type": "event",
                "event_name": "Started Checkout",
                "constraints": {
                    "and": [
                        {
                            "field": "$value",
                            "operator": "greater_than",
                            "value": 0
                        }
                    ]
                }
            }
        ],
        "Welcome Series": [
            {
                "type": "list_trigger",
                "list_name": "Welcome List"
            }
        ],
        "Post-Purchase": [
            {
                "type": "event",
                "event_name": "Placed Order",
                "constraints": {
                    "and": [
                        {
                            "field": "$value", 
                            "operator": "greater_than",
                            "value": 0
                        }
                    ]
                }
            }
        ],
        "Win-Back": [
            {
                "type": "segment",
                "segment_name": "Inactive Customers"
            }
        ]
    }
    
    return trigger_mapping.get(campaign_type, [
        {
            "type": "custom_event",
            "event_name": "Custom Trigger"
        }
    ])

def create_klaviyo_flow_filters(campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create Klaviyo flow filters"""
    
    base_filters = [
        {
            "type": "property_filter",
            "property": "email",
            "operator": "is_set"
        },
        {
            "type": "property_filter",
            "property": "can_receive_email_marketing",
            "operator": "equals",
            "value": True
        }
    ]
    
    # Add campaign-specific filters
    campaign_type = campaign_data.get("campaign_type", "")
    
    if "Cart Abandonment" in campaign_type:
        base_filters.append({
            "type": "event_filter",
            "event": "Placed Order",
            "operator": "has_not_happened_since",
            "timeframe": "24_hours"
        })
    
    return base_filters

def create_klaviyo_actions(campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create Klaviyo flow actions (emails and SMS)"""
    
    actions = []
    
    # Add email actions
    emails = campaign_data.get("emails", [])
    for i, email in enumerate(emails):
        timing = email.get("timing", {})
        delay_hours = timing.get("send_after_hours", 24)
        
        email_action = {
            "type": "email",
            "name": f"Email {i + 1}: {email.get('subject', 'Email')}",
            "delay": {
                "type": "time_delay",
                "value": delay_hours,
                "unit": "hours"
            },
            "email_template": create_klaviyo_email_template(email),
            "tracking": {
                "utm_params": True,
                "open_tracking": True,
                "click_tracking": True
            }
        }
        
        actions.append(email_action)
    
    # Add SMS actions
    sms_messages = campaign_data.get("sms", [])
    for i, sms in enumerate(sms_messages):
        timing = sms.get("timing", {})
        delay_hours = timing.get("send_after_hours", 48)
        
        sms_action = {
            "type": "sms",
            "name": f"SMS {i + 1}",
            "delay": {
                "type": "time_delay",
                "value": delay_hours,
                "unit": "hours"
            },
            "message": sms.get("message", ""),
            "media_url": None
        }
        
        actions.append(sms_action)
    
    return actions

def create_klaviyo_email_template(email: Dict[str, Any]) -> Dict[str, Any]:
    """Create Klaviyo email template from email data"""
    
    template = {
        "subject": email.get("subject", ""),
        "preview_text": email.get("preview_text", ""),
        "from_email": "{{ organization.from_email }}",
        "from_name": "{{ organization.from_name }}",
        "reply_to": "{{ organization.reply_to_email }}",
        "template_html": create_klaviyo_html_template(email),
        "template_text": create_klaviyo_text_template(email),
        "personalization": email.get("personalization", [])
    }
    
    return template

def create_klaviyo_html_template(email: Dict[str, Any]) -> str:
    """Create HTML template for Klaviyo email"""
    
    body = email.get("body", "")
    cta = email.get("cta", {})
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{email.get('subject', 'Email')}</title>
        <style>
            body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .content {{ color: #333; }}
            .cta {{ text-align: center; margin: 30px 0; }}
            .cta a {{ 
                display: inline-block; 
                padding: 15px 30px; 
                background-color: #007bff; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
                font-weight: bold;
            }}
            .footer {{ 
                margin-top: 40px; 
                padding-top: 20px; 
                border-top: 1px solid #eee; 
                text-align: center; 
                font-size: 12px; 
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="{{{{ organization.logo }}}}" alt="{{{{ organization.name }}}}" style="max-height: 80px;">
            </div>
            
            <div class="content">
                {format_email_body_for_klaviyo(body)}
            </div>
            
            {format_cta_for_klaviyo(cta)}
            
            <div class="footer">
                <p>{{{{ unsubscribe_link }}}}</p>
                <p>{{{{ organization.address }}}}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def format_email_body_for_klaviyo(body: str) -> str:
    """Format email body with Klaviyo personalization"""
    
    # Replace common personalization patterns
    formatted_body = body.replace("{{first_name}}", "{{ person.first_name|default:'there' }}")
    formatted_body = formatted_body.replace("{{name}}", "{{ person.first_name|default:'valued customer' }}")
    formatted_body = formatted_body.replace("{{product_name}}", "{{ event.ProductName|default:'our product' }}")
    
    # Convert line breaks to HTML
    formatted_body = formatted_body.replace('\n', '<br>')
    
    # Wrap in paragraphs
    paragraphs = formatted_body.split('<br><br>')
    html_paragraphs = [f"<p>{p}</p>" for p in paragraphs if p.strip()]
    
    return ''.join(html_paragraphs)

def format_cta_for_klaviyo(cta: Dict[str, str]) -> str:
    """Format CTA button for Klaviyo"""
    
    if not cta or not cta.get("text"):
        return ""
    
    return f"""
    <div class="cta">
        <a href="{cta.get('url', '#')}">
            {cta.get('text', 'Click Here')}
        </a>
    </div>
    """

def create_klaviyo_text_template(email: Dict[str, Any]) -> str:
    """Create plain text template for Klaviyo email"""
    
    body = email.get("body", "")
    cta = email.get("cta", {})
    
    # Convert HTML to plain text
    text_body = body.replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n\n')
    
    # Add personalization
    text_body = text_body.replace("{{first_name}}", "{{ person.first_name|default:'there' }}")
    
    text_template = f"""
    {text_body}
    
    {cta.get('text', '')}: {cta.get('url', '')}
    
    ---
    {{{{ unsubscribe_link }}}}
    {{{{ organization.address }}}}
    """
    
    return text_template

def create_klaviyo_email_templates(emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create individual Klaviyo email templates"""
    
    templates = []
    
    for i, email in enumerate(emails):
        template = {
            "template_id": f"template_{i+1}",
            "name": f"Email {i+1}: {email.get('subject', 'Email')}",
            "subject": email.get("subject", ""),
            "html": create_klaviyo_html_template(email),
            "text": create_klaviyo_text_template(email),
            "created_at": datetime.now().isoformat()
        }
        
        templates.append(template)
    
    return templates

def create_klaviyo_sms_templates(sms_messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create Klaviyo SMS templates"""
    
    templates = []
    
    for i, sms in enumerate(sms_messages):
        template = {
            "template_id": f"sms_template_{i+1}",
            "name": f"SMS {i+1}",
            "message": format_sms_for_klaviyo(sms.get("message", "")),
            "created_at": datetime.now().isoformat()
        }
        
        templates.append(template)
    
    return templates

def format_sms_for_klaviyo(message: str) -> str:
    """Format SMS message with Klaviyo personalization"""
    
    # Replace personalization tags
    formatted_message = message.replace("{{name}}", "{{ person.first_name|default:'there' }}")
    formatted_message = formatted_message.replace("{{first_name}}", "{{ person.first_name|default:'there' }}")
    formatted_message = formatted_message.replace("{{product}}", "{{ event.ProductName|default:'product' }}")
    
    return formatted_message

def create_klaviyo_segments(campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create Klaviyo segments for targeting"""
    
    segments = []
    
    # Create segment based on campaign type
    campaign_type = campaign_data.get("campaign_type", "Custom")
    target_audience = campaign_data.get("target_audience", "General customers")
    
    if campaign_type == "Cart Abandonment":
        segments.append({
            "name": "Cart Abandoners",
            "definition": {
                "and": [
                    {
                        "property": "Started Checkout",
                        "operator": "has_happened",
                        "timeframe": "last_7_days"
                    },
                    {
                        "property": "Placed Order",
                        "operator": "has_not_happened_since",
                        "timeframe": "last_24_hours"
                    }
                ]
            }
        })
    elif campaign_type == "Win-Back":
        segments.append({
            "name": "Inactive Customers",
            "definition": {
                "and": [
                    {
                        "property": "Placed Order",
                        "operator": "has_happened",
                        "timeframe": "ever"
                    },
                    {
                        "property": "Placed Order",
                        "operator": "has_not_happened_since",
                        "timeframe": "last_30_days"
                    }
                ]
            }
        })
    
    # Add general targeting segment
    segments.append({
        "name": f"{campaign_type} Target Audience",
        "definition": {
            "and": [
                {
                    "property": "email",
                    "operator": "is_set"
                },
                {
                    "property": "can_receive_email_marketing",
                    "operator": "equals",
                    "value": True
                }
            ]
        },
        "description": f"Target audience: {target_audience}"
    })
    
    return segments

def generate_csv_exports(campaign_data: Dict[str, Any]) -> Dict[str, str]:
    """Generate CSV exports for Klaviyo import"""
    
    csv_files = {}
    
    # Email CSV
    email_csv = generate_email_csv(campaign_data.get("emails", []))
    csv_files["emails.csv"] = email_csv
    
    # SMS CSV
    sms_csv = generate_sms_csv(campaign_data.get("sms", []))
    csv_files["sms.csv"] = sms_csv
    
    # Flow structure CSV
    flow_csv = generate_flow_csv(campaign_data)
    csv_files["flow_structure.csv"] = flow_csv
    
    return csv_files

def generate_email_csv(emails: List[Dict[str, Any]]) -> str:
    """Generate CSV for email templates"""
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        "Template Name", "Subject", "Preview Text", "Body HTML", "Body Text", 
        "Delay Hours", "Purpose", "Personalization Tags"
    ])
    
    # Data rows
    for i, email in enumerate(emails):
        writer.writerow([
            f"Email {i+1}",
            email.get("subject", ""),
            email.get("preview_text", ""),
            create_klaviyo_html_template(email).replace('\n', ' '),
            email.get("body", "").replace('\n', ' '),
            email.get("timing", {}).get("send_after_hours", 24),
            email.get("purpose", ""),
            ', '.join(email.get("personalization", []))
        ])
    
    return output.getvalue()

def generate_sms_csv(sms_messages: List[Dict[str, Any]]) -> str:
    """Generate CSV for SMS templates"""
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        "Template Name", "Message", "Character Count", "Delay Hours", 
        "Purpose", "Compliance Check"
    ])
    
    # Data rows
    for i, sms in enumerate(sms_messages):
        message = sms.get("message", "")
        writer.writerow([
            f"SMS {i+1}",
            message,
            len(message),
            sms.get("timing", {}).get("send_after_hours", 48),
            sms.get("purpose", ""),
            "Yes" if sms.get("compliance", {}).get("opt_out_included", False) else "No"
        ])
    
    return output.getvalue()

def generate_flow_csv(campaign_data: Dict[str, Any]) -> str:
    """Generate CSV for flow structure"""
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        "Step Number", "Step Type", "Content", "Delay", "Conditions"
    ])
    
    # Email steps
    emails = campaign_data.get("emails", [])
    for i, email in enumerate(emails):
        writer.writerow([
            i + 1,
            "Email",
            email.get("subject", ""),
            f"{email.get('timing', {}).get('send_after_hours', 24)} hours",
            "Active subscriber, hasn't converted"
        ])
    
    # SMS steps
    sms_messages = campaign_data.get("sms", [])
    for i, sms in enumerate(sms_messages):
        step_number = len(emails) + i + 1
        writer.writerow([
            step_number,
            "SMS",
            sms.get("message", "")[:50] + "...",
            f"{sms.get('timing', {}).get('send_after_hours', 48)} hours",
            "Active subscriber, SMS consent, hasn't converted"
        ])
    
    return output.getvalue()

def validate_klaviyo_export(export_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate Klaviyo export data"""
    
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check required fields
    required_fields = ["flow_data", "email_templates"]
    for field in required_fields:
        if field not in export_data:
            validation_results["errors"].append(f"Missing required field: {field}")
            validation_results["valid"] = False
    
    # Validate flow data
    flow_data = export_data.get("flow_data", {})
    if not flow_data.get("name"):
        validation_results["errors"].append("Flow must have a name")
        validation_results["valid"] = False
    
    # Validate email templates
    email_templates = export_data.get("email_templates", [])
    for i, template in enumerate(email_templates):
        if not template.get("subject"):
            validation_results["warnings"].append(f"Email template {i+1} missing subject")
        if not template.get("html"):
            validation_results["errors"].append(f"Email template {i+1} missing HTML content")
            validation_results["valid"] = False
    
    return validation_results

def create_klaviyo_import_instructions() -> Dict[str, Any]:
    """Create instructions for importing into Klaviyo"""
    
    instructions = {
        "flow_import": [
            "1. Log into Klaviyo account",
            "2. Navigate to Flows section",
            "3. Click 'Create Flow' > 'Create from Scratch'",
            "4. Set up trigger using provided trigger filters",
            "5. Add flow filters as specified",
            "6. Create email and SMS actions using provided templates",
            "7. Set delays and timing as specified",
            "8. Test flow with test profiles",
            "9. Activate flow when ready"
        ],
        "template_import": [
            "1. Navigate to Content > Email Templates",
            "2. Create new template",
            "3. Copy HTML content from export",
            "4. Test template rendering",
            "5. Save template with provided name"
        ],
        "segment_import": [
            "1. Navigate to Audience > Lists & Segments",
            "2. Create new segment",
            "3. Set up conditions using provided definitions",
            "4. Test segment with sample data",
            "5. Save segment"
        ],
        "best_practices": [
            "Always test flows with test profiles first",
            "Review personalization tokens work correctly",
            "Check mobile rendering of emails",
            "Verify compliance with email regulations",
            "Monitor performance after activation"
        ]
    }
    
    return instructions

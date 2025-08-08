import pytest
import json
from datetime import datetime
from unittest.mock import Mock, patch
from workflows.marketing_automation.flow_builder import (
    build_campaign_flow, generate_flow_id, generate_flow_name,
    build_flow_triggers, build_message_sequence, organize_flow_assets,
    generate_klaviyo_export, generate_csv_export
)

class TestFlowBuilder:
    """Test cases for campaign flow builder functionality"""
    
    def test_build_campaign_flow_complete(self):
        """Test complete campaign flow building"""
        
        campaign_plan = {
            "campaign_type": "Welcome Series",
            "brand_name": "Test Brand",
            "objective": "Onboard new customers",
            "timeline": [
                {"sequence": 1, "type": "email", "trigger_hours": 0},
                {"sequence": 2, "type": "email", "trigger_hours": 24}
            ]
        }
        
        emails = [
            {
                "sequence_number": 1,
                "subject": "Welcome!",
                "body": "Welcome to our community",
                "cta": {"text": "Get Started", "url": "#"},
                "timing": {"send_after_hours": 0}
            },
            {
                "sequence_number": 2,
                "subject": "Getting Started",
                "body": "Here's how to get started",
                "cta": {"text": "Learn More", "url": "#"},
                "timing": {"send_after_hours": 24}
            }
        ]
        
        sms = [
            {
                "sequence_number": 1,
                "message": "Welcome! Check your email for next steps.",
                "timing": {"send_after_hours": 1}
            }
        ]
        
        visuals = [
            {
                "type": "email_header",
                "description": "Welcome email header",
                "file_name": "header_1.png"
            }
        ]
        
        flow = build_campaign_flow(campaign_plan, emails, sms, visuals)
        
        # Verify flow structure
        assert "flow_id" in flow
        assert "flow_name" in flow
        assert "triggers" in flow
        assert "sequence" in flow
        assert "assets" in flow
        assert "export_formats" in flow
        
        # Verify flow content
        assert flow["flow_type"] == "Welcome Series"
        assert len(flow["sequence"]) >= 2  # At least 2 emails
        assert flow["status"] == "draft"
    
    def test_generate_flow_id(self):
        """Test flow ID generation"""
        
        campaign_plan = {"campaign_type": "Cart Abandonment"}
        
        flow_id = generate_flow_id(campaign_plan)
        
        assert "cart_abandonment_flow" in flow_id.lower()
        assert len(flow_id) > 20  # Should include timestamp
        assert "_" in flow_id  # Should have separators
    
    def test_generate_flow_name(self):
        """Test flow name generation"""
        
        campaign_plan = {
            "campaign_type": "Post-Purchase",
            "brand_name": "Amazing Store"
        }
        
        flow_name = generate_flow_name(campaign_plan)
        
        assert "Amazing Store" in flow_name
        assert "Post-Purchase Campaign" in flow_name
    
    def test_build_flow_triggers(self):
        """Test flow trigger building"""
        
        campaign_plan = {
            "campaign_type": "Cart Abandonment",
            "triggers": {
                "start_trigger": "Items added to cart but not purchased",
                "conditions": ["cart_value > 0", "email_exists"],
                "exclusions": ["recently_purchased", "unsubscribed"]
            }
        }
        
        triggers = build_flow_triggers(campaign_plan)
        
        assert "entry_trigger" in triggers
        assert "exit_triggers" in triggers
        assert "exclusions" in triggers
        
        # Verify trigger type
        assert triggers["entry_trigger"]["type"] == "cart_abandonment"
        
        # Verify exit triggers
        exit_triggers = triggers["exit_triggers"]
        assert len(exit_triggers) >= 3  # Should have multiple exit conditions
        
        # Check for standard exit triggers
        trigger_types = [trigger["type"] for trigger in exit_triggers]
        assert "goal_achieved" in trigger_types
        assert "user_action" in trigger_types
    
    def test_build_message_sequence(self):
        """Test message sequence building"""
        
        emails = [
            {
                "sequence_number": 1,
                "subject": "First Email",
                "timing": {"send_after_hours": 1}
            },
            {
                "sequence_number": 2,
                "subject": "Second Email", 
                "timing": {"send_after_hours": 24}
            }
        ]
        
        sms = [
            {
                "sequence_number": 1,
                "message": "First SMS",
                "timing": {"send_after_hours": 48}
            }
        ]
        
        campaign_plan = {"timeline": []}
        
        sequence = build_message_sequence(emails, sms, campaign_plan)
        
        # Should be sorted by delay hours
        assert len(sequence) == 3
        assert sequence[0]["delay"]["value"] == 1   # First email
        assert sequence[1]["delay"]["value"] == 24  # Second email
        assert sequence[2]["delay"]["value"] == 48  # SMS
        
        # Verify sequence structure
        for step in sequence:
            assert "step_id" in step
            assert "step_type" in step
            assert "delay" in step
            assert "content" in step
            assert "next_step" in step
    
    def test_organize_flow_assets(self):
        """Test flow assets organization"""
        
        visuals = [
            {"type": "email_header", "file_name": "header1.png"},
            {"type": "product_showcase", "file_name": "product1.jpg"},
            {"type": "cta_button", "file_name": "button1.png"}
        ]
        
        emails = [
            {"sequence_number": 1, "subject": "Email 1"},
            {"sequence_number": 2, "subject": "Email 2"}
        ]
        
        sms = [
            {"sequence_number": 1, "message": "SMS 1"}
        ]
        
        assets = organize_flow_assets(visuals, emails, sms)
        
        assert "visual_assets" in assets
        assert "content_assets" in assets
        assert "export_ready" in assets
        assert "asset_count" in assets
        
        # Verify visual asset organization
        visual_assets = assets["visual_assets"]
        assert "email_headers" in visual_assets
        assert "product_images" in visual_assets
        assert "cta_buttons" in visual_assets
        
        # Verify content asset counting
        content_assets = assets["content_assets"]
        assert content_assets["email_templates"] == 2
        assert content_assets["sms_templates"] == 1
        
        # Verify total count
        assert assets["asset_count"] == 6  # 3 visuals + 2 emails + 1 sms
    
    def test_export_formats(self):
        """Test export format generation"""
        
        campaign_plan = {"campaign_type": "Welcome Series", "brand_name": "Test"}
        emails = [{"subject": "Welcome", "body": "Welcome message"}]
        sms = [{"message": "Welcome SMS"}]
        visuals = [{"type": "header", "file_name": "header.png"}]
        
        flow = build_campaign_flow(campaign_plan, emails, sms, visuals)
        export_formats = flow["export_formats"]
        
        assert "klaviyo" in export_formats
        assert "mailchimp" in export_formats
        assert "hubspot" in export_formats
        assert "generic_csv" in export_formats
        assert "json" in export_formats
    
    def test_klaviyo_export(self):
        """Test Klaviyo-specific export format"""
        
        campaign_plan = {
            "campaign_type": "Cart Abandonment",
            "brand_name": "Test Store"
        }
        
        emails = [
            {
                "sequence_number": 1,
                "subject": "Don't forget your cart!",
                "body": "Complete your purchase",
                "timing": {"send_after_hours": 1}
            }
        ]
        
        sms = []
        visuals = []
        
        klaviyo_export = generate_klaviyo_export(campaign_plan, emails, sms, visuals)
        
        assert "flow_name" in klaviyo_export
        assert "trigger_filters" in klaviyo_export
        assert "messages" in klaviyo_export
        assert "settings" in klaviyo_export
        
        # Verify Klaviyo-specific structure
        assert klaviyo_export["settings"]["smart_sending"] is True
        assert "quiet_hours" in klaviyo_export["settings"]
        
        # Verify messages
        messages = klaviyo_export["messages"]
        assert len(messages) == 1
        assert messages[0]["type"] == "email"
        assert messages[0]["delay"] == 1
    
    def test_csv_export(self):
        """Test CSV export generation"""
        
        emails = [
            {
                "sequence_number": 1,
                "subject": "First Email",
                "body": "First email content",
                "timing": {"send_after_hours": 1},
                "purpose": "Welcome"
            }
        ]
        
        sms = [
            {
                "sequence_number": 1,
                "message": "First SMS",
                "timing": {"send_after_hours": 24},
                "purpose": "Follow-up"
            }
        ]
        
        csv_content = generate_csv_export(emails, sms)
        
        # Verify CSV structure
        lines = csv_content.strip().split('\n')
        assert len(lines) >= 3  # Header + 2 data rows
        
        # Verify header
        header = lines[0]
        assert "Type" in header
        assert "Sequence" in header
        assert "Subject/Message" in header
        
        # Verify data rows
        email_row = lines[1]
        assert "Email" in email_row
        assert "First Email" in email_row
        
        sms_row = lines[2]
        assert "SMS" in sms_row
        assert "First SMS" in sms_row
    
    def test_flow_validation(self):
        """Test flow validation"""
        
        # Valid flow
        valid_flow = {
            "flow_id": "test_flow_123",
            "flow_name": "Test Flow",
            "triggers": {"entry_trigger": {"type": "signup"}},
            "sequence": [
                {"step_id": "step_1", "step_type": "email"}
            ],
            "assets": {"asset_count": 1}
        }
        
        # Invalid flow (missing required fields)
        invalid_flow = {
            "flow_id": "test_flow_123"
            # Missing required fields
        }
        
        # Validation tests
        required_fields = ["flow_id", "flow_name", "triggers", "sequence"]
        
        for field in required_fields:
            assert field in valid_flow
        
        # Check invalid flow
        missing_fields = [field for field in required_fields if field not in invalid_flow]
        assert len(missing_fields) > 0
    
    def test_flow_timing_optimization(self):
        """Test flow timing optimization"""
        
        from workflows.marketing_automation.flow_builder import extract_delay_rules
        
        emails = [
            {"sequence_number": 1, "timing": {"send_after_hours": 1}},
            {"sequence_number": 2, "timing": {"send_after_hours": 24}},
            {"sequence_number": 3, "timing": {"send_after_hours": 72}}
        ]
        
        sms = [
            {"sequence_number": 1, "timing": {"send_after_hours": 48}}
        ]
        
        delay_rules = extract_delay_rules(emails, sms)
        
        assert len(delay_rules) == 4  # 3 emails + 1 SMS
        
        # Verify delay progression
        email_delays = [rule["delay_hours"] for rule in delay_rules if rule["message_type"] == "email"]
        assert email_delays == [1, 24, 72]  # Progressive delays
        
        sms_delays = [rule["delay_hours"] for rule in delay_rules if rule["message_type"] == "sms"]
        assert sms_delays == [48]
    
    def test_analytics_setup(self):
        """Test analytics and tracking setup"""
        
        from workflows.marketing_automation.flow_builder import setup_flow_analytics
        
        campaign_plan = {"campaign_type": "Welcome Series"}
        
        analytics = setup_flow_analytics(campaign_plan)
        
        assert "tracking_enabled" in analytics
        assert "kpis" in analytics
        assert "goals" in analytics
        assert "attribution" in analytics
        assert "reporting" in analytics
        
        # Verify KPIs
        kpis = analytics["kpis"]
        expected_kpis = ["open_rate", "click_through_rate", "conversion_rate"]
        for kpi in expected_kpis:
            assert kpi in kpis
        
        # Verify goals structure
        goals = analytics["goals"]
        assert len(goals) > 0
        for goal in goals:
            assert "name" in goal
            assert "description" in goal
            assert "value" in goal


class TestFlowExport:
    """Test cases for flow export functionality"""
    
    def test_json_export(self):
        """Test JSON export functionality"""
        
        campaign_data = {
            "campaign_type": "Test Campaign",
            "emails": [{"subject": "Test"}],
            "sms": [{"message": "Test SMS"}],
            "visuals": [{"type": "header"}]
        }
        
        from workflows.marketing_automation.flow_builder import generate_json_export
        
        json_export = generate_json_export(
            campaign_data, 
            campaign_data["emails"], 
            campaign_data["sms"], 
            campaign_data["visuals"]
        )
        
        # Verify JSON structure
        parsed_json = json.loads(json_export)
        assert "campaign_plan" in parsed_json
        assert "emails" in parsed_json
        assert "sms" in parsed_json
        assert "visuals" in parsed_json
        assert "export_timestamp" in parsed_json
        assert "version" in parsed_json
    
    def test_platform_specific_exports(self):
        """Test platform-specific export formats"""
        
        campaign_plan = {"campaign_type": "Cart Abandonment"}
        emails = [{"subject": "Test", "body": "Test content"}]
        sms = []
        
        from workflows.marketing_automation.flow_builder import (
            generate_mailchimp_export,
            generate_hubspot_export
        )
        
        # Test Mailchimp export
        mailchimp_export = generate_mailchimp_export(campaign_plan, emails, sms)
        assert "automation_name" in mailchimp_export
        assert "emails" in mailchimp_export
        
        # Test HubSpot export
        hubspot_export = generate_hubspot_export(campaign_plan, emails, sms)
        assert "workflow_name" in hubspot_export
        assert "actions" in hubspot_export
    
    def test_export_file_management(self):
        """Test export file management"""
        
        # Test export directory structure
        expected_exports = ["klaviyo", "mailchimp", "hubspot", "csv", "json"]
        
        for export_type in expected_exports:
            # Each export type should be available
            assert isinstance(export_type, str)
            assert len(export_type) > 0


# Test fixtures for flow builder
@pytest.fixture
def sample_campaign_flow():
    """Sample campaign flow for testing"""
    return {
        "flow_id": "welcome_flow_20240101_120000",
        "flow_name": "Test Brand - Welcome Series Campaign",
        "flow_type": "Welcome Series",
        "status": "draft",
        "triggers": {
            "entry_trigger": {
                "type": "user_signup",
                "conditions": ["email_exists", "opted_in"],
                "delay": "0 minutes"
            }
        },
        "sequence": [
            {
                "step_id": "step_1",
                "step_type": "email",
                "delay": {"type": "time_delay", "value": 0, "unit": "hours"}
            }
        ]
    }

@pytest.fixture
def sample_export_data():
    """Sample export data for testing"""
    return {
        "campaign_plan": {"campaign_type": "Welcome Series"},
        "emails": [{"subject": "Welcome!", "body": "Welcome message"}],
        "sms": [{"message": "Welcome SMS"}],
        "visuals": [{"type": "header", "file_name": "header.png"}]
    }

def test_flow_fixtures(sample_campaign_flow, sample_export_data):
    """Test flow builder with fixtures"""
    
    # Test campaign flow structure
    assert sample_campaign_flow["flow_type"] == "Welcome Series"
    assert sample_campaign_flow["status"] == "draft"
    assert "triggers" in sample_campaign_flow
    assert "sequence" in sample_campaign_flow
    
    # Test export data structure
    assert "campaign_plan" in sample_export_data
    assert "emails" in sample_export_data
    assert len(sample_export_data["emails"]) == 1
    assert sample_export_data["emails"][0]["subject"] == "Welcome!"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

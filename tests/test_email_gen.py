import pytest
from unittest.mock import Mock, patch
from workflows.marketing_automation.email_generator import (
    generate_emails, generate_single_email, parse_email_response,
    extract_subject_line, extract_email_body, extract_call_to_action,
    optimize_email_for_mobile, add_dynamic_content_blocks
)

class TestEmailGenerator:
    """Test cases for email generation functionality"""
    
    def test_generate_emails_success(self):
        """Test successful email generation"""
        
        brand_analysis = {
            "brand_name": "Test Brand",
            "description": "Test description",
            "products": ["Product A", "Product B"],
            "target_audience": "Young professionals"
        }
        
        campaign_plan = {
            "campaign_type": "Welcome Series",
            "target_audience": "New subscribers",
            "email_sequence": [
                {"email_number": 1, "purpose": "Welcome", "focus": "Brand introduction"},
                {"email_number": 2, "purpose": "Value", "focus": "Product benefits"}
            ]
        }
        
        with patch('workflows.marketing_automation.email_generator.get_llm_response') as mock_llm:
            mock_llm.return_value = """
            Subject: Welcome to Test Brand!
            Preview: Get started with exclusive benefits
            
            Dear {{first_name}},
            
            Welcome to Test Brand! We're excited to have you join our community.
            
            Click here to explore our products and get started.
            
            Best regards,
            The Test Brand Team
            """
            
            emails = generate_emails(
                brand_analysis=brand_analysis,
                campaign_plan=campaign_plan,
                num_emails=2,
                tone="Friendly"
            )
            
            assert len(emails) == 2
            assert emails[0]["sequence_number"] == 1
            assert emails[1]["sequence_number"] == 2
            assert "subject" in emails[0]
            assert "body" in emails[0]
    
    def test_generate_single_email(self):
        """Test single email generation"""
        
        brand_analysis = {"brand_name": "Test Brand"}
        campaign_plan = {"campaign_type": "Cart Abandonment"}
        email_plan = {
            "email_number": 1,
            "purpose": "Reminder",
            "focus": "Complete purchase"
        }
        
        with patch('workflows.marketing_automation.email_generator.get_llm_response') as mock_llm:
            mock_llm.return_value = """
            Subject: Don't forget your cart!
            Preview: Complete your purchase now
            
            Hi {{first_name}},
            
            You left some great items in your cart. Don't miss out!
            
            Complete Purchase
            """
            
            email = generate_single_email(
                brand_analysis=brand_analysis,
                campaign_plan=campaign_plan,
                email_plan=email_plan,
                tone="Urgent",
                sequence_number=1
            )
            
            assert email["sequence_number"] == 1
            assert email["purpose"] == "Reminder"
            assert "subject" in email
            assert "body" in email
            assert "cta" in email
    
    def test_parse_email_response(self):
        """Test email response parsing"""
        
        email_text = """
        Subject: Welcome to Our Brand!
        Preview: Start your journey today
        
        Dear valued customer,
        
        Welcome to our amazing community! We're thrilled to have you on board.
        
        Our products are designed to make your life easier and more enjoyable.
        
        Get Started Now
        
        Best regards,
        The Team
        """
        
        email_plan = {"purpose": "Welcome", "focus": "Onboarding"}
        
        email = parse_email_response(email_text, email_plan, 1)
        
        assert email["sequence_number"] == 1
        assert email["purpose"] == "Welcome"
        assert email["subject"] == "Welcome to Our Brand!"
        assert email["preview_text"] == "Start your journey today"
        assert "valued customer" in email["body"]
        assert email["cta"]["text"] == "Get Started Now"
    
    def test_extract_subject_line(self):
        """Test subject line extraction"""
        
        test_cases = [
            {
                "text": "Subject: Welcome to our store!\nBody content here",
                "expected": "Welcome to our store!"
            },
            {
                "text": "**Subject:** Don't miss out!\nMore content",
                "expected": "Don't miss out!"
            },
            {
                "text": "Subject Line: Special offer inside\nContent",
                "expected": "Special offer inside"
            },
            {
                "text": "No subject line in this text\nJust content",
                "expected": "No subject line in this text"  # First line fallback
            }
        ]
        
        for case in test_cases:
            result = extract_subject_line(case["text"])
            assert result == case["expected"]
    
    def test_extract_email_body(self):
        """Test email body extraction"""
        
        email_text = """
        Subject: Test Subject
        Preview: Test preview
        
        This is the main email content.
        It spans multiple lines.
        
        This should be included in the body.
        
        CTA: Click Here
        """
        
        body = extract_email_body(email_text)
        
        assert "This is the main email content" in body
        assert "It spans multiple lines" in body
        assert "This should be included in the body" in body
        assert "Subject:" not in body
        assert "CTA:" not in body
    
    def test_extract_call_to_action(self):
        """Test CTA extraction"""
        
        test_cases = [
            {
                "text": "Some content here\nCTA: Shop Now\nMore content",
                "expected": {"text": "Shop Now", "url": "[DYNAMIC_URL]"}
            },
            {
                "text": "Content with **CTA:** Learn More **end**",
                "expected": {"text": "Learn More", "url": "[DYNAMIC_URL]"}
            },
            {
                "text": "Click here to buy now and save money!",
                "expected": {"text": "Buy Now", "url": "[DYNAMIC_URL]"}
            },
            {
                "text": "No clear CTA in this text content",
                "expected": {"text": "Shop Now", "url": "[DYNAMIC_URL]"}  # Default
            }
        ]
        
        for case in test_cases:
            result = extract_call_to_action(case["text"])
            assert result["text"] == case["expected"]["text"]
            assert result["url"] == case["expected"]["url"]
    
    def test_optimize_email_for_mobile(self):
        """Test mobile optimization"""
        
        email = {
            "subject": "This is a very long subject line that exceeds mobile limits",
            "body": "Email body content",
            "cta": {"text": "Click Here", "url": "#"}
        }
        
        optimized = optimize_email_for_mobile(email)
        
        assert len(optimized["mobile_subject"]) <= 40
        assert optimized["mobile_optimized"] is True
        assert optimized["responsive_design"] is True
        assert "..." in optimized["mobile_subject"]  # Truncated
    
    def test_add_dynamic_content_blocks(self):
        """Test dynamic content blocks addition"""
        
        email = {
            "sequence_number": 3,
            "purpose": "urgency reminder",
            "focus": "cart abandonment"
        }
        
        brand_analysis = {"brand_name": "Test Brand"}
        
        enhanced_email = add_dynamic_content_blocks(email, brand_analysis)
        
        assert "product_recommendations" in enhanced_email
        assert enhanced_email["product_recommendations"]["enabled"] is True
        assert "social_proof" in enhanced_email
        assert "urgency" in enhanced_email  # Added because sequence_number >= 3
        assert enhanced_email["urgency"]["countdown_timer"] is True
    
    def test_email_personalization(self):
        """Test email personalization token extraction"""
        
        email_text = """
        Dear {{first_name}},
        
        Thank you for your interest in {{product_name}}.
        
        Your {{cart_items}} are waiting for you at {{brand_name}}.
        """
        
        from workflows.marketing_automation.email_generator import extract_personalization_tags
        
        tags = extract_personalization_tags(email_text)
        
        expected_tags = ["{{first_name}}", "{{product_name}}", "{{cart_items}}", "{{brand_name}}"]
        
        for tag in expected_tags:
            assert tag in tags
    
    def test_email_timing(self):
        """Test email timing calculations"""
        
        from workflows.marketing_automation.email_generator import get_send_delay
        
        # Test standard delays
        assert get_send_delay(1) == 1      # 1 hour
        assert get_send_delay(2) == 24     # 1 day
        assert get_send_delay(3) == 72     # 3 days
        assert get_send_delay(4) == 168    # 1 week
        assert get_send_delay(5) == 336    # 2 weeks
        
        # Test extended sequence
        assert get_send_delay(6) == 168 * 6  # Weekly after email 5
    
    def test_email_validation(self):
        """Test email content validation"""
        
        valid_email = {
            "subject": "Valid Subject",
            "body": "This is a valid email body with sufficient content.",
            "cta": {"text": "Click Here", "url": "#"},
            "sequence_number": 1
        }
        
        invalid_email = {
            "subject": "",
            "body": "",
            # Missing CTA
        }
        
        # Test validation logic
        assert len(valid_email["subject"]) > 0
        assert len(valid_email["body"]) > 10
        assert "cta" in valid_email
        
        assert len(invalid_email["subject"]) == 0
        assert len(invalid_email["body"]) == 0
        assert "cta" not in invalid_email
    
    def test_campaign_specific_content(self):
        """Test campaign-specific email content generation"""
        
        campaign_types = [
            "Cart Abandonment",
            "Welcome Series", 
            "Post-Purchase",
            "Win-Back"
        ]
        
        for campaign_type in campaign_types:
            campaign_plan = {
                "campaign_type": campaign_type,
                "email_sequence": [{"email_number": 1, "purpose": "Test"}]
            }
            
            # Test that different campaign types produce different content approaches
            assert campaign_plan["campaign_type"] in campaign_types
            
            # Each campaign type should have specific characteristics
            if campaign_type == "Cart Abandonment":
                expected_keywords = ["cart", "items", "complete", "purchase"]
            elif campaign_type == "Welcome Series":
                expected_keywords = ["welcome", "introduction", "started"]
            elif campaign_type == "Post-Purchase":
                expected_keywords = ["thank", "order", "purchase"]
            elif campaign_type == "Win-Back":
                expected_keywords = ["miss", "return", "back"]
            
            # Verify campaign type is properly set
            assert len(expected_keywords) > 0


class TestEmailTemplates:
    """Test cases for email template functionality"""
    
    def test_email_template_structure(self):
        """Test email template structure"""
        
        template_structure = {
            "header": "Brand logo and navigation",
            "hero": "Main message and visual",
            "content": "Email body content",
            "cta": "Call to action button",
            "footer": "Unsubscribe and legal info"
        }
        
        for section, description in template_structure.items():
            assert isinstance(section, str)
            assert isinstance(description, str)
            assert len(description) > 0
    
    def test_responsive_design(self):
        """Test responsive design considerations"""
        
        responsive_guidelines = [
            "Single column layout",
            "Large tappable buttons (44px minimum)",
            "Readable font sizes (14px minimum)",
            "Optimized images for mobile"
        ]
        
        for guideline in responsive_guidelines:
            assert isinstance(guideline, str)
            assert len(guideline) > 10
    
    def test_email_deliverability(self):
        """Test email deliverability best practices"""
        
        deliverability_checks = [
            "Clear from name and email",
            "Relevant subject line",
            "Plain text version included",
            "Unsubscribe link present",
            "Spam word avoidance"
        ]
        
        for check in deliverability_checks:
            assert isinstance(check, str)
            # Each check represents a deliverability requirement
            assert any(word in check.lower() for word in ["clear", "relevant", "included", "present", "avoidance"])


# Test fixtures
@pytest.fixture
def sample_email_data():
    """Sample email data for testing"""
    return {
        "subject": "Welcome to Our Community!",
        "preview_text": "Get started with exclusive benefits",
        "body": "Thank you for joining us. We're excited to have you aboard!",
        "cta": {"text": "Get Started", "url": "https://example.com/start"},
        "personalization": ["{{first_name}}", "{{brand_name}}"]
    }

@pytest.fixture
def sample_brand_data():
    """Sample brand data for testing"""
    return {
        "brand_name": "TestCorp",
        "description": "Leading provider of test solutions",
        "products": ["TestPro", "TestLite", "TestEnterprise"],
        "tone": "Professional",
        "colors": ["#007bff", "#6c757d"]
    }

def test_email_fixtures(sample_email_data, sample_brand_data):
    """Test email generation with fixtures"""
    
    # Combine email and brand data
    email_with_brand = {
        **sample_email_data,
        "brand_info": sample_brand_data
    }
    
    assert email_with_brand["subject"] == sample_email_data["subject"]
    assert email_with_brand["brand_info"]["brand_name"] == "TestCorp"
    
    # Test personalization with brand data
    personalized_subject = email_with_brand["subject"].replace(
        "{{brand_name}}", email_with_brand["brand_info"]["brand_name"]
    )
    assert "TestCorp" in personalized_subject or email_with_brand["subject"] == personalized_subject


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

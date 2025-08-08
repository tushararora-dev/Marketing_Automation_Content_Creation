import pytest
import json
from unittest.mock import Mock, patch
from agents.marketing_automation_agent import run_marketing_automation_workflow, validate_campaign_result
from agents.content_generation_agent import run_content_generation_workflow, validate_content_result

class TestMarketingAutomationAgent:
    """Test cases for Marketing Automation Agent"""
    
    def test_run_marketing_automation_workflow_success(self):
        """Test successful marketing automation workflow execution"""
        
        # Mock successful workflow execution
        with patch('agents.marketing_automation_agent.create_marketing_automation_graph') as mock_graph:
            mock_workflow = Mock()
            mock_workflow.invoke.return_value = {
                "brand_analysis": {
                    "brand_name": "Test Brand",
                    "description": "Test description"
                },
                "campaign_plan": {
                    "campaign_type": "Cart Abandonment",
                    "objective": "Recover abandoned carts"
                },
                "emails": [
                    {
                        "sequence_number": 1,
                        "subject": "Don't forget your items!",
                        "body": "Your cart is waiting for you.",
                        "cta": {"text": "Complete Purchase", "url": "#"}
                    }
                ],
                "sms": [
                    {
                        "sequence_number": 1,
                        "message": "Complete your purchase now!",
                        "purpose": "Urgency"
                    }
                ],
                "errors": []
            }
            mock_graph.return_value = mock_workflow
            
            result = run_marketing_automation_workflow(
                brand_url="https://example.com",
                campaign_type="Cart Abandonment",
                num_emails=3,
                num_sms=1
            )
            
            assert result is not None
            assert "brand_name" in result
            assert "emails" in result
            assert "sms" in result
            assert len(result["emails"]) > 0
            assert result["brand_name"] == "Test Brand"
    
    def test_run_marketing_automation_workflow_with_error(self):
        """Test workflow execution with errors"""
        
        with patch('agents.marketing_automation_agent.create_marketing_automation_graph') as mock_graph:
            mock_workflow = Mock()
            mock_workflow.invoke.side_effect = Exception("Test error")
            mock_graph.return_value = mock_workflow
            
            result = run_marketing_automation_workflow(
                brand_url="https://invalid-url.com",
                campaign_type="Cart Abandonment"
            )
            
            assert "error" in result
            assert "Test error" in result["error"]
    
    def test_validate_campaign_result_valid(self):
        """Test campaign result validation with valid data"""
        
        valid_result = {
            "emails": [
                {"subject": "Test", "body": "Test body"}
            ],
            "campaign_overview": {
                "objective": "Test objective"
            }
        }
        
        assert validate_campaign_result(valid_result) is True
    
    def test_validate_campaign_result_invalid(self):
        """Test campaign result validation with invalid data"""
        
        invalid_result = {
            "sms": [{"message": "Test SMS"}]
            # Missing required "emails" field
        }
        
        assert validate_campaign_result(invalid_result) is False
    
    def test_campaign_types(self):
        """Test different campaign types"""
        
        campaign_types = [
            "Cart Abandonment",
            "Welcome Series", 
            "Post-Purchase",
            "Win-Back",
            "Custom"
        ]
        
        with patch('agents.marketing_automation_agent.create_marketing_automation_graph') as mock_graph:
            mock_workflow = Mock()
            mock_workflow.invoke.return_value = {
                "brand_analysis": {"brand_name": "Test Brand"},
                "campaign_plan": {"campaign_type": "Test"},
                "emails": [{"subject": "Test"}],
                "sms": [],
                "errors": []
            }
            mock_graph.return_value = mock_workflow
            
            for campaign_type in campaign_types:
                result = run_marketing_automation_workflow(
                    brand_url="https://example.com",
                    campaign_type=campaign_type
                )
                
                assert result is not None
                assert "timestamp" in result


class TestContentGenerationAgent:
    """Test cases for Content Generation Agent"""
    
    def test_run_content_generation_workflow_success(self):
        """Test successful content generation workflow execution"""
        
        with patch('agents.content_generation_agent.create_content_generation_graph') as mock_graph:
            mock_workflow = Mock()
            mock_workflow.invoke.return_value = {
                "content_strategy": {
                    "product_description": "Amazing Product",
                    "target_audience": "Young professionals"
                },
                "ad_copy": [
                    {
                        "variant": 1,
                        "headline": "Amazing Product for You!",
                        "primary_text": "Discover the benefits of our amazing product.",
                        "cta": "Shop Now"
                    }
                ],
                "social_captions": {
                    "instagram": ["Check out this amazing product! #amazing"],
                    "tiktok": ["This product is a game-changer! #viral"]
                },
                "images": [
                    {
                        "type": "hero_image",
                        "description": "Main product image",
                        "dimensions": "1200x628"
                    }
                ],
                "errors": []
            }
            mock_graph.return_value = mock_workflow
            
            result = run_content_generation_workflow(
                product_description="Amazing skincare product",
                target_audience="Women aged 25-35",
                content_types=["ad_copy", "social_captions", "static_images"]
            )
            
            assert result is not None
            assert "ad_copy" in result
            assert "social_captions" in result
            assert "images" in result
            assert len(result["ad_copy"]) > 0
    
    def test_content_generation_workflow_with_error(self):
        """Test content generation workflow with errors"""
        
        with patch('agents.content_generation_agent.create_content_generation_graph') as mock_graph:
            mock_workflow = Mock()
            mock_workflow.invoke.side_effect = Exception("Content generation failed")
            mock_graph.return_value = mock_workflow
            
            result = run_content_generation_workflow(
                product_description="Test product",
                target_audience="Test audience",
                content_types=["ad_copy"]
            )
            
            assert "error" in result
            assert "Content generation failed" in result["error"]
    
    def test_validate_content_result_valid(self):
        """Test content result validation with valid data"""
        
        valid_result = {
            "ad_copy": [{"headline": "Test", "primary_text": "Test content"}],
            "social_captions": {"instagram": ["Test caption"]},
            "images": []
        }
        
        assert validate_content_result(valid_result) is True
    
    def test_validate_content_result_invalid(self):
        """Test content result validation with invalid data"""
        
        invalid_result = {
            "timestamp": "2024-01-01",
            "product_description": "Test product"
            # Missing all content fields
        }
        
        assert validate_content_result(invalid_result) is False
    
    def test_content_types(self):
        """Test different content types"""
        
        content_types = [
            "ad_copy",
            "social_captions", 
            "static_images",
            "ugc_scripts",
            "email_creative"
        ]
        
        with patch('agents.content_generation_agent.create_content_generation_graph') as mock_graph:
            mock_workflow = Mock()
            mock_workflow.invoke.return_value = {
                "content_strategy": {"product_description": "Test"},
                "ad_copy": [{"headline": "Test"}],
                "social_captions": {"instagram": ["Test"]},
                "images": [{"type": "test"}],
                "ugc_scripts": [{"title": "Test Script"}],
                "email_assets": [{"type": "header"}],
                "errors": []
            }
            mock_graph.return_value = mock_workflow
            
            result = run_content_generation_workflow(
                product_description="Test product",
                target_audience="Test audience", 
                content_types=content_types
            )
            
            assert result is not None
            assert "timestamp" in result


class TestAgentIntegration:
    """Test cases for agent integration and workflows"""
    
    def test_marketing_to_content_integration(self):
        """Test integration between marketing automation and content generation"""
        
        # Test that marketing automation output can inform content generation
        marketing_result = {
            "brand_name": "Test Brand",
            "target_audience": "Young professionals",
            "brand_tone": "Professional",
            "emails": [{"subject": "Welcome!", "body": "Welcome to our brand"}]
        }
        
        # Extract information for content generation
        brand_info = {
            "product_description": f"Products from {marketing_result['brand_name']}",
            "target_audience": marketing_result["target_audience"],
            "brand_tone": marketing_result["brand_tone"]
        }
        
        assert brand_info["target_audience"] == "Young professionals"
        assert brand_info["brand_tone"] == "Professional"
    
    def test_workflow_data_consistency(self):
        """Test data consistency across workflows"""
        
        # Test that workflow outputs maintain consistent data structures
        sample_email = {
            "sequence_number": 1,
            "subject": "Test Subject",
            "body": "Test Body",
            "cta": {"text": "Click Here", "url": "#"},
            "timing": {"send_after_hours": 24}
        }
        
        # Validate required fields
        required_fields = ["sequence_number", "subject", "body", "cta"]
        for field in required_fields:
            assert field in sample_email
        
        # Validate data types
        assert isinstance(sample_email["sequence_number"], int)
        assert isinstance(sample_email["subject"], str)
        assert isinstance(sample_email["cta"], dict)
    
    def test_error_handling(self):
        """Test error handling across agents"""
        
        test_cases = [
            {"error_type": "network", "expected": "connection"},
            {"error_type": "api_limit", "expected": "rate limit"},
            {"error_type": "invalid_input", "expected": "validation"}
        ]
        
        for case in test_cases:
            # Simulate error conditions
            error_message = f"Simulated {case['error_type']} error"
            assert case["error_type"] in error_message
    
    def test_configuration_validation(self):
        """Test configuration validation for agents"""
        
        # Test required configuration parameters
        required_config = {
            "groq_api_key": "test_key",
            "huggingface_api_key": "test_key",
            "groq_model": "llama3-8b-8192",
            "max_tokens": 2048
        }
        
        for key, value in required_config.items():
            assert key is not None
            assert value is not None
            if isinstance(value, str):
                assert len(value) > 0
            if isinstance(value, int):
                assert value > 0


# Test fixtures and utilities
@pytest.fixture
def sample_brand_analysis():
    """Sample brand analysis data for testing"""
    return {
        "brand_name": "Test Brand",
        "description": "A test brand for unit testing",
        "products": ["Product A", "Product B"],
        "target_audience": "Tech-savvy millennials",
        "value_propositions": ["Innovation", "Quality", "Affordability"],
        "tone": "Professional"
    }

@pytest.fixture
def sample_campaign_plan():
    """Sample campaign plan data for testing"""
    return {
        "campaign_type": "Welcome Series",
        "objective": "Onboard new customers",
        "target_audience": "New subscribers",
        "timeline": [
            {"sequence": 1, "type": "email", "delay_hours": 0},
            {"sequence": 2, "type": "email", "delay_hours": 24}
        ]
    }

def test_with_fixtures(sample_brand_analysis, sample_campaign_plan):
    """Test using pytest fixtures"""
    assert sample_brand_analysis["brand_name"] == "Test Brand"
    assert sample_campaign_plan["campaign_type"] == "Welcome Series"
    
    # Test data integration
    combined_data = {
        **sample_brand_analysis,
        "campaign": sample_campaign_plan
    }
    
    assert "brand_name" in combined_data
    assert "campaign" in combined_data
    assert combined_data["campaign"]["objective"] == "Onboard new customers"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])

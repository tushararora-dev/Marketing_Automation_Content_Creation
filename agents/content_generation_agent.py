import json
import time
from datetime import datetime
from typing import Dict, List, Any
from langgraph.graph import StateGraph, END
from workflows.content_generation.ad_writer import generate_ad_copy
from workflows.content_generation.static_image_gen import generate_static_images
from workflows.content_generation.ugc_script_gen import generate_ugc_scripts
from workflows.content_generation.video_editor import generate_video_content
from workflows.content_generation.asset_packager import package_assets

def create_content_generation_graph():
    """Create the LangGraph workflow for content generation"""
    
    def analyze_requirements_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to analyze content requirements"""
        try:
            # Process and validate content requirements
            content_strategy = {
                "product_description": state["product_description"],
                "target_audience": state["target_audience"],
                "content_types": state["content_types"],
                "brand_tone": state["brand_tone"],
                "brand_colors": state.get("brand_colors", ""),
                "content_pillars": extract_content_pillars(state["product_description"]),
                "key_messages": extract_key_messages(state["product_description"], state["target_audience"])
            }
            state["content_strategy"] = content_strategy
            return state
        except Exception as e:
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Requirements analysis failed: {str(e)}")
            return state
    
    def generate_ad_copy_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate ad copy content"""
        try:
            if "ad_copy" in state["content_types"]:
                ad_copy = generate_ad_copy(
                    content_strategy=state["content_strategy"],
                    target_audience=state["target_audience"],
                    brand_tone=state["brand_tone"]
                )
                state["ad_copy"] = ad_copy
            return state
        except Exception as e:
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Ad copy generation failed: {str(e)}")
            return state
    
    def generate_social_content_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate social media content"""
        try:
            if "social_captions" in state["content_types"]:
                from workflows.content_generation.ad_writer import generate_social_captions
                social_captions = generate_social_captions(
                    content_strategy=state["content_strategy"],
                    target_audience=state["target_audience"],
                    brand_tone=state["brand_tone"]
                )
                state["social_captions"] = social_captions
            return state
        except Exception as e:
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Social content generation failed: {str(e)}")
            return state
    
    def generate_images_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate static images"""
        try:
            if "static_images" in state["content_types"] or "product_visuals" in state["content_types"]:
                images = generate_static_images(
                    content_strategy=state["content_strategy"],
                    brand_colors=state.get("brand_colors", ""),
                    include_product_visuals="product_visuals" in state["content_types"]
                )
                state["images"] = images
            return state
        except Exception as e:
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Image generation failed: {str(e)}")
            return state
    
    def generate_video_scripts_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate UGC video scripts"""
        try:
            if "ugc_scripts" in state["content_types"]:
                ugc_scripts = generate_ugc_scripts(
                    content_strategy=state["content_strategy"],
                    target_audience=state["target_audience"],
                    brand_tone=state["brand_tone"]
                )
                state["ugc_scripts"] = ugc_scripts
            return state
        except Exception as e:
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Video script generation failed: {str(e)}")
            return state
    
    def generate_email_assets_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate email creative assets"""
        try:
            if "email_creative" in state["content_types"]:
                from workflows.content_generation.static_image_gen import generate_email_assets
                email_assets = generate_email_assets(
                    content_strategy=state["content_strategy"],
                    brand_colors=state.get("brand_colors", "")
                )
                state["email_assets"] = email_assets
            return state
        except Exception as e:
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Email asset generation failed: {str(e)}")
            return state
    
    def package_final_assets_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to package all generated assets"""
        try:
            final_package = package_assets(
                ad_copy=state.get("ad_copy", []),
                social_captions=state.get("social_captions", {}),
                images=state.get("images", []),
                ugc_scripts=state.get("ugc_scripts", []),
                email_assets=state.get("email_assets", []),
                content_strategy=state["content_strategy"]
            )
            state["final_package"] = final_package
            return state
        except Exception as e:
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Asset packaging failed: {str(e)}")
            return state
    
    # Create the workflow graph
    workflow = StateGraph(dict)
    
    # Add nodes
    workflow.add_node("analyze_requirements", analyze_requirements_node)
    workflow.add_node("generate_ad_copy", generate_ad_copy_node)
    workflow.add_node("generate_social_content", generate_social_content_node)
    workflow.add_node("generate_images", generate_images_node)
    workflow.add_node("generate_video_scripts", generate_video_scripts_node)
    workflow.add_node("generate_email_assets", generate_email_assets_node)
    workflow.add_node("package_assets", package_final_assets_node)
    
    # Define the workflow edges
    workflow.set_entry_point("analyze_requirements")
    workflow.add_edge("analyze_requirements", "generate_ad_copy")
    workflow.add_edge("generate_ad_copy", "generate_social_content")
    workflow.add_edge("generate_social_content", "generate_images")
    workflow.add_edge("generate_images", "generate_video_scripts")
    workflow.add_edge("generate_video_scripts", "generate_email_assets")
    workflow.add_edge("generate_email_assets", "package_assets")
    workflow.add_edge("package_assets", END)
    
    return workflow.compile()

def extract_content_pillars(product_description: str) -> List[str]:
    """Extract key content pillars from product description"""
    # Simple keyword extraction - in production, this would use more sophisticated NLP
    pillars = []
    
    # Common content pillar keywords
    pillar_keywords = {
        "quality": ["quality", "premium", "high-quality", "superior"],
        "benefits": ["benefit", "advantage", "help", "improve", "enhance"],
        "lifestyle": ["lifestyle", "daily", "routine", "life", "living"],
        "innovation": ["innovative", "new", "technology", "advanced", "cutting-edge"],
        "sustainability": ["eco", "sustainable", "green", "environment", "natural"],
        "value": ["affordable", "value", "price", "cost-effective", "savings"]
    }
    
    description_lower = product_description.lower()
    
    for pillar, keywords in pillar_keywords.items():
        if any(keyword in description_lower for keyword in keywords):
            pillars.append(pillar)
    
    return pillars[:4]  # Return top 4 pillars

def extract_key_messages(product_description: str, target_audience: str) -> List[str]:
    """Extract key marketing messages"""
    messages = []
    
    # Extract product benefits
    if "health" in product_description.lower():
        messages.append("Supports your health and wellness goals")
    
    if "time" in product_description.lower() or "busy" in target_audience.lower():
        messages.append("Saves you time and effort")
    
    if "eco" in product_description.lower() or "sustainable" in product_description.lower():
        messages.append("Environmentally conscious choice")
    
    if "premium" in product_description.lower() or "quality" in product_description.lower():
        messages.append("Premium quality you can trust")
    
    # Default message
    if not messages:
        messages.append("Perfect solution for your needs")
    
    return messages

def run_content_generation_workflow(
    product_description: str,
    target_audience: str,
    content_types: List[str],
    brand_tone: str = "Professional",
    brand_colors: str = ""
) -> Dict[str, Any]:
    """
    Run the complete content generation workflow
    
    Args:
        product_description: Description of the product/service
        target_audience: Target audience description
        content_types: List of content types to generate
        brand_tone: Brand tone/voice
        brand_colors: Brand color scheme
    
    Returns:
        Complete content package with all generated assets
    """
    
    # Initialize workflow state
    initial_state = {
        "product_description": product_description,
        "target_audience": target_audience,
        "content_types": content_types,
        "brand_tone": brand_tone,
        "brand_colors": brand_colors,
        "errors": []
    }
    
    # Create and run the workflow
    workflow = create_content_generation_graph()
    
    try:
        result = workflow.invoke(initial_state)
        
        # Format the final result
        content_result = {
            "timestamp": datetime.now().isoformat(),
            "product_description": product_description,
            "target_audience": target_audience,
            "brand_tone": brand_tone,
            "ad_copy": result.get("ad_copy", []),
            "social_captions": result.get("social_captions", {}),
            "images": result.get("images", []),
            "ugc_scripts": result.get("ugc_scripts", []),
            "email_assets": result.get("email_assets", []),
            "final_package": result.get("final_package", {}),
            "errors": result.get("errors", [])
        }
        
        return content_result
        
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "error": f"Content generation workflow failed: {str(e)}",
            "product_description": product_description
        }

def validate_content_result(result: Dict[str, Any]) -> bool:
    """Validate that the content result contains required elements"""
    # Check if at least one content type was generated successfully
    content_fields = ["ad_copy", "social_captions", "images", "ugc_scripts", "email_assets"]
    return any(result.get(field) for field in content_fields)

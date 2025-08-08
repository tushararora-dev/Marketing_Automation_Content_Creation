import json
import time
from datetime import datetime
from typing import Dict, List, Any
from langgraph.graph import StateGraph, END
from tools.browser_utils import analyze_brand_from_url
from workflows.marketing_automation.planner import plan_campaign
from workflows.marketing_automation.email_generator import generate_emails
from workflows.marketing_automation.sms_generator import generate_sms
from workflows.marketing_automation.visual_generator import generate_visuals
from workflows.marketing_automation.flow_builder import build_campaign_flow

# Define the workflow state
class MarketingWorkflowState:
    def __init__(self):
        self.brand_analysis = None
        self.campaign_plan = None
        self.emails = []
        self.sms = []
        self.visuals = []
        self.campaign_flow = None
        self.errors = []

def create_marketing_automation_graph():
    """Create the LangGraph workflow for marketing automation"""
    
    def analyze_brand_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to analyze brand from URL"""
        try:
            brand_url = state["brand_url"]
            brand_analysis = analyze_brand_from_url(brand_url)
            state["brand_analysis"] = brand_analysis
            return state
        except Exception as e:
            state["errors"].append(f"Brand analysis failed: {str(e)}")
            return state
    
    def plan_campaign_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to plan the marketing campaign"""
        try:
            campaign_plan = plan_campaign(
                brand_analysis=state["brand_analysis"],
                campaign_type=state["campaign_type"],
                custom_prompt=state.get("custom_prompt", ""),
                num_emails=state["num_emails"],
                num_sms=state["num_sms"],
                target_audience=state["target_audience"],
                tone=state["tone"]
            )
            state["campaign_plan"] = campaign_plan
            return state
        except Exception as e:
            state["errors"].append(f"Campaign planning failed: {str(e)}")
            return state
    
    def generate_emails_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate email content"""
        try:
            emails = generate_emails(
                brand_analysis=state["brand_analysis"],
                campaign_plan=state["campaign_plan"],
                num_emails=state["num_emails"],
                tone=state["tone"]
            )
            state["emails"] = emails
            return state
        except Exception as e:
            state["errors"].append(f"Email generation failed: {str(e)}")
            return state
    
    def generate_sms_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate SMS content"""
        try:
            if state["num_sms"] > 0:
                sms = generate_sms(
                    brand_analysis=state["brand_analysis"],
                    campaign_plan=state["campaign_plan"],
                    num_sms=state["num_sms"],
                    tone=state["tone"]
                )
                state["sms"] = sms
            return state
        except Exception as e:
            state["errors"].append(f"SMS generation failed: {str(e)}")
            return state
    
    def generate_visuals_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to generate visual assets"""
        try:
            visuals = generate_visuals(
                brand_analysis=state["brand_analysis"],
                campaign_plan=state["campaign_plan"],
                emails=state["emails"]
            )
            state["visuals"] = visuals
            return state
        except Exception as e:
            state["errors"].append(f"Visual generation failed: {str(e)}")
            return state
    
    def build_flow_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Node to build the complete campaign flow"""
        try:
            campaign_flow = build_campaign_flow(
                campaign_plan=state["campaign_plan"],
                emails=state["emails"],
                sms=state["sms"],
                visuals=state["visuals"]
            )
            state["campaign_flow"] = campaign_flow
            return state
        except Exception as e:
            state["errors"].append(f"Flow building failed: {str(e)}")
            return state
    
    # Create the workflow graph
    workflow = StateGraph(dict)
    
    # Add nodes
    workflow.add_node("analyze_brand", analyze_brand_node)
    workflow.add_node("plan_campaign", plan_campaign_node)
    workflow.add_node("generate_emails", generate_emails_node)
    workflow.add_node("generate_sms", generate_sms_node)
    workflow.add_node("generate_visuals", generate_visuals_node)
    workflow.add_node("build_flow", build_flow_node)
    
    # Define the workflow edges
    workflow.set_entry_point("analyze_brand")
    workflow.add_edge("analyze_brand", "plan_campaign")
    workflow.add_edge("plan_campaign", "generate_emails")
    workflow.add_edge("generate_emails", "generate_sms")
    workflow.add_edge("generate_sms", "generate_visuals")
    workflow.add_edge("generate_visuals", "build_flow")
    workflow.add_edge("build_flow", END)
    
    return workflow.compile()

def run_marketing_automation_workflow(
    brand_url: str,
    campaign_type: str,
    custom_prompt: str = "",
    num_emails: int = 5,
    num_sms: int = 2,
    target_audience: str = "General customers",
    tone: str = "Professional"
) -> Dict[str, Any]:
    """
    Run the complete marketing automation workflow
    
    Args:
        brand_url: URL of the brand website to analyze
        campaign_type: Type of campaign to create
        custom_prompt: Custom instructions for the campaign
        num_emails: Number of emails to generate
        num_sms: Number of SMS messages to generate
        target_audience: Target audience description
        tone: Campaign tone
    
    Returns:
        Complete campaign data including emails, SMS, visuals, and flow
    """
    
    # Initialize workflow state
    initial_state = {
        "brand_url": brand_url,
        "campaign_type": campaign_type,
        "custom_prompt": custom_prompt,
        "num_emails": num_emails,
        "num_sms": num_sms,
        "target_audience": target_audience,
        "tone": tone,
        "errors": []
    }
    
    # Create and run the workflow
    workflow = create_marketing_automation_graph()
    
    try:
        result = workflow.invoke(initial_state)
        
        # Format the final result
        campaign_result = {
            "timestamp": datetime.now().isoformat(),
            "brand_name": result.get("brand_analysis", {}).get("brand_name", "Unknown"),
            "campaign_type": campaign_type,
            "campaign_overview": result.get("campaign_plan", {}),
            "emails": result.get("emails", []),
            "sms": result.get("sms", []),
            "visuals": result.get("visuals", []),
            "campaign_flow": result.get("campaign_flow", {}),
            "errors": result.get("errors", [])
        }
        
        return campaign_result
        
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "error": f"Workflow execution failed: {str(e)}",
            "campaign_type": campaign_type
        }

def validate_campaign_result(result: Dict[str, Any]) -> bool:
    """Validate that the campaign result contains required elements"""
    required_fields = ["emails", "campaign_overview"]
    return all(field in result for field in required_fields)

def save_campaign_to_memory(campaign_result: Dict[str, Any], brand_name: str) -> None:
    """Save campaign result to memory for future reference"""
    import os
    
    memory_dir = "memory"
    os.makedirs(memory_dir, exist_ok=True)
    
    memory_file = f"{memory_dir}/{brand_name.lower().replace(' ', '_')}_memory.json"
    
    # Load existing memory or create new
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            memory = json.load(f)
    else:
        memory = {"brand_name": brand_name, "campaigns": []}
    
    # Add new campaign
    memory["campaigns"].append(campaign_result)
    
    # Keep only last 10 campaigns
    if len(memory["campaigns"]) > 10:
        memory["campaigns"] = memory["campaigns"][-10:]
    
    # Save updated memory
    with open(memory_file, 'w') as f:
        json.dump(memory, f, indent=2)

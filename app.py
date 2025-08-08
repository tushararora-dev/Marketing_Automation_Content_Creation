import streamlit as st
import json
import os
from pathlib import Path
from agents.marketing_automation_agent import run_marketing_automation_workflow
from agents.content_generation_agent import run_content_generation_workflow
from tools.browser_utils import analyze_brand_from_url
from config.settings import load_config

# Initialize configuration
config = load_config()

def main():
    st.set_page_config(
        page_title="Agentic AI Marketing Tools",
        page_icon="📢",
        layout="wide"
    )
    
    st.title("🚀 Agentic AI Marketing Automation & Content Creation")
    st.markdown("Automate your marketing campaigns and content generation with AI-powered workflows")
    
    # Sidebar for navigation
    st.sidebar.title("👉 Navigation")
    selected_agent = st.sidebar.selectbox(
        "Choose Agent",
        ["Marketing Automation Agent", "Content Generation Agent"]
    )
    
    if selected_agent == "Marketing Automation Agent":
        marketing_automation_interface()
    else:
        st.sidebar.title("⚙️ Features")
        st.sidebar.write("✅ Prompt-to-Content Generation")
        st.sidebar.write("❌ Ad & Social Content Creation")
        st.sidebar.write("❌ Creative Asset Generation")
        st.sidebar.write("❌ UGC/Video Content Scripting & Editing")
        st.sidebar.write("❌ Rich Media / Interactive Content")
        st.sidebar.write("❌ Edit, Iterate, Personalize")
        st.sidebar.write("❌ Integration & Deployment")
        st.sidebar.write("❌ Modularity & Reusability")
        content_generation_interface()

def marketing_automation_interface():
    st.header("📧 Marketing Automation Agent")
    st.markdown("Create complete email and SMS marketing sequences from brand analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Campaign Configuration")
        
        # Brand URL input
        brand_url = st.text_input(
            "Brand Website URL",
            placeholder="https://example.com",
            help="Enter the brand's website URL for analysis"
        )
        
        # Campaign type selection
        campaign_type = st.selectbox(
            "Campaign Type",
            ["Cart Abandonment", "Welcome Series", "Post-Purchase", "Win-Back", "Custom"]
        )
        
        # Custom prompt for detailed instructions
        if campaign_type == "Custom":
            custom_prompt = st.text_area(
                "Custom Campaign Instructions",
                placeholder="Describe the specific campaign you want to create...",
                height=100
            )
        else:
            custom_prompt = f"Create a {campaign_type.lower()} campaign"
        
        # Campaign parameters
        st.subheader("Campaign Parameters")
        col_a, col_b = st.columns(2)
        
        with col_a:
            num_emails = st.slider("Number of Emails", 1, 10, 5)
            num_sms = st.slider("Number of SMS", 0, 5, 2)
        
        with col_b:
            target_audience = st.text_input("Target Audience", "General customers")
            campaign_tone = st.selectbox("Campaign Tone", ["Professional", "Casual", "Urgent", "Friendly"])
        
        # Generate campaign button
        if st.button("🚀 Generate Marketing Campaign", type="primary"):
            if brand_url:
                with st.spinner("Analyzing brand and generating campaign..."):
                    try:
                        # Run the marketing automation workflow
                        result = run_marketing_automation_workflow(
                            brand_url=brand_url,
                            campaign_type=campaign_type,
                            custom_prompt=custom_prompt,
                            num_emails=num_emails,
                            num_sms=num_sms,
                            target_audience=target_audience,
                            tone=campaign_tone
                        )
                        
                        st.session_state.marketing_result = result
                        st.success("Campaign generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Error generating campaign: {str(e)}")
            else:
                st.warning("Please enter a brand URL")
    
    with col2:
        st.subheader("Recent Campaigns")
        # Display recent campaigns from memory
        memory_path = Path("memory")
        if memory_path.exists():
            memory_files = list(memory_path.glob("*.json"))
            if memory_files:
                for file in memory_files[-3:]:  # Show last 3
                    brand_name = file.stem.replace("_memory", "")
                    st.write(f"📁 {brand_name}")
            else:
                st.write("No previous campaigns")
        else:
            st.write("No previous campaigns")
    
    # Display results
    if hasattr(st.session_state, 'marketing_result') and st.session_state.marketing_result:
        display_marketing_results(st.session_state.marketing_result)

def content_generation_interface():
    st.header("🎨 Content Generation Agent")
    st.markdown("Create multi-format content for advertising campaigns")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Content Configuration")
        
        # Product/service description
        product_description = st.text_area(
            "Product/Service Description",
            placeholder="Describe the product or service you want to create content for...",
            height=100
        )
        
        # Target audience
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., busy moms aged 30-45, Gen Z health enthusiasts"
        )
        
        # Content types
        st.subheader("Content Types")
        content_types = []
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.checkbox("Ad Copy (Headlines, CTAs)", value=True):
                content_types.append("ad_copy")
            if st.checkbox("Social Media Captions"):
                content_types.append("social_captions")
            if st.checkbox("Email Creative Assets"):
                content_types.append("email_creative")
        
        with col_b:
            if st.checkbox("Static Images"):
                content_types.append("static_images")
            if st.checkbox("UGC Video Scripts"):
                content_types.append("ugc_scripts")
            if st.checkbox("Product Visuals"):
                content_types.append("product_visuals")
        
        # Brand guidelines
        st.subheader("Brand Guidelines")
        brand_tone = st.selectbox("Brand Tone", ["Professional", "Casual", "Playful", "Luxury", "Eco-friendly"])
        brand_colors = st.text_input("Brand Colors (optional)", placeholder="e.g., #FF6B6B, #4ECDC4")
        
        # Generate content button
        if st.button("🎨 Generate Content", type="primary"):
            if product_description and target_audience and content_types:
                with st.spinner("Generating content assets..."):
                    try:
                        # Run the content generation workflow
                        result = run_content_generation_workflow(
                            product_description=product_description,
                            target_audience=target_audience,
                            content_types=content_types,
                            brand_tone=brand_tone,
                            brand_colors=brand_colors
                        )
                        
                        st.session_state.content_result = result
                        st.success("Content generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Error generating content: {str(e)}")
            else:
                st.warning("Please fill in all required fields and select at least one content type")
    
    with col2:
        st.subheader("Content Templates")
        st.write("🎯 Ad Copy Templates")
        st.write("📱 Social Media Templates")
        st.write("🖼️ Visual Asset Templates")
        st.write("🎬 Video Script Templates")
    
    # Display results
    if hasattr(st.session_state, 'content_result') and st.session_state.content_result:
        display_content_results(st.session_state.content_result)

def display_marketing_results(result):
    st.header("📊 Generated Marketing Campaign")
    
    # Campaign overview
    if 'campaign_overview' in result:
        st.subheader("Campaign Overview")
        st.json(result['campaign_overview'])
    
    # Email sequence
    if 'emails' in result:
        st.subheader("📧 Email Sequence")
        for i, email in enumerate(result['emails'], 1):
            with st.expander(f"Email {i}: {email.get('subject', 'No Subject')}"):
                st.write("**Subject Line:**", email.get('subject', ''))
                st.write("**Body:**")
                st.write(email.get('body', ''))
                if 'cta' in email:
                    st.write("**Call to Action:**", email['cta'])
    
    # SMS sequence
    if 'sms' in result:
        st.subheader("📱 SMS Sequence")
        for i, sms in enumerate(result['sms'], 1):
            with st.expander(f"SMS {i}"):
                st.write(sms.get('message', ''))
    
    # Export options
    st.subheader("📥 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export as JSON"):
            export_path = f"export/campaign_{result.get('brand_name', 'unknown')}.json"
            with open(export_path, 'w') as f:
                json.dump(result, f, indent=2)
            st.success(f"Exported to {export_path}")
    
    with col2:
        if st.button("Export for Klaviyo"):
            st.info("Klaviyo export functionality coming soon")
    
    with col3:
        if st.button("Save to Memory"):
            save_to_memory(result)
            st.success("Saved to memory")

def display_content_results(result):
    st.header("🎨 Generated Content Assets")
    
    # Ad copy
    if 'ad_copy' in result:
        st.subheader("🎯 Ad Copy")
        for i, copy in enumerate(result['ad_copy'], 1):
            with st.expander(f"Ad Copy Variant {i}"):
                st.write("**Headline:**", copy.get('headline', ''))
                st.write("**Primary Text:**", copy.get('primary_text', ''))
                st.write("**CTA:**", copy.get('cta', ''))
    
    # Social media captions
    if 'social_captions' in result:
        st.subheader("📱 Social Media Captions")
        for platform, captions in result['social_captions'].items():
            with st.expander(f"{platform.title()} Captions"):
                for i, caption in enumerate(captions, 1):
                    st.write(f"**Caption {i}:**")
                    st.write(caption)
    
    # Generated images
    if 'images' in result:
        st.subheader("🖼️ Generated Images")
        for image_info in result['images']:
            st.write(f"**{image_info['type']}:** {image_info['description']}")
            if 'url' in image_info:
                st.image(image_info['url'])
    
    # UGC scripts
    if 'ugc_scripts' in result:
        st.subheader("🎬 UGC Video Scripts")
        for i, script in enumerate(result['ugc_scripts'], 1):
            with st.expander(f"Script {i}: {script.get('title', '')}"):
                st.write("**Duration:**", script.get('duration', ''))
                st.write("**Script:**")
                st.write(script.get('script', ''))
    
    # Export options
    st.subheader("📥 Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Content Package"):
            export_path = f"export/content_package_{result.get('timestamp', 'unknown')}.json"
            with open(export_path, 'w') as f:
                json.dump(result, f, indent=2)
            st.success(f"Exported to {export_path}")
    
    with col2:
        if st.button("Download Assets"):
            st.info("Asset download functionality coming soon")

def save_to_memory(result):
    """Save campaign result to memory for future reference"""
    brand_name = result.get('brand_name', 'unknown_brand')
    memory_file = f"memory/{brand_name}_memory.json"
    
    # Create memory directory if it doesn't exist
    os.makedirs("memory", exist_ok=True)
    
    # Load existing memory or create new
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            memory = json.load(f)
    else:
        memory = {"brand_name": brand_name, "campaigns": []}
    
    # Add new campaign
    memory["campaigns"].append(result)
    
    # Save updated memory
    with open(memory_file, 'w') as f:
        json.dump(memory, f, indent=2)

if __name__ == "__main__":
    main()

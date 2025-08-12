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
    
    st.title("📢 Agentic AI Tools for Marketing Automation & Content Creation")
    
    # Sidebar for navigation
    st.sidebar.title("👉 Navigation")
    selected_agent = st.sidebar.selectbox(
        "Choose Agent",
        [ "Marketing Automation Agent", "Content Generation Agent"]
    )
    
    if selected_agent == "Marketing Automation Agent":
        st.sidebar.markdown(
            """
            <h1 style='text-align: justify;'>🛠️ Features Prototype</h1>
            <p style='text-align: justify;'>Brand analysis based on a webpage from a website URL</p>
            <p style='text-align: justify;'>View structured campaign plan with detailed strategy</p>
            <p style='text-align: justify;'>Generate fully-written, conversion-focused email</p>
            <p style='text-align: justify;'>Generate conversion-focused SMS with Call to action</p>
            """,unsafe_allow_html=True)
        marketing_automation_interface()

    else:
        st.sidebar.markdown(
            """
            <h1 style='text-align: justify;'>🛠️ Features Prototype</h1>
            <p style='text-align: justify;'>Variants of ad copy (headlines, primary text, CTAS)</p>
            <p style='text-align: justify;'>Captions for Instagram, TikTok and Linkedin</p>
            <p style='text-align: justify;'>Static creatives for images (utilising AI design tools)</p>
            <p style='text-align: justify;'>Scripts for UGC-style videos or product demonstrations</p>
            """,
            unsafe_allow_html=True
        )


        content_generation_interface()
   

def marketing_automation_interface():
    st.header("📧 Marketing Automation Agent 📈")
    
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
        if st.button("🚨 Generate Marketing Campaign"):
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

        st.subheader("💡 Example : 1")
        st.text("Website URL : https://euron.one")
        st.subheader("💡 Example : 2")
        st.text("Website URL : https://amlgolabs.com")
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
    st.header("✍️ Content Generation Agent ✨")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Content Configuration")
        
        # Product/service description
        product_description = st.text_area(
            "Product/Service Description",
            placeholder="Describe the product or service you want to create content for e.g., Launch a matcha drink for Gen Z",
            height=100
        )
        
        # Target audience
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., aged 30-45, Gen Z health enthusiasts"
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
            if st.checkbox("Generate Logo (Coming Soon)", value=False, disabled=True):
                content_types.append("logo")
        
        with col_b:
            if st.checkbox("Static Images"):
                content_types.append("static_images")
            if st.checkbox("UGC Video Scripts"):
                content_types.append("ugc_scripts")
            if st.checkbox("Product Visuals"):
                content_types.append("product_visuals")
            if st.checkbox("AI Video Generator(Coming Soon)", value=False, disabled=True):
                content_types.append("product_visuals")
        
        # Brand guidelines
        st.subheader("Brand Guidelines")
        brand_tone = st.selectbox("Brand Tone", ["Professional", "Casual", "Playful", "Luxury", "Eco-friendly"])
        # brand_colors = st.text_input("Brand Colors (optional)", placeholder="e.g., #FF6B6B, #4ECDC4")
        brand_colors = None
        
        # Generate content button
        if st.button("🚨 Generate Content"):
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
                st.error("Please fill in all required fields and select at least one content type")
    
    with col2:
        st.subheader("💡 Example : 1")
        st.write("Product/Service Description: Launching a new eco-friendly shampoo")
        st.write("Target Audience: Busy mums, aged 30–45")
        st.subheader("💡 Example : 2")
        st.write("Product/Service Description: We’re launching a new matcha drink")
        st.write("Target Audience: Gen Z")



    
    # Display results
    if hasattr(st.session_state, 'content_result') and st.session_state.content_result:
        display_content_results(st.session_state.content_result)

def display_marketing_results(result):
    st.header("✍️ Generated Marketing Campaign ✨")
    
    # Campaign overview
    if result.get('campaign_overview'):
        st.subheader("📋 campaign overview ")
        # Create a copy without "full_plan"
        overview_display = {
            k: v for k, v in result['campaign_overview'].items() if k != "full_plan"}
        with st.expander("Parse Campaign Overview", expanded=True):
            st.json(overview_display)

        # Add separate expander for full_plan
        if result['campaign_overview'].get('full_plan'):
            with st.expander("Full Campaign Plan", expanded=False):
                st.write(result['campaign_overview']['full_plan'])

    
    # Email sequence
    if result.get('emails'):  # non-empty list
        st.subheader("📧 Email Sequence")
        for i, email in enumerate(result['emails'], 1):
            with st.expander(f"Email {i}: {email.get('subject', '')}"):
                st.write(email.get('body', ''))
    
    # SMS sequence
    if result.get('sms'):  # non-empty list
        st.subheader("📱 SMS Sequence")
        for i, sms in enumerate(result['sms'], 1):
            with st.expander(f"SMS {i}"):
                st.write(sms.get('full_response', ''))
    
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
    st.header("✍️ Content Generation Assets ✨")
    
    # Ad copy
    if result.get('ad_copy'):  # non-empty list
        st.subheader("🔥 Ads copy (headlines, primary text, CTAs)")
        for i, copy in enumerate(result['ad_copy'], 1):
            with st.expander(f"Ad Copy Variant {i}"):
                st.write("**Headline:**", copy.get('headline', ''))
                st.write("**Primary Text:**", copy.get('description', ''))
                st.write("**CTA:**", copy.get('cta', ''))
    
    # Social media captions
    if result.get('social_captions'):  # non-empty dict
        st.subheader("📱 Social Media Captions")
        for platform, captions in result['social_captions'].items():
            if captions:  # skip empty lists per platform
                with st.expander(f"{platform.title()} Captions"):
                    for i, caption in enumerate(captions, 1):
                        st.write(f"**Caption {i}:**")
                        st.write(caption)
    
    if result.get('images'):  # non-empty list
        st.subheader("🖼️ Generated Images")
        
        images = result['images']
        # Create two columns for every two images
        for i in range(0, len(images), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(images):
                    image_info = images[idx]
                    with col:
                        st.write(f"**{image_info['type']}:** {image_info['description']}")
                        if image_info.get("image_obj") is not None:
                            st.image(image_info["image_obj"], width=400)
                        else:
                            st.write("Image not available")

    
    # UGC scripts
    if result.get('ugc_scripts'):  # non-empty list
        st.subheader("🎬 UGC Video Scripts")
        for i, script in enumerate(result['ugc_scripts'], 1):
            with st.expander(f"Script {i}: {script.get('title', '')}"):
                st.write("**Duration:**", script.get('duration', ''))
                st.write("**Script:**")
                st.write(script.get('script', ''))

    # Email assets
    if result.get('email_assets'):  # non-empty list
        st.subheader("📧 Email Assets")
        
        email_assets = result['email_assets']
        # Create two columns for every two images
        for i in range(0, len(email_assets), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(email_assets):
                    image_info = email_assets[idx]
                    with col:
                        st.write(f"**{image_info['type']}:** {image_info['description']}")
                        if image_info.get("image_obj") is not None:
                            st.image(image_info["image_obj"], width=400)
                        else:
                            st.write("Image not available")

    
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

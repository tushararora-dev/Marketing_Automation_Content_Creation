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
        ["About Me", "Marketing Automation Agent", "Content Generation Agent"]
    )
    
    if selected_agent == "Marketing Automation Agent":
        marketing_automation_interface()
    elif selected_agent == "Content Generation Agent":
        st.sidebar.title("⚙️ Features Prototype")
        st.sidebar.write("✅ Prompt-to-Content Generation")
        st.sidebar.write("✅ Ad & Social Content Creation")
        st.sidebar.write("✅ Creative Asset Generation")
        st.sidebar.write("✅ UGC/Video Content Scripting & Editing")
        st.sidebar.write("❌ Rich Media / Interactive Content")
        st.sidebar.write("❌ Edit, Iterate, Personalize")
        st.sidebar.write("❌ Integration & Deployment")
        st.sidebar.write("❌ Modularity & Reusability")
        content_generation_interface()
    else:
        st.sidebar.markdown(
            """
            <div style='text-align: justify;'>
            🚀 Project Overview

            This project showcases a combined solution for **Marketing Automation** and **AI-Powered Content Creation**.

            - The **Marketing Automation** module enables users to automate multi-channel campaigns, audience segmentation, lead scoring, and performance tracking — leveraging AI and integrations with platforms like Klaviyo for seamless execution.
            
            - The **Content Creation** module empowers users to generate high-quality marketing assets including ad copy, email templates, social media captions, UGC video scripts, and more — all powered by advanced AI and retrieval-augmented generation techniques.

            Together, these modules demonstrate how AI can streamline marketing workflows, personalize customer engagement, and accelerate content production at scale.
            </div>
            """,
            unsafe_allow_html=True,
        )
        about_me()



def about_me():

    col1, col2 = st.columns(2)

    with col1:
        st.header("📈 Marketing Automation")
        st.write("""
        🚀 Marketing Automation allows businesses to streamline, automate, and measure marketing tasks and workflows to increase operational efficiency and grow revenue faster.

        🔑 **Key capabilities include:**

        - 📧 **Multi-channel Campaigns:** Automate email, SMS, push notifications, and social messaging to reach customers wherever they are.
        - 🎯 **Personalized Content Delivery:** Use AI to dynamically create tailored messages based on customer behavior, preferences, and lifecycle stage.
        - 🔥 **Lead Scoring & Segmentation:** Automatically segment your audience and prioritize leads based on engagement data and predictive models.
        - ⏰ **Automated Follow-ups:** Set up triggered sequences like drip campaigns that nurture leads or re-engage inactive customers.
        - 📊 **Performance Tracking & Reporting:** Measure campaign effectiveness with analytics dashboards and use insights to optimize future campaigns.
        - 🔗 **Integration with Platforms:** Connect with services like Klaviyo, Mailchimp, Twilio, and CRMs to leverage their powerful APIs for contact management, campaign execution, and data synchronization.
        - 🤖 **AI-powered Content Generation:** Combine with AI tools to generate campaign copy, subject lines, and messaging variants on the fly, increasing creativity and efficiency.

        🎯 With marketing automation, businesses can deliver the right message to the right person at the right time — all at scale.
        """)

    with col2:
        st.header("🎨 Content Creation")
        st.write("""
        AI-Powered Content Creation Possibilities:

        **✍️ Text Content**
        - 📝 Ad Copy (headlines, taglines, body text for ads)
        - 📧 Email Assets (headers, footers, CTA buttons, subject lines, email body)
        - 📱 Social Media Captions (with hashtags, tone/style matching brand)
        - 📰 Blog Posts & Articles (long-form or short-form)
        - 🛍️ Product Descriptions (e-commerce descriptions, features, benefits)
        - 🎬 Video Scripts (UGC scripts, explainer videos, tutorials)
        - 🏆 Landing Page Copy (headlines, benefits, testimonials)
        - 🔍 SEO Content (keywords, meta descriptions, FAQs)
        - 📢 Press Releases (announcements, new launches)
        - 🤖 Chatbot Dialogues (customer service scripts, FAQs)
        - 📖 Storytelling Content (brand stories, customer success stories)

        **🖼️ Image & Visual Content**
        - 🖼️ Static Images (product images, marketing banners, social posts)
        - 🎨 AI-Generated Illustrations (custom artwork, brand mascots)
        - 📊 Infographics (visual data representation)
        - 😂 Memes (for social engagement)
        - 🛡️ Logo Concepts (initial design ideas)
        - 🎭 Image Variations (style transfer, color modifications)
        - 📦 Product Mockups (placing product images on real-world backgrounds)

        **🎥 Video & Multimedia**
        - 🤖 AI Video Generation (from scripts, text-to-video tools)
        - 📽️ Animated Explainers (short clips explaining product/features)
        - 🎥 UGC Video Scripts (user-generated content style videos)
        - 🎙️ Voiceover/Narration (AI-generated voices matching scripts)
        - 📝 Subtitles/Closed Captions (auto-generated captions for videos)
        - 🖼️ Video Thumbnails (eye-catching images for video previews)
        - 📲 Social Stories (Instagram/Facebook story content)

        **🎧 Audio Content**
        - 🎙️ Podcasts Scripts (episode outlines, talking points)
        - 📚 Audiobook Narration (text-to-speech for books or articles)
        - 🎵 Jingles and Audio Ads (short catchy music clips)
        - 🗣️ Voice Cloning (personalized voice assistants or narrators)

        **🧩 Interactive Content**
        - ❓ Quizzes & Polls (engaging user interaction)
        - 🤖 Chatbots & Virtual Assistants (AI-driven customer support)
        - 🎯 Personalized Recommendations (product or content suggestions)

        **📊 Data & Research**
        - 📈 Market Research Summaries (trends, competitor analysis)
        - 🕵️ Customer Insights (sentiment analysis, feedback summaries)
        - 📉 Content Performance Reports (analytics and suggestions)
        """)

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
                        print(result)
                        st.session_state.content_result = result
                        st.success("Content generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Error generating content: {str(e)}")
            else:
                st.warning("Please fill in all required fields and select at least one content type")
    
    with col2:
        st.subheader("Content Templates")
        st.markdown("##### 🎯 Ad Copy Templates", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: justify;'>
            Provide complete ad creative deliverables including headline, primary text, call-to-action, description, 
            character counts, platform-specific adaptations, and the full response.
        </div><br>
            
        """, unsafe_allow_html=True)
        st.markdown("##### 📱 Social Media Templates", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: justify;'>
            Provide complete captions with relevant hashtags for Instagram, LinkedIn, TikTok, and other platforms.
        </div><br>
        """, unsafe_allow_html=True)
        st.markdown("##### 🖼️ Static and Product Visual", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: justify;'>
            Generate the following image types: ad_creative (advertising creative), product_showcase (product showcase image), social_post (social media post image), and hero_image (main campaign hero image).
        </div><br>
        """, unsafe_allow_html=True)
        st.markdown("##### 🎥 UGC Video Script", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: justify;'>
            Generate ugc video script with title, duration, timeline, dialoge, Visual Directions, Props/Setup Requirements etc. for tiktok, insta, youtube and facebook.
        </div><br>
        """, unsafe_allow_html=True)

        st.markdown("##### 📧 Email Assets", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: justify;'>
            Generate email header, hero section, footer, and CTA buttons as email assets.
        </div>
        """, unsafe_allow_html=True)



    
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
                st.write(sms.get('extract_sms', ''))
    
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
                st.write("**Description:**", copy.get('description', ''))
                # st.write("**Description:**", copy.get('character_counts', ''))
                # st.write("**Description:**", copy.get('platform_adaptations', ''))
                # st.write("**Description:**", copy.get('full_response', ''))
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
            if image_info.get("image_obj") is not None:
                st.image(image_info["image_obj"], width=400)
            else:
                st.write("Image not available")
    
    # UGC scripts
    if 'ugc_scripts' in result:
        st.subheader("🎬 UGC Video Scripts")
        for i, script in enumerate(result['ugc_scripts'], 1):
            with st.expander(f"Script {i}: {script.get('title', '')}"):
                st.write("**Duration:**", script.get('duration', ''))
                st.write("**Script:**")
                st.write(script.get('script', ''))

    # email assets
    if 'email_assets' in result:
        st.subheader("📧 Email Assets")
        for image_info in result['email_assets']:
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

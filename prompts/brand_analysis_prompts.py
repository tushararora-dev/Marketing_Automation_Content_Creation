from typing import Dict, Any, List

def get_campaign_planning_prompt(
    brand_analysis: Dict[str, Any],
    campaign_type: str,
    custom_prompt: str,
    num_emails: int,
    num_sms: int,
    target_audience: str,
    tone: str
) -> str:
    """
    Generate comprehensive prompt for campaign planning
    
    Args:
        brand_analysis: Analysis of the brand from website
        campaign_type: Type of campaign to plan
        custom_prompt: Custom instructions from user
        num_emails: Number of emails to plan
        num_sms: Number of SMS messages to plan
        target_audience: Target audience description
        tone: Campaign tone
    
    Returns:
        Detailed prompt for campaign planning
    """
    
    brand_name = brand_analysis.get("brand_name", "Brand")
    brand_description = brand_analysis.get("description", "")
    products = brand_analysis.get("products", [])
    value_propositions = brand_analysis.get("value_propositions", [])
    keywords = brand_analysis.get("keywords", [])
    brand_tone_analysis = brand_analysis.get("tone", "Professional")
    
    prompt = f"""
    Create a comprehensive marketing campaign plan for {brand_name}.
    
    BRAND ANALYSIS:
    - Brand Name: {brand_name}
    - Description: {brand_description}
    - Products/Services: {', '.join(products[:5])}
    - Value Propositions: {', '.join(value_propositions[:3])}
    - Key Keywords: {', '.join(keywords[:10])}
    - Brand Tone: {brand_tone_analysis}
    
    CAMPAIGN REQUIREMENTS:
    - Campaign Type: {campaign_type}
    - Target Audience: {target_audience}
    - Desired Tone: {tone}
    - Email Sequence: {num_emails} emails
    - SMS Sequence: {num_sms} SMS messages
    - Custom Instructions: {custom_prompt if custom_prompt else "Follow best practices"}
    
    CAMPAIGN PLANNING OBJECTIVES:
    1. Create a strategic campaign that aligns with brand values
    2. Design a customer journey that maximizes engagement
    3. Develop messaging that resonates with the target audience
    4. Plan timing and sequencing for optimal results
    5. Include personalization and segmentation strategies
    
    CAMPAIGN STRATEGY FRAMEWORK:
    
    1. CAMPAIGN OBJECTIVE:
    - Define the primary goal (awareness, conversion, retention, etc.)
    - Establish success metrics and KPIs
    - Align with overall business objectives
    
    2. AUDIENCE STRATEGY:
    - Profile the target audience in detail
    - Identify pain points and motivations
    - Determine preferred communication channels
    - Plan segmentation approach
    
    3. MESSAGING STRATEGY:
    - Core value proposition for this campaign
    - Key messages for each stage of the journey
    - Tone and voice guidelines
    - Personalization elements
    
    4. CHANNEL STRATEGY:
    - Email marketing approach and cadence
    - SMS marketing integration and timing
    - Cross-channel coordination
    - Platform-specific optimizations
    
    5. CONTENT STRATEGY:
    - Content themes and pillars
    - Visual and creative direction
    - Asset requirements
    - Brand consistency guidelines
    
    6. TIMING AND SEQUENCING:
    - Campaign launch strategy
    - Message timing and frequency
    - Trigger conditions for each message
    - Optimal send times and days
    
    CAMPAIGN TYPE SPECIFIC GUIDANCE:
    {get_campaign_type_guidance(campaign_type)}
    
    DELIVERABLES REQUIRED:
    1. Campaign Overview and Objectives
    2. Target Audience Profile and Segmentation
    3. Messaging Strategy and Key Themes
    4. Email Sequence Plan (subjects, purposes, timing)
    5. SMS Sequence Plan (purposes, timing)
    6. Trigger Conditions and Automation Rules
    7. Personalization and Dynamic Content Strategy
    8. Success Metrics and Optimization Plan
    
    Create a strategic, actionable campaign plan that leverages {brand_name}'s strengths to achieve maximum impact with {target_audience}.
    """
    
    return prompt




def get_brand_analysis_prompt(
    website_content: str,
    url: str
) -> str:
    """
    Generate prompt for comprehensive brand analysis from website content
    
    Args:
        website_content: Extracted website text content
        url: Brand website URL
    
    Returns:
        Prompt for brand analysis
    """
    
    prompt = f"""
    Analyze the following website content to extract comprehensive brand information for marketing campaign development.
    
    WEBSITE URL: {url}
    
    WEBSITE CONTENT:
    {website_content[:3000]}...
    
    ANALYSIS REQUIREMENTS:
    
    1. BRAND IDENTITY:
    - Extract the brand name and key identifiers
    - Determine brand positioning and unique value proposition
    - Identify brand personality and tone of voice
    - Assess brand maturity and market position
    
    2. PRODUCT/SERVICE ANALYSIS:
    - List main products or services offered
    - Identify product categories and features
    - Determine pricing strategy (if mentioned)
    - Assess product differentiation factors
    
    3. TARGET AUDIENCE ANALYSIS:
    - Identify primary target demographics
    - Determine customer segments and personas
    - Assess customer needs and pain points
    - Identify customer journey touchpoints
    
    4. COMPETITIVE LANDSCAPE:
    - Identify mentioned competitors or alternatives
    - Assess competitive advantages
    - Determine market differentiation strategy
    - Identify positioning gaps and opportunities
    
    5. MESSAGING AND COMMUNICATION:
    - Extract key brand messages and themes
    - Identify content pillars and topics
    - Assess communication style and tone
    - Determine brand voice characteristics
    
    6. MARKETING INTELLIGENCE:
    - Identify current marketing channels and tactics
    - Assess content marketing approach
    - Determine lead generation strategies
    - Identify conversion optimization elements
    
    7. BUSINESS MODEL INSIGHTS:
    - Understand revenue streams and offerings
    - Identify sales process and customer acquisition
    - Assess business maturity and scale
    - Determine growth opportunities
    
    OUTPUT FORMAT:
    Provide detailed insights for each category above, focusing on actionable information that can inform marketing campaign development. Include specific quotes or examples from the website content where relevant.
    
    Focus on extracting information that will help create targeted, effective marketing campaigns that align with the brand's established identity and messaging.
    """
    
    return prompt

def get_campaign_type_guidance(campaign_type: str) -> str:
    """Get specific guidance for different campaign types"""
    
    guidance_map = {
        "Cart Abandonment": """
        CART ABANDONMENT CAMPAIGN STRATEGY:
        - Primary Goal: Recover abandoned purchases and increase conversion rates
        - Key Triggers: Items added to cart but not purchased within 1-4 hours
        - Messaging Focus: Convenience, urgency, and value reinforcement
        - Sequence Strategy: Gentle reminder → Value reinforcement → Urgency creation → Social proof → Final incentive
        - Personalization: Product-specific messaging, cart value consideration
        - Timing: 1 hour, 24 hours, 3 days, 1 week intervals
        - Success Metrics: Recovery rate, revenue per email, conversion rate
        """,
        
        "Welcome Series": """
        WELCOME SERIES CAMPAIGN STRATEGY:
        - Primary Goal: Onboard new subscribers and build brand relationship
        - Key Triggers: Email signup, account creation, first purchase
        - Messaging Focus: Brand introduction, value delivery, expectation setting
        - Sequence Strategy: Welcome → Value delivery → Product education → Community building → First offer
        - Personalization: Signup source, interests, demographic data
        - Timing: Immediate, 1 day, 3 days, 1 week, 2 weeks
        - Success Metrics: Engagement rate, time to first purchase, lifetime value
        """,
        
        "Post-Purchase": """
        POST-PURCHASE CAMPAIGN STRATEGY:
        - Primary Goal: Maximize customer satisfaction and drive repeat purchases
        - Key Triggers: Completed purchase, product delivery, usage milestones
        - Messaging Focus: Gratitude, usage optimization, community building
        - Sequence Strategy: Thank you → Usage tips → Review request → Cross-sell → Reorder
        - Personalization: Product-specific content, purchase history, usage patterns
        - Timing: 1 hour, 1 day, 1 week, 3 weeks, 1 month
        - Success Metrics: Customer satisfaction, repeat purchase rate, review generation
        """,
        
        "Win-Back": """
        WIN-BACK CAMPAIGN STRATEGY:
        - Primary Goal: Re-engage inactive customers and drive repeat purchases
        - Key Triggers: 30+ days inactive, declined engagement, no recent purchases
        - Messaging Focus: Acknowledgment, value reminder, special incentives
        - Sequence Strategy: We miss you → Special offer → New products → VIP treatment → Final goodbye
        - Personalization: Past purchase behavior, preferences, inactivity duration
        - Timing: 30 days inactive, +3 days, +1 week, +2 weeks, +1 month
        - Success Metrics: Reactivation rate, revenue recovery, engagement restoration
        """,
        
        "Product Launch": """
        PRODUCT LAUNCH CAMPAIGN STRATEGY:
        - Primary Goal: Generate awareness and drive initial adoption
        - Key Triggers: Product announcement, pre-launch signup, launch date
        - Messaging Focus: Innovation, exclusivity, early adopter benefits
        - Sequence Strategy: Teaser → Announcement → Features → Social proof → Availability
        - Personalization: Interest level, customer segment, purchase history
        - Timing: -2 weeks, -1 week, launch day, +3 days, +1 week
        - Success Metrics: Awareness metrics, pre-orders, launch day sales
        """,
        
        "Seasonal Campaign": """
        SEASONAL CAMPAIGN STRATEGY:
        - Primary Goal: Capitalize on seasonal buying behavior and trends
        - Key Triggers: Seasonal dates, weather changes, holiday calendar
        - Messaging Focus: Seasonal relevance, limited-time nature, gift-giving
        - Sequence Strategy: Early announcement → Preparation → Peak season → Last chance
        - Personalization: Geographic location, past seasonal behavior, preferences
        - Timing: Varies by season and holidays
        - Success Metrics: Seasonal revenue lift, campaign ROI, market share
        """
    }
    
    return guidance_map.get(campaign_type, """
    CUSTOM CAMPAIGN STRATEGY:
    - Define clear objectives and success metrics
    - Identify target audience and their journey stage
    - Create compelling messaging aligned with brand voice
    - Plan logical sequence with appropriate timing
    - Include personalization and segmentation elements
    - Design for multi-channel optimization
    """)

def get_audience_segmentation_prompt(
    brand_analysis: Dict[str, Any],
    campaign_type: str
) -> str:
    """Generate prompt for audience segmentation strategy"""
    
    brand_name = brand_analysis.get("brand_name", "Brand")
    target_audience = brand_analysis.get("target_audience", "General audience")
    products = brand_analysis.get("products", [])
    
    prompt = f"""
    Develop a comprehensive audience segmentation strategy for {brand_name}'s {campaign_type.lower()} campaign.
    
    BRAND CONTEXT:
    - Brand: {brand_name}
    - Primary Audience: {target_audience}
    - Products/Services: {', '.join(products[:3])}
    - Campaign Type: {campaign_type}
    
    SEGMENTATION FRAMEWORK:
    
    1. DEMOGRAPHIC SEGMENTATION:
    - Age groups and generational cohorts
    - Geographic locations and markets
    - Income levels and purchasing power
    - Education and professional status
    
    2. BEHAVIORAL SEGMENTATION:
    - Purchase history and frequency
    - Engagement levels and preferences
    - Website behavior and interactions
    - Email and communication preferences
    
    3. PSYCHOGRAPHIC SEGMENTATION:
    - Values and lifestyle preferences
    - Interests and hobbies
    - Pain points and motivations
    - Brand affinity and loyalty levels
    
    4. CUSTOMER JOURNEY SEGMENTATION:
    - Awareness stage prospects
    - Consideration stage evaluators
    - Decision stage buyers
    - Post-purchase customers
    - Loyalty and advocacy segments
    
    CAMPAIGN-SPECIFIC SEGMENTS:
    {get_campaign_specific_segments(campaign_type)}
    
    PERSONALIZATION STRATEGY:
    For each segment, define:
    - Unique messaging approaches
    - Content preferences and formats
    - Optimal communication channels
    - Timing and frequency preferences
    - Personalization data points to use
    
    OUTPUT REQUIREMENTS:
    1. Define 3-5 primary audience segments
    2. Create detailed persona profiles for each segment
    3. Specify targeting criteria for each segment
    4. Recommend personalization strategies
    5. Suggest A/B testing opportunities
    6. Provide performance tracking metrics
    
    Create actionable segment definitions that enable precise targeting and personalized experiences.
    """
    
    return prompt

def get_campaign_specific_segments(campaign_type: str) -> str:
    """Get campaign-specific audience segments"""
    
    segments = {
        "Cart Abandonment": """
        CART ABANDONMENT SEGMENTS:
        - High-value cart abandoners ($100+)
        - First-time visitor abandoners
        - Repeat customer abandoners
        - Mobile vs. desktop abandoners
        - Product category specific abandoners
        - Time-based segments (recent vs. older abandonment)
        """,
        
        "Welcome Series": """
        WELCOME SERIES SEGMENTS:
        - New email subscribers
        - First-time purchasers
        - Account creators (no purchase)
        - Newsletter-only subscribers
        - Social media converts
        - Referral traffic converts
        """,
        
        "Post-Purchase": """
        POST-PURCHASE SEGMENTS:
        - First-time buyers
        - Repeat customers
        - High-value customers
        - Product category buyers
        - Gift purchasers
        - Subscription customers
        """,
        
        "Win-Back": """
        WIN-BACK SEGMENTS:
        - Recently inactive (30-60 days)
        - Long-term inactive (60+ days)
        - High-value inactive customers
        - Single-purchase customers
        - Engagement-only inactive
        - Seasonal customers
        """
    }
    
    return segments.get(campaign_type, "Define segments based on campaign objectives and customer behavior patterns.")

def get_competitive_analysis_prompt(
    brand_analysis: Dict[str, Any],
    industry_context: str = ""
) -> str:
    """Generate prompt for competitive analysis"""
    
    brand_name = brand_analysis.get("brand_name", "Brand")
    products = brand_analysis.get("products", [])
    competitors = brand_analysis.get("competitors", [])
    
    prompt = f"""
    Conduct a competitive analysis for {brand_name} to inform marketing campaign development.
    
    BRAND CONTEXT:
    - Brand: {brand_name}
    - Products/Services: {', '.join(products[:5])}
    - Known Competitors: {', '.join(competitors[:3]) if competitors else "To be identified"}
    - Industry Context: {industry_context}
    
    COMPETITIVE ANALYSIS FRAMEWORK:
    
    1. COMPETITOR IDENTIFICATION:
    - Direct competitors (same products/services)
    - Indirect competitors (alternative solutions)
    - Aspirational competitors (market leaders)
    - Emerging competitors (new market entrants)
    
    2. MESSAGING ANALYSIS:
    - Core value propositions used
    - Key marketing messages and themes
    - Brand positioning strategies
    - Unique selling propositions (USPs)
    
    3. MARKETING TACTICS ANALYSIS:
    - Email marketing approaches and frequency
    - Social media strategies and content types
    - Advertising channels and creative approaches
    - Content marketing themes and formats
    
    4. CUSTOMER EXPERIENCE ANALYSIS:
    - User journey and touchpoint optimization
    - Personalization and segmentation strategies
    - Customer service and support approaches
    - Loyalty and retention programs
    
    5. DIFFERENTIATION OPPORTUNITIES:
    - Messaging gaps in the market
    - Underserved customer segments
    - Unique positioning opportunities
    - Innovation areas for competitive advantage
    
    CAMPAIGN IMPLICATIONS:
    Based on the competitive analysis, provide recommendations for:
    - Unique messaging angles to pursue
    - Differentiation strategies to emphasize
    - Competitive advantages to highlight
    - Market gaps to exploit
    - Positioning strategies to adopt
    
    OUTPUT REQUIREMENTS:
    1. Competitive landscape overview
    2. Key competitor profiles and strategies
    3. Market positioning map
    4. Differentiation opportunities
    5. Campaign messaging recommendations
    6. Competitive monitoring suggestions
    
    Focus on actionable insights that can directly inform campaign strategy and messaging development.
    """
    
    return prompt

def get_content_strategy_prompt(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any]
) -> str:
    """Generate prompt for content strategy development"""
    
    brand_name = brand_analysis.get("brand_name", "Brand")
    content_themes = brand_analysis.get("content_themes", [])
    campaign_type = campaign_plan.get("campaign_type", "Marketing")
    target_audience = campaign_plan.get("target_audience", "General audience")
    
    prompt = f"""
    Develop a comprehensive content strategy for {brand_name}'s {campaign_type.lower()} campaign.
    
    BRAND AND CAMPAIGN CONTEXT:
    - Brand: {brand_name}
    - Campaign Type: {campaign_type}
    - Target Audience: {target_audience}
    - Content Themes: {', '.join(content_themes[:5])}
    - Campaign Objective: {campaign_plan.get("objective", "Drive engagement and conversions")}
    
    CONTENT STRATEGY FRAMEWORK:
    
    1. CONTENT PILLARS:
    Define 3-5 core content pillars that will guide all campaign content:
    - Educational content (how-to, tips, insights)
    - Product-focused content (features, benefits, use cases)
    - Brand story content (values, mission, behind-the-scenes)
    - Customer-centric content (testimonials, success stories)
    - Industry/trend content (news, analysis, thought leadership)
    
    2. CONTENT FORMATS AND TYPES:
    For each channel, specify optimal content formats:
    - Email: Templates, layouts, visual elements
    - SMS: Message types, personalization elements
    - Social Media: Post types, visual content, video content
    - Website: Landing pages, blog content, resources
    
    3. VISUAL CONTENT STRATEGY:
    - Brand visual identity and guidelines
    - Image and graphic requirements
    - Video content opportunities
    - Infographic and data visualization needs
    - User-generated content integration
    
    4. CONTENT CALENDAR AND SEQUENCING:
    - Content release timing and sequencing
    - Seasonal and timely content opportunities
    - Evergreen vs. timely content balance
    - Cross-channel content coordination
    
    5. PERSONALIZATION AND DYNAMIC CONTENT:
    - Audience-specific content variations
    - Dynamic content blocks and elements
    - Behavioral trigger content
    - Personalization data utilization
    
    6. CONTENT OPTIMIZATION AND TESTING:
    - A/B testing strategies for content elements
    - Performance metrics and success indicators
    - Content iteration and improvement processes
    - User feedback integration methods
    
    CONTENT REQUIREMENTS BY CAMPAIGN TYPE:
    {get_content_requirements_by_type(campaign_type)}
    
    OUTPUT DELIVERABLES:
    1. Content pillar definitions and guidelines
    2. Content format specifications by channel
    3. Visual content strategy and requirements
    4. Content calendar framework
    5. Personalization and dynamic content plan
    6. Content testing and optimization strategy
    
    Create a strategic content framework that ensures consistency, relevance, and effectiveness across all campaign touchpoints.
    """
    
    return prompt

def get_content_requirements_by_type(campaign_type: str) -> str:
    """Get content requirements specific to campaign types"""
    
    requirements = {
        "Cart Abandonment": """
        CART ABANDONMENT CONTENT REQUIREMENTS:
        - Product-focused visuals showing abandoned items
        - Urgency-creating copy and design elements
        - Social proof content (reviews, ratings, testimonials)
        - Incentive-based content (discounts, free shipping)
        - Trust-building elements (security badges, guarantees)
        - Clear product information and specifications
        """,
        
        "Welcome Series": """
        WELCOME SERIES CONTENT REQUIREMENTS:
        - Brand introduction and story content
        - Educational content about products/services
        - Value demonstration through tips and insights
        - Community and culture content
        - Product showcase and feature highlights
        - Customer success stories and use cases
        """,
        
        "Post-Purchase": """
        POST-PURCHASE CONTENT REQUIREMENTS:
        - Thank you and appreciation messaging
        - Product usage guides and tutorials
        - Care and maintenance instructions
        - Complementary product suggestions
        - Review and feedback request content
        - Community and user-generated content features
        """,
        
        "Win-Back": """
        WIN-BACK CONTENT REQUIREMENTS:
        - Nostalgic and relationship-focused content
        - New product and feature announcements
        - Exclusive offers and VIP treatment content
        - Success stories from returning customers
        - Brand evolution and improvement messaging
        - Personalized recommendations based on past behavior
        """
    }
    
    return requirements.get(campaign_type, "Develop content that aligns with campaign objectives and audience needs.")

def get_performance_optimization_prompt(
    campaign_type: str,
    success_metrics: List[str]
) -> str:
    """Generate prompt for campaign performance optimization"""
    
    prompt = f"""
    Develop a comprehensive performance optimization strategy for the {campaign_type.lower()} campaign.
    
    CAMPAIGN CONTEXT:
    - Campaign Type: {campaign_type}
    - Success Metrics: {', '.join(success_metrics)}
    
    OPTIMIZATION FRAMEWORK:
    
    1. KEY PERFORMANCE INDICATORS (KPIs):
    Define primary and secondary metrics:
    - Primary KPIs: Core business impact metrics
    - Secondary KPIs: Supporting engagement and behavior metrics
    - Leading Indicators: Early performance signals
    - Lagging Indicators: Final outcome measurements
    
    2. TESTING AND EXPERIMENTATION:
    - A/B testing priorities and methodologies
    - Multivariate testing opportunities
    - Subject line and headline testing
    - Content format and layout testing
    - Timing and frequency optimization tests
    
    3. AUDIENCE OPTIMIZATION:
    - Segmentation performance analysis
    - Personalization effectiveness testing
    - Audience expansion and refinement
    - Behavioral trigger optimization
    
    4. CONTENT OPTIMIZATION:
    - Message resonance testing
    - Creative element performance analysis
    - Call-to-action optimization
    - Visual content effectiveness
    
    5. CHANNEL OPTIMIZATION:
    - Email deliverability improvement
    - SMS delivery and engagement optimization
    - Cross-channel performance analysis
    - Channel attribution and contribution
    
    6. AUTOMATION AND WORKFLOW OPTIMIZATION:
    - Trigger timing optimization
    - Flow logic and decision point improvement
    - Exit and re-entry condition refinement
    - Cross-campaign interaction optimization
    
    OPTIMIZATION PRIORITIES:
    {get_optimization_priorities(campaign_type)}
    
    MEASUREMENT AND REPORTING:
    - Performance dashboard requirements
    - Reporting frequency and stakeholders
    - Success criteria and benchmarks
    - Optimization decision frameworks
    
    OUTPUT REQUIREMENTS:
    1. KPI hierarchy and measurement plan
    2. Testing roadmap and prioritization
    3. Optimization tactics by campaign element
    4. Performance monitoring and alerting setup
    5. Continuous improvement process definition
    6. Success criteria and benchmark establishment
    
    Create a systematic approach to campaign optimization that enables continuous improvement and maximum ROI.
    """
    
    return prompt

def get_optimization_priorities(campaign_type: str) -> str:
    """Get optimization priorities specific to campaign types"""
    
    priorities = {
        "Cart Abandonment": """
        CART ABANDONMENT OPTIMIZATION PRIORITIES:
        1. Email deliverability and inbox placement
        2. Subject line and preview text optimization
        3. Product recommendation accuracy
        4. Incentive timing and amount optimization
        5. Mobile experience and loading speed
        6. Cross-device cart recovery
        """,
        
        "Welcome Series": """
        WELCOME SERIES OPTIMIZATION PRIORITIES:
        1. Onboarding completion rates
        2. Time-to-first-purchase optimization
        3. Content engagement and progression
        4. Unsubscribe and opt-out minimization
        5. Cross-channel integration effectiveness
        6. Long-term customer value development
        """,
        
        "Post-Purchase": """
        POST-PURCHASE OPTIMIZATION PRIORITIES:
        1. Customer satisfaction and NPS improvement
        2. Repeat purchase rate optimization
        3. Review and referral generation
        4. Cross-sell and upsell effectiveness
        5. Support ticket reduction
        6. Customer lifetime value maximization
        """
    }
    
    return priorities.get(campaign_type, "Focus on metrics that directly impact campaign objectives and business outcomes.")

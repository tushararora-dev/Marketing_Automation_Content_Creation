```bash
# 📁 Project Structure
Marketing_auomation_content_creation/
│
├── app.py                           # Main entrypoint (e.g., Streamlit or CLI app)
├── config/                          # Configurations (API keys, constants)
│   ├── settings.py
│   └── env.example
│
├── agents/                          # Agent logic (LangGraph or CrewAI)
│   ├── __init__.py
│   ├── marketing_automation_agent.py
│   └── content_generation_agent.py
│
├── workflows/                       # Agent workflows / LangGraph nodes
│   ├── marketing_automation/        # Nodes specific to marketing flow
│   │   ├── planner.py
│   │   ├── email_generator.py
│   │   ├── sms_generator.py
│   │   ├── visual_generator.py
│   │   └── flow_builder.py
│   └── content_generation/          # Nodes for content generation
│       ├── ad_writer.py
│       ├── video_editor.py
│       ├── static_image_gen.py
│       ├── ugc_script_gen.py
│       └── asset_packager.py
│
├── tools/                           # Tools/utilities like LLMs, APIs, Translators
│   ├── llm_manager.py               # Handles HuggingFace/OpenAI/Groq LLMs
│   ├── image_gen.py                 # Image generation (e.g., stable diffusion)
│   ├── video_editor_api.py          # Interface with Opus Clip, Captions
│   ├── klaviyo_exporter.py          # Export campaign to Klaviyo format
│   └── browser_utils.py             # Brand scraping, info extraction
│
├── prompts/                         # All prompt templates
│   ├── __init__.py
│   ├── email_prompts.py
│   ├── ad_prompts.py
│   └── brand_analysis_prompts.py
│
├── export/                          # Exported flows (json, csv, zip)
│   └── sample_campaigns/
│       ├── demo_flow_1.json
│       ├── demo_emails.csv
│       └── demo_images.zip
│
├── memory/                          # Saved history (ChromaDB or simple JSON)
│   ├── brand_1_memory.json
│   └── brand_2_memory.json
│
├── tests/                           # Unit + integration tests
│   ├── test_agents.py
│   ├── test_email_gen.py
│   └── test_flow_builder.py
│
├── docker/                          # Docker + container setup
│   ├── Dockerfile
│   └── requirements.txt
├── docs/                            # Documentation
├── notebook/                        # notebook ipynb for testing
│
└── README.md                        # Project overview & instructions
└── create_structure.py              # Folder creation           
└── pyproject.toml       
└── .python-version 
└── requirements.txt                  
└── README.md                        
```
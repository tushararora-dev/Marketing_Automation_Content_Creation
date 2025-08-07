import os

project_structure = {
    "config": ["settings.py", "env.example"],
    "agents": ["__init__.py", "marketing_automation_agent.py", "content_generation_agent.py"],
    "workflows": {
        "marketing_automation": [
            "planner.py", "email_generator.py", "sms_generator.py",
            "visual_generator.py", "flow_builder.py"
        ],
        "content_generation": [
            "ad_writer.py", "video_editor.py", "static_image_gen.py",
            "ugc_script_gen.py", "asset_packager.py"
        ]
    },
    "tools": [
        "llm_manager.py", "image_gen.py", "video_editor_api.py",
        "klaviyo_exporter.py", "browser_utils.py"
    ],
    "prompts": ["__init__.py", "email_prompts.py", "ad_prompts.py", "brand_analysis_prompts.py"],
    "export/sample_campaigns": ["demo_flow_1.json", "demo_emails.csv", "demo_images.zip"],
    "memory": ["brand_1_memory.json", "brand_2_memory.json"],
    "tests": ["test_agents.py", "test_email_gen.py", "test_flow_builder.py"],
    "docker": ["Dockerfile", "requirements.txt"],
    ".": ["app.py", "README.md"]
}

def create_structure(base_path, structure):
    for folder, files in structure.items():
        if isinstance(files, list):
            folder_path = os.path.join(base_path, folder)
            if folder != ".":
                os.makedirs(folder_path, exist_ok=True)
                for file in files:
                    open(os.path.join(folder_path, file), "w").close()
            else:
                for file in files:
                    open(os.path.join(base_path, file), "w").close()
        elif isinstance(files, dict):
            for subfolder, subfiles in files.items():
                subfolder_path = os.path.join(base_path, folder, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)
                for file in subfiles:
                    open(os.path.join(subfolder_path, file), "w").close()

if __name__ == "__main__":
    create_structure(".", project_structure)
    print("✅ Project folder structure created in current directory.")

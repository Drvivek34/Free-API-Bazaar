#!/usr/bin/env python3
import os
import json
import re
from datetime import datetime

FREE_API_DIR = "/root/bazaars/Free-API-Bazaar"
PROVIDERS_JSON = "/root/awesome-free-llm-apis/free-llm-providers.json"

def kebab_case(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def classify_provider(p):
    quota = p.get("quota", "").lower()
    name = p.get("name", "").lower()
    models = [m.lower() for m in p.get("models", [])]
    category = p.get("category", "").lower()

    # Image generation
    if any("stable-diffusion" in m or "stable diffusion" in m or "flux" in m or "dall-e" in m or "midjourney" in m for m in models) or "image" in quota or "image generation" in quota:
        return "image-generation"
    
    # Audio / TTS / STT
    if category == "transcription" or any("whisper" in m or "tts" in m or "speech" in m or "audio" in m for m in models):
        return "audio-tts-stt"

    # Embeddings
    if "embedding" in name or "embedding" in quota or any("embedding" in m for m in models):
        return "embeddings"

    # Vision / Multimodal
    if any("vision" in m or "multimodal" in m or "gpt-4o" in m or "gemini-1.5" in m or "claude-3" in m for m in models) or "vision" in quota:
        return "vision-multimodal"

    # Gateways & Routers
    if "router" in name or "gateway" in name or "openrouter" in name or "llm-router" in name:
        return "gateways-routers"

    # OpenAI-Compatible
    if p.get("openai_compatible", False):
        return "openai-compatible"

    # Free Trials / Credits vs Free LLM Inference
    if "no permanent free tier" in quota or "credit" in quota or "trial" in quota or "free trial" in quota:
        return "free-trials-credits"

    if "free tier" in quota or "free token" in quota or "free request" in quota or "per day" in quota or "per month" in quota or "always free" in quota:
        return "free-llm-inference"

    return "misc"

def main():
    if not os.path.exists(PROVIDERS_JSON):
        print(f"Error: {PROVIDERS_JSON} not found!")
        return

    with open(PROVIDERS_JSON, "r") as f:
        data = json.load(f)

    providers = data.get("providers", [])
    print(f"Loaded {len(providers)} providers from {PROVIDERS_JSON}")

    today_str = datetime.today().strftime("%Y-%m-%d")
    count_added = 0

    # Categorize and write
    for p in providers:
        cat_slug = classify_provider(p)
        prov_slug = kebab_case(p["name"])
        
        target_dir = os.path.join(FREE_API_DIR, cat_slug, prov_slug)
        os.makedirs(target_dir, exist_ok=True)

        # Determine card requirement
        quota = p.get("quota", "")
        card_required = "No"
        if "credit card required" in quota.lower() or "card required" in quota.lower() or "requires card" in quota.lower():
            card_required = "Yes"
        elif "no credit card required" in quota.lower() or "no card" in quota.lower():
            card_required = "No"

        # Build models list markdown
        models_md = ""
        if p.get("models"):
            models_md = "\n".join(f"- {m}" for m in p["models"])
        else:
            models_md = "None specified / custom models"

        # Build OpenAI compatible section
        openai_compat = "Yes" if p.get("openai_compatible") else "No"
        base_url = p.get("base_url", "N/A")

        readme_content = f"""# {p['name']}

{p.get('quota', 'No description available.')}

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## Details

- **Signup / Docs URL**: [{p['url']}]({p['url']})
- **Free-tier Limits**: {p.get('quota', 'N/A')}
- **Credit Card Required**: {card_required}
- **OpenAI Compatible**: {openai_compat}
- **OpenAI Base URL**: `{base_url}`
- **Source**: Upstream Free LLM API List
- **Date Verified**: {today_str}

## Models Available

{models_md}
"""
        with open(os.path.join(target_dir, "README.md"), "w") as out_f:
            out_f.write(readme_content)
        count_added += 1

    print(f"Successfully imported {count_added} providers into Free-API-Bazaar.")

if __name__ == "__main__":
    main()

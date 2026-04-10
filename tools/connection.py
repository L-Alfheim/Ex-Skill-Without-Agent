import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 自动定位项目根目录的 .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def get_client():
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        raise ValueError(f"未能加载 API Key。请检查 {BASE_DIR}/.env 是否存在。")
    
    return OpenAI(
        api_key=api_key,
        base_url="https://api.siliconflow.cn/v1"
    )
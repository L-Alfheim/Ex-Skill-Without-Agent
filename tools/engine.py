from tools.connection import get_client, BASE_DIR

class ChatEngine:
    # 模型参数
    MODEL_NAME = "deepseek-ai/DeepSeek-V3.2"
    TEMPERATURE = 0.8
    TOP_P = 0.9
    FREQUENCY_PENALTY = 0.6
    STREAM = False

    def __init__(self, slug: str):
        self.client = get_client()
        self.slug = slug
        self.skill_path = BASE_DIR / "exes" / slug / "SKILL.md"
        self.skill_content = ""
        
        # 初始化
        self._load_skill()

    def _load_skill(self):
        """加载并校验镜像文件"""
        if not self.skill_path.exists():
            raise FileNotFoundError(f"缺少镜像文件，请检查路径: {self.skill_path}")
        
        with open(self.skill_path, 'r', encoding='utf-8') as f:
            self.skill_content = f.read()
        
        print(f"--- 已连接到 {self.slug} 的数字镜像 ---")

    def fetch_reply_and_usage(self, user_input: str, chat_history: list):
        """
        请求 API 获取回复
        :param user_input: 当前用户输入
        :param chat_history: 历史对话列表
        :return: (content, usage)
        """
        # 构造标准消息体
        messages = [{"role": "system", "content": self.skill_content}]
        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_input})

        # 调用模型 
        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=messages, # type: ignore
            temperature=self.TEMPERATURE,
            top_p=self.TOP_P,
            frequency_penalty=self.FREQUENCY_PENALTY,
            stream=self.STREAM
        ) # type: ignore
        
        return response.choices[0].message.content, response.usage
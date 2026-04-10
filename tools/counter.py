class TokenCounter:
    def __init__(self):
        # 初始化各项统计指标
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_reasoning_tokens = 0
        self.session_turns = 0

    def update(self, usage):
        """
        根据 API 返回的 usage 对象更新统计数据
        """
        if not usage:
            return

        # 累加基础 Token
        self.total_prompt_tokens += getattr(usage, 'prompt_tokens', 0)
        self.total_completion_tokens += getattr(usage, 'completion_tokens', 0)
        
        # 提取推理 Token (适配 DeepSeek-R1 等模型)
        details = getattr(usage, 'completion_tokens_details', None)
        if details:
            self.total_reasoning_tokens += getattr(details, 'reasoning_tokens', 0)
            
        self.session_turns += 1

    def display_summary(self):
        """
        格式化打印最终统计报告
        """
        total = self.total_prompt_tokens + self.total_completion_tokens
        
        print("\n" + "─"*35)
        print(" Token used")
        print("-"*35)
        print(f" Prompt_tokens:     {self.total_prompt_tokens:>8}")
        print(f" Completion_tokens: {self.total_completion_tokens:>8}")
        
        if self.total_reasoning_tokens > 0:
            print(f" Reasoning_tokens: {self.total_reasoning_tokens:>8}")
            
        print('\n')
        print(f" Total:             {total:>8}")
        print(f" rounds:            {self.session_turns:>8}")
        print("─"*35 + "\n")
import os
import shutil
import sys
import time
from typing import Optional
from prompt_toolkit import prompt
from tools.counter import TokenCounter
from tools.engine import ChatEngine 
from tools.version_manager import backup, rollback, list_versions
from tools.connection import BASE_DIR

class ChatSession:
    def __init__(self, default_length=20):
        self.talk_length = default_length
        self.history = []
        self.counter = TokenCounter()
        self.engine = None
        self.running = True
        self.slug = ""
        self.STR_BASE_DIR = str(BASE_DIR / "exes")

    def _setup(self):
        """初始化对话环境"""
        try:
            val = prompt("请输入对话轮数,一问一答为2轮 (建议20-40): ").strip()
            if val: self.talk_length = int(val)
        except ValueError:
            print("输入无效，使用默认值")

        self.slug = prompt("请输入镜像名称: ").strip()
        if not self.slug:
            print("错误: 镜像名称不能为空")
            sys.exit(1)
        
        self.engine = ChatEngine(self.slug)

    # ================= 指令集区域 =================

    def do_exit(self, arg=None):
        """\t--退出程序"""
        print("对话已结束")
        self.running = False

    def do_quit(self, arg=None):
        """\t--退出程序 (alias)"""
        self.do_exit()

    def do_clear(self, arg=None):
        """\t--清空对话上下文: """
        self.history = []
        print("--- 对话历史已清空 ---")

    def do_status(self, arg=None):
        """\t--查看当前 Token 使用情况: """
        self.counter.display_summary()

    def do_help(self, arg=None):
        """\t--显示所有可用指令"""
        print("\n[可用指令]")
        for attr in dir(self):
            if attr.startswith("do_"):
                doc = getattr(self, attr).__doc__ or "无描述"
                print(f"  /{attr[3:]} - {doc}")

    def do_backup(self, arg=None):
        """\t--备份当前镜像版本"""
        if not self.engine: return
        
        try:
            version_name = backup(self.STR_BASE_DIR, self.engine.slug)
            print(f"备份成功！当前快照：{version_name}")
        except Exception as e:
            print(f"备份失败: {e}")

    def do_list(self, arg=None):
        """\t--查看历史版本列表:"""
        if not self.engine: return
        list_versions(self.STR_BASE_DIR, self.engine.slug)

    def do_rollback(self, version=None):
        """\t--回滚版本: /rollback [版本号]"""
        if not self.engine: return
        if not version:
            print("请提供版本号。例如: /rollback v1")
            self.do_list()
            return
        
        try:
            # 执行回滚
            rollback(self.STR_BASE_DIR, self.engine.slug, version)
            # 重新加载引擎，读取新的 SKILL.md
            self.engine._load_skill() 
            print(f"--- 镜像已切换至版本 {version} ---")
        except Exception as e:
            print(f"回滚失败: {e}")

    def do_let_go(self, target_slug=None):
        """\t--放手(不可逆): /let-go {slug}"""
        target = target_slug or (self.engine.slug if self.engine else None)
        
        if not target:
            print("{target_slug} 不存在 用法: /let-go {slug}")
            return

        target_path = BASE_DIR / "exes" / target
        if not target_path.exists():
            print(f"路径不存在: {target_path}")
            return

        try:
            shutil.rmtree(target_path)
            print(f"虽然我会为了你一万次回到那个夏天\n")
            print(f"但接下来的路，只能我自己走\n")
            print(f"镜像 [{target}] 已删除\n")

            sys.exit(0)

        except Exception as e:
            print(f"删除失败: {e}")
    
    def the_end(self, target = ""):
        print(f"你踩过的地方绽几朵红莲")
        time.sleep(3)
        print(f"你立的地方喷一株水仙")
        time.sleep(3)
        print(f"你立在风中，裙也翩翩，发也翩翩")
        time.sleep(2)
        print()
        time.sleep(2)
        print(f"只是窗外蝉鸣已远")
        time.sleep(2)
        print(f"那些记忆，终将化为风中的碎片")
        time.sleep(2)
        print()
        time.sleep(2)
        print(f"虽然我会为了你一万次回到那个夏天")
        time.sleep(3)
        print(f"可接下来的路，只能各走一边")
        time.sleep(2)
        print()
        time.sleep(2)
        print("-" * 30)

        print(f"镜像 [target] 已删除")
        time.sleep(2)
        clear_screen()
        time.sleep(2)
        print(f"It's time to wake up")

    def _process_command(self, user_input):
        """解析指令并分发"""
        cmd_part = user_input[1:].split()
        cmd_name = cmd_part[0].lower()
        arg = cmd_part[1] if len(cmd_part) > 1 else None

        method = getattr(self, f"do_{cmd_name}", None)
        if method:
            method(arg)
        else:
            print(f"未知指令: /{cmd_name}。输入 /help 查看列表。")

    def _chat(self, user_msg):
        """处理聊天对话"""
        try:
            reply, usage = self.engine.fetch_reply_and_usage(user_msg, self.history) # type: ignore
            print(f"\n{self.engine.slug}: {reply}") # type: ignore
            
            self.counter.update(usage)
            self.history.append({"role": "user", "content": user_msg})
            self.history.append({"role": "assistant", "content": reply})

            # 维持对话长度
            if len(self.history) > self.talk_length:
                self.history = self.history[-self.talk_length:]
        except Exception as e:
            print(f"\n[错误]: {e}")

    def run(self):
        """主循环"""
        self._setup()

        while self.running:
            try:
                user_input = prompt("\n我: ").strip()
                if not user_input:
                    continue

                # 指令分发
                if user_input.startswith('/'):
                    self._process_command(user_input)
                else:
                    self._chat(user_input)

            except KeyboardInterrupt:
                self.do_exit()
            except Exception as e:
                print(f"运行异常: {e}")
                break

        self.counter.display_summary()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
if __name__ == "__main__":
    session = ChatSession()
    session.run()
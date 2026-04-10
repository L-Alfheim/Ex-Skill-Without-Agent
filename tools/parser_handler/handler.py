import json
import os

def process_messages(input_path, output_path):
    """
    只保留微信的文本消息作为提取记忆的材料
    """
    if not os.path.exists(input_path):
        print(f"错误：找不到文件 {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError:
            print("错误：JSON 格式非法，请检查括号是否闭合")
            return

    all_msgs = raw_data.get('messages', []) if isinstance(raw_data, dict) else raw_data
    
    cleaned_list = []

    for msg in all_msgs:
        if msg.get('type') == '文本消息':
            cleaned_msg = {
                "formattedTime": msg.get('formattedTime'),
                "senderDisplayName": msg.get('senderDisplayName'),
                "content": msg.get('content')
            }
            cleaned_list.append(cleaned_msg)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_list, f, ensure_ascii=False, indent=2)

    print(f"处理完成！")
    print(f"过滤掉非文本/冗余字段后，剩余：{len(cleaned_list)} 条记录")
    print(f"结果已存至：{output_path}")

if __name__ == "__main__":
    # 这里手动更改路径
    process_messages("原消息.json", "精简消息.json")
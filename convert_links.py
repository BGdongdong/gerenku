import re
import os
import hashlib
from datetime import datetime

def backup_file(file_path):
    """创建文件备份并返回备份路径"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    os.rename(file_path, backup_path)
    return backup_path

def convert_links_to_blank(file_path):
    """
    将Markdown文件中的所有外部链接转换为在新标签页打开
    保留内部锚点链接在当前页打开
    """
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配标准Markdown链接 [text](url)
    pattern = r'(\[[^\]]+\]\(([^\)]+)\))'
    matches = re.findall(pattern, content)
    
    # 计算文件哈希以确定是否修改
    original_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    modified_content = content
    
    for full_match, url in matches:
        # 跳过内部锚点链接
        if any(url.startswith(prefix) for prefix in ['#', './#', '/#']):
            continue
            
        # 判断是否是图片链接 ![alt](url)
        is_image = False
        # 向前查找是否有感叹号
        prev_char_idx = content.find(full_match) - 1
        if prev_char_idx >= 0 and content[prev_char_idx] == '!':
            is_image = True
        
        # 替换为HTML链接并添加target="_blank"
        if not is_image:  # 非图片链接才添加target
            text_part = full_match[1:-1].split(']', 1)[0]
            html_link = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text_part}</a>'
            modified_content = modified_content.replace(full_match, html_link)
    
    # 计算修改后哈希
    modified_hash = hashlib.md5(modified_content.encode('utf-8')).hexdigest()
    
    # 只有内容发生变化时才写入
    if original_hash != modified_hash:
        # 创建备份
        backup_path = backup_file(file_path)
        
        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
            
        return True, backup_path, modified_content
    
    return False, None, modified_content

def main():
    """主函数：处理GitHub仓库中的README.md"""
    # 检测当前目录是否是GitHub仓库
    if not os.path.exists('.git'):
        print("⚠️ 警告：当前目录不是GitHub仓库，建议在本地仓库副本中运行")
    
    # 查找仓库中的README文件
    readme_files = []
    for filename in ['README.md', 'README.MD', 'readme.md']:
        if os.path.exists(filename):
            readme_files.append(filename)
    
    if not readme_files:
        print("❌ 错误：未在当前目录中找到README.md文件")
        return
    
    print("✨ GitHub README链接转换工具")
    print("==================================")
    
    for file in readme_files:
        print(f"\n处理文件: {file}")
        changed, backup_path, _ = convert_links_to_blank(file)
        
        if changed:
            print(f"✅ 链接已转换成功！原文件备份为: {backup_path}")
            print("👉 建议使用命令查看文件变化: git diff")
        else:
            print("ℹ️ 文件无变化或已处理过，不需要转换")
    
    print("\n==================================")
    print("✅ 处理完成！")
    print("👉 接下来请使用以下命令完成操作:")
    print("   1. 检查文件: git diff")
    print("   2. 提交更改: git add README.md")
    print("   3. 推送到GitHub: git commit -m \"优化链接打开方式\" && git push")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        print("💡 请确保脚本在包含README.md的目录中运行")

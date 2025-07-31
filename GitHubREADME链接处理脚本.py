import re
import os

def convert_links_to_blank(file_path):
    """
    将Markdown文件中的所有外部链接转换为在新标签页打开
    保留内部锚点链接在当前页打开
    """
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        
        # 匹配标准Markdown链接 [text](url)
        markdown_links = re.findall(r'(\[[^\]]+\]\(([^\)]+)\))', content)
        
        for full_match, url in markdown_links:
            # 跳过内部锚点链接
            if url.startswith('#') or url.startswith('./#') or url.startswith('/#'):
                continue
                
            # 替换为HTML链接并添加target="_blank"
            html_link = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{full_match[1:-1].split("]")[0]}</a>'
            content = content.replace(full_match, html_link)
        
        # 移回文件开头并写入
        f.seek(0)
        f.write(content)
        f.truncate()

# 处理当前目录下的README.md文件
if __name__ == "__main__":
    readme_path = os.path.join(os.getcwd(), 'README.md')
    if os.path.exists(readme_path):
        convert_links_to_blank(readme_path)
        print("README.md链接已成功转换！")
    else:
        print("错误：当前目录下未找到README.md文件")

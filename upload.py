#!/usr/bin/env python
import os
from urllib import parse

HEADER="""# 📚 백준, 프로그래머스 문제 풀이 목록

"""

def get_language(file):
    """파일 확장자로 언어명을 반환합니다."""
    ext = os.path.splitext(file)[1].lower()
    mapping = {
        '.py': 'Python',
        '.kt': 'Kotlin',
        '.java': 'Java',
        '.cpp': 'C++',
        '.js': 'JavaScript',
        '.swift': 'Swift'
    }
    return mapping.get(ext, ext[1:].upper() if ext else "Unknown")

def main():
    content = HEADER
    directories = []
    solveds = []
    
    for root, dirs, files in os.walk("."):
        dirs.sort()
        if root == '.':
            for dir in ('.git', '.github'):
                try: dirs.remove(dir)
                except ValueError: pass
            continue
        
        category = os.path.basename(root)
        if category == 'images': continue
        
        directory = os.path.basename(os.path.dirname(root))
        if directory == '.': continue
            
        if directory not in directories:
            if directory in ["백준", "프로그래머스"]:
                content += f"## 📚 {directory}\n"
            else:
                content += f"### 🚀 {directory}\n"
                # 표 헤더에 '언어' 추가
                content += "| 문제번호 | 언어 | 링크 |\n| :--- | :---: | :--- |\n"
            directories.append(directory)
            
        for file in files:
            if category not in solveds:
                link = parse.quote(os.path.join(root, file))
                lang = get_language(file)
                # 데이터 행에 언어 정보 추가
                content += f"|{category}|{lang}|[링크]({link})|\n"
                solveds.append(category)
        
    with open("README.md", "w", encoding="utf-8") as fd:
        fd.write(content)

if __name__ == "__main__":
    main()

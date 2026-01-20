import os
from urllib import parse

HEADER = """# 📚 알고리즘 문제 풀이 목록
# 백준, 프로그래머스, SWEA 문제 풀이 목록
"""

def get_language(file_path):
    """파일 확장자로 언어 추출"""
    ext = os.path.splitext(file_path)[1].lower()
    language_map = {
        '.py': 'Python',
        '.kt': 'Kotlin',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.js': 'JavaScript',
        '.swift': 'Swift',
    }
    return language_map.get(ext, ext[1:].upper() if ext else '-')

def main():
    content = ""
    content += HEADER
    
    directories = []
    solveds = []
    
    for root, dirs, files in os.walk("."):
        dirs.sort()
        if root == '.':
            for dir in ('.git', '.github'):
                try:
                    dirs.remove(dir)
                except ValueError:
                    pass
            continue
        
        category = os.path.basename(root)
        
        if category == 'images':
            continue
            
        directory = os.path.basename(os.path.dirname(root))
        
        if directory == '.':
            continue
            
        if directory not in directories:
            if directory in ["백준", "프로그래머스", "SWEA"]:
                content += "## 📚 {}\n".format(directory)
            else:
                content += "### 🚀 {}\n".format(directory)
                content += "| 문제번호 | 언어 | 링크 |\n"
                content += "| ----- | ----- | ----- |\n"
            directories.append(directory)
            
        for file in files:
            if category not in solveds:
                language = get_language(file)
                content += "|{}|{}|[링크]({})|\n".format(
                    category, 
                    language,
                    parse.quote(os.path.join(root, file))
                )
                solveds.append(category)
                
    with open("README.md", "w") as fd:
        fd.write(content)

if __name__ == "__main__":
    main()

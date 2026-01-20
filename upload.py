import os
from urllib import parse

HEADER = """# 📚 코딩테스트 문제 풀이 목록

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

def is_code_file(file_name):
    """코드 파일인지 확인 (README.md 등 제외)"""
    file_lower = file_name.lower()
    
    # 제외할 파일들
    if file_lower in ['readme.md', '.ds_store', '.gitignore']:
        return False
    
    # .md 파일 제외
    if file_lower.endswith('.md'):
        return False
    
    # 코드 파일 확장자만 허용
    code_extensions = ['.py', '.kt', '.java', '.cpp', '.c', '.js', '.swift', '.go', '.rs']
    return any(file_lower.endswith(ext) for ext in code_extensions)

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
            # 코드 파일만 처리
            if not is_code_file(file):
                continue
                
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

#!/usr/bin/env python
import os
from urllib import parse

HEADER="""# 📚 백준, 프로그래머스 등 코딩테스트 문제 풀이 목록

"""

def get_language(file):
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
    
    # 1. 모든 경로를 탐색
    for root, dirs, files in os.walk("."):
        dirs.sort()
        if root == '.':
            for dir in ('.git', '.github'):
                try: dirs.remove(dir)
                except ValueError: pass
            continue
        
        category = os.path.basename(root)
        if category == 'images': continue
        
        # 현재 폴더의 상위 폴더들 리스트 추출
        parts = root.split(os.sep)
        
        # 2. 플랫폼 이름 결정 로직
        # [SWEA/D2/문제] 구조라면 parts는 ['.', 'SWEA', 'D2', '문제'] 형태임
        if len(parts) >= 3:
            # 부모 폴더가 D2, D3 같은 난이도 폴더라면 그 위를 플랫폼으로 인식
            if parts[-2].lower() in ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']:
                platform = parts[-3] if len(parts) >= 4 else parts[-2]
                display_dir = f"{parts[-2]} (SWEA)" # 예: D2 (SWEA)
            else:
                platform = parts[1]
                display_dir = parts[-2]
        else:
            continue

        # 3. 플랫폼 섹션 헤더 생성
        if platform not in directories:
            content += f"## 📚 {platform}\n"
            directories.append(platform)
            # 새로운 플랫폼 시작 시 현재 섹션의 테이블 헤더를 초기화하기 위해 초기값 설정
            current_sub_dir = ""

        # 4. 소분류(D2, D3 혹은 카테고리) 헤더 생성
        if display_dir not in solveds:
            content += f"### 🚀 {display_dir}\n"
            content += "| 문제번호 | 언어 | 링크 |\n| :--- | :---: | :--- |\n"
            solveds.append(display_dir)

        # 5. 파일 목록 처리 (.md 제외)
        files.sort()
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext == '.md' or ext == '': continue
            
            # 문제 번호(폴더명) 중복 체크
            problem_key = f"{platform}_{display_dir}_{category}"
            if problem_key not in solveds:
                link = parse.quote(os.path.join(root, file))
                lang = get_language(file)
                content += f"|{category}|{lang}|[링크]({link})|\n"
                solveds.append(problem_key)
        
    with open("README.md", "w", encoding="utf-8") as fd:
        fd.write(content)

if __name__ == "__main__":
    main()

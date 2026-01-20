#!/usr/bin/env python
import os
from urllib import parse

HEADER="""# 📚 알고리즘 문제 풀이 목록

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
    sections_added = []
    solved_problems = []
    
    # 모든 경로 탐색
    for root, dirs, files in os.walk("."):
        dirs.sort()
        if root == '.':
            for dir in ('.git', '.github'):
                try: dirs.remove(dir)
                except ValueError: pass
            continue
        
        category = os.path.basename(root)
        if category == 'images': continue
        
        parts = root.split(os.sep)
        if len(parts) < 2: continue
        
        # 섹션 이름 결정 (SWEA 특수 구조 처리)
        if len(parts) >= 3 and parts[1].upper() == 'SWEA':
            if parts[2].lower() in ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']:
                display_section = f"{parts[2].upper()} (SWEA)"
            else:
                display_section = parts[2]
        else:
            # 일반 구조 (백준, 프로그래머스 등)
            display_section = parts[1]

        # 플랫폼 큰 제목은 생략하고, 섹션 소제목(###)과 테이블 헤더만 생성
        if display_section not in sections_added:
            content += f"\n### 🚀 {display_section}\n"
            content += "| 문제번호 | 언어 | 링크 |\n| :--- | :---: | :--- |\n"
            sections_added.append(display_section)

        # 소스 코드 파일만 처리 (.md 제외)
        files.sort()
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            
            # MD 파일 및 확장자 없는 파일 필터링
            if ext == '.md' or ext == '':
                continue
                
            # 문제 중복 방지 (섹션+카테고리 기준)
            problem_key = f"{display_section}_{category}"
            if problem_key not in solved_problems:
                link = parse.quote(os.path.join(root, file))
                lang = get_language(file)
                # 표 내용 추가
                content += f"| {category} | {lang} | [링크]({link}) |\n"
                solved_problems.append(problem_key)
        
    with open("README.md", "w", encoding="utf-8") as fd:
        fd.write(content)
    print("✅ README.md 업데이트 완료!")

if __name__ == "__main__":
    main()

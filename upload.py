#!/usr/bin/env python
import os
from urllib import parse

# README 상단 고정 텍스트
HEADER="""# 📚 백준, 프로그래머스 등 코딩테스트 문제 풀이 목록

"""

def get_language(file):
    """파일 확장자로 언어명을 반환합니다."""
    ext = os.path.splitext(file)[1].lower()
    mapping = {
        '.py': 'Python', '.kt': 'Kotlin', '.java': 'Java',
        '.cpp': 'C++', '.js': 'JavaScript', '.swift': 'Swift'
    }
    return mapping.get(ext, ext[1:].upper() if ext else "Unknown")

def main():
    content = HEADER
    platforms_added = []
    sections_added = []
    solved_problems = []
    
    # 디렉토리 순회 (알파벳/숫자 순 정렬)
    for root, dirs, files in os.walk("."):
        dirs.sort()
        if root == '.':
            # 깃 관련 및 이미지 폴더 제외
            for dir in ('.git', '.github', 'images'):
                if dir in dirs: dirs.remove(dir)
            continue
        
        # 1. 경로 분석
        parts = root.split(os.sep)
        if len(parts) < 2: continue
        
        platform = parts[1] # 백준, 프로그래머스, SWEA 등
        category = os.path.basename(root) # 실제 문제 번호/제목 폴더명
        
        # 2. 섹션(티어) 결정 로직
        # [SWEA/D2/문제] 구조 처리
        if platform.upper() == 'SWEA' and len(parts) >= 3:
            if parts[2].lower() in ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']:
                display_section = f"{parts[2].upper()}"
            else:
                display_section = parts[2]
        else:
            # [백준/Bronze/문제] 구조에서 'Bronze' 추출
            display_section = parts[-2] if len(parts) >= 3 else "기타"

        # 3. ## 플랫폼 헤더 추가
        if platform not in platforms_added:
            content += f"\n## 📚 {platform}\n"
            platforms_added.append(platform)

        # 4. ### 티어/섹션 헤더 및 테이블 생성
        # 플랫폼별로 섹션을 구분하기 위해 platform을 키에 포함
        section_key = f"{platform}_{display_section}"
        if section_key not in sections_added:
            content += f"\n### 🚀 {display_section}\n"
            content += "| 문제번호 | 언어 | 링크 |\n| :--- | :---: | :--- |\n"
            sections_added.append(section_key)

        # 5. 파일 처리 (소스 코드만, .md 제외)
        files.sort()
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext == '.md' or ext == '': continue
                
            # 문제 중복 방지 (플랫폼+섹션+문제번호 기준)
            problem_key = f"{platform}_{display_section}_{category}"
            if problem_key not in solved_problems:
                link = parse.quote(os.path.join(root, file))
                lang = get_language(file)
                # 테이블 행 추가
                content += f"| {category} | {lang} | [링크]({link}) |\n"
                solved_problems.append(problem_key)
        
    # 6. 최종 파일 쓰기 (UTF-8)
    with open("README.md", "w", encoding="utf-8") as fd:
        fd.write(content)
    print("✅ README.md has been updated to match the requested layout.")

if __name__ == "__main__":
    main()

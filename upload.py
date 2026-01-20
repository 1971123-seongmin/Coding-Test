#!/usr/bin/env python
import os
import re
from urllib import parse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

# 설정
HEADER = """# 📚 알고리즘 문제 풀이 목록

> 백준, 프로그래머스 등의 문제 풀이 기록을 자동으로 업데이트합니다.

[![solved.ac tier](http://mazassumnida.wtf/api/mini/generate_badge?boj=YOUR_BAEKJOON_ID)](https://solved.ac/YOUR_BAEKJOON_ID)

"""

EXCLUDE_DIRS = {'.git', '.github', 'images', '__pycache__', '.idea', 'venv'}
EXCLUDE_FILES = {'.DS_Store', 'README.md', 'upload.py', '.gitignore'}

PLATFORMS = {
    "백준": {
        "emoji": "🥇",
        "url_template": "https://www.acmicpc.net/problem/{problem_id}"
    },
    "프로그래머스": {
        "emoji": "💻",
        "url_template": "https://programmers.co.kr/learn/courses/30/lessons/{problem_id}"
    }
}


@dataclass
class Problem:
    """문제 정보"""
    platform: str
    category: str
    problem_id: str
    title: str
    file_path: str
    language: str


class MarkdownGenerator:
    def __init__(self):
        self.content = HEADER
        self.problems: Dict[str, List[Problem]] = {
            platform: [] for platform in PLATFORMS.keys()
        }
    
    def generate_list(self):
        """README 생성"""
        self._scan_directories()
        self._build_content()
        self._save_file()
    
    def _scan_directories(self):
        """디렉토리 스캔하여 문제 수집"""
        for platform in PLATFORMS.keys():
            platform_path = Path(platform)
            
            if not platform_path.exists():
                continue
            
            # 플랫폼 디렉토리 내 모든 하위 디렉토리 탐색
            for category_path in platform_path.iterdir():
                if not category_path.is_dir():
                    continue
                
                if category_path.name in EXCLUDE_DIRS:
                    continue
                
                # 카테고리 내 문제 파일 수집
                for file_path in category_path.rglob('*'):
                    if not file_path.is_file():
                        continue
                    
                    if file_path.name in EXCLUDE_FILES:
                        continue
                    
                    problem = self._parse_problem(platform, category_path.name, file_path)
                    if problem:
                        self.problems[platform].append(problem)
    
    def _parse_problem(self, platform: str, category: str, file_path: Path) -> Problem:
        """파일에서 문제 정보 추출"""
        
        # 파일명에서 문제 번호 추출 시도
        # 예: "1000.py", "1000_A+B.kt", "두개뽑아서더하기.py"
        filename = file_path.stem  # 확장자 제외
        
        # 숫자로 시작하는 경우 (백준)
        number_match = re.match(r'^(\d+)', filename)
        if number_match:
            problem_id = number_match.group(1)
            title = filename[len(problem_id):].strip('_- ') or f"문제 {problem_id}"
        else:
            # 프로그래머스 등 (파일명이 문제 제목)
            problem_id = ""
            title = filename
        
        # 언어 추출
        language = self._get_language(file_path.suffix)
        
        return Problem(
            platform=platform,
            category=category,
            problem_id=problem_id,
            title=title,
            file_path=str(file_path),
            language=language
        )
    
    def _get_language(self, extension: str) -> str:
        """확장자에서 언어 추출"""
        language_map = {
            '.py': 'Python',
            '.kt': 'Kotlin',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.swift': 'Swift',
            '.go': 'Go',
            '.rs': 'Rust',
        }
        return language_map.get(extension.lower(), extension[1:].upper())
    
    def _build_content(self):
        """마크다운 콘텐츠 생성"""
        for platform, problems in self.problems.items():
            if not problems:
                continue
            
            config = PLATFORMS[platform]
            self.content += f"\n## {config['emoji']} {platform}\n\n"
            
            # 카테고리별로 그룹화
            categories = {}
            for problem in problems:
                if problem.category not in categories:
                    categories[problem.category] = []
                categories[problem.category].append(problem)
            
            # 카테고리별로 출력
            for category in sorted(categories.keys()):
                self.content += f"### 📂 {category}\n\n"
                self.content += "| 번호 | 제목 | 언어 | 링크 |\n"
                self.content += "| :---: | :--- | :---: | :---: |\n"
                
                # 문제 번호순 정렬
                category_problems = sorted(
                    categories[category],
                    key=lambda p: int(p.problem_id) if p.problem_id.isdigit() else 0
                )
                
                for problem in category_problems:
                    self._add_problem_row(problem, config)
                
                self.content += "\n"
    
    def _add_problem_row(self, problem: Problem, config: Dict):
        """문제 행 추가"""
        # 파일 링크
        file_link = parse.quote(problem.file_path)
        
        # 문제 링크 (번호가 있는 경우만)
        if problem.problem_id:
            problem_url = config['url_template'].format(problem_id=problem.problem_id)
            problem_link = f"[{problem.problem_id}]({problem_url})"
        else:
            problem_link = "-"
        
        # 제목 링크 (파일로)
        title_link = f"[{problem.title}]({file_link})"
        
        self.content += f"| {problem_link} | {title_link} | {problem.language} | [코드]({file_link}) |\n"
    
    def _save_file(self):
        """파일 저장"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(self.content)
        
        print("✅ README.md 업데이트 완료!")
        
        # 통계 출력
        total = sum(len(problems) for problems in self.problems.values())
        print(f"📊 총 {total}개 문제 풀이 기록")
        for platform, problems in self.problems.items():
            if problems:
                print(f"   - {platform}: {len(problems)}개")


if __name__ == "__main__":
    generator = MarkdownGenerator()
    generator.generate_list()
```

#!/usr/bin/env python
import os
from urllib import parse

# 설정 값 관리
HEADER = """# 📚 알고리즘 문제 풀이 목록
> 백준, 프로그래머스 등의 문제 풀이 기록을 자동으로 업데이트합니다.

"""
EXCLUDE_DIRS = {'.git', '.github', 'images'}
PLATFORMS = ["백준", "프로그래머스"]

class MarkdownGenerator:
    def __init__(self):
        self.content = HEADER
        self.directories = set()
        self.solved_categories = set()

    def generate_list(self):
        # 현재 경로의 디렉토리 탐색
        for root, dirs, files in os.walk("."):
            dirs.sort()
            
            # 불필요한 디렉토리 제외
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            if root == '.': continue

            category = os.path.basename(root)
            parent_dir = os.path.basename(os.path.dirname(root))

            if parent_dir == '.': continue

            # 섹션 및 테이블 헤더 생성
            self._add_section(parent_dir)
            
            # 문제 항목 추가
            for file in files:
                self._add_problem(category, root, file)

        self._save_file()

    def _add_section(self, directory):
        if directory not in self.directories:
            if directory in PLATFORMS:
                self.content += f"\n## 📚 {directory}\n"
            else:
                self.content += f"\n### 🚀 {directory}\n"
                self.content += "| 문제번호 | 링크 |\n| :--- | :--- |\n"
            self.directories.add(directory)

    def _add_problem(self, category, root, file):
        if category not in self.solved_categories:
            relative_path = os.path.join(root, file)
            link = parse.quote(relative_path)
            self.content += f"| {category} | [바로가기]({link}) |\n"
            self.solved_categories.add(category)

    def _save_file(self):
        with open("README.md", "w", encoding="utf-8") as fd:
            fd.write(self.content)

if __name__ == "__main__":
    generator = MarkdownGenerator()
    generator.generate_list()

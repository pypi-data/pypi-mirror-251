import requests
from setuptools import setup

# GitHub README 파일의 URL
github_readme_url = "https://raw.githubusercontent.com/jjvoka/getpath/main/README.md"

# README 파일 내용 가져오기
response = requests.get(github_readme_url)

# README 파일 내용을 사용할 수 있습니다.
readme_content = response.text

# 패키지 정보 설정
setup(
    name='GetResourcePath',
    version='1.0',
    description="A Python package for managing resource paths and file operations in cross-platform applications.",
    long_description=readme_content,  # GitHub README 내용을 사용
    long_description_content_type='text/markdown',  # README 파일 형식 지정
    author='voka',
    author_email='jjvoka@gmail.com',
    url='https://github.com/jjvoka/getpath',
    packages=['get_resource_path'],
    install_requires=[
        # 패키지의 의존성이 있다면 여기에 추가
    ],
)
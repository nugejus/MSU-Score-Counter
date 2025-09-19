"""
config.py — 전역 설정 및 환경변수 로딩
"""

import os
from pathlib import Path
# -------------------
# 기본 경로
# -------------------
BASE_DIR = Path(__file__).resolve().parent

# -------------------
# 서비스 URL
# -------------------
MSU_LOGIN_URL = os.getenv("MSU_LOGIN_URL", "https://lk.msu.ru/cabinet")


# config.py (추가)
LOGIN_SUCCESS_PROBES = [
    ("link", "Оценки"),                 # 상단/사이드 메뉴에 'Оценки' 링크가 보이면 성공
]
LOGIN_ERROR_PROBES = [
    ("css", ".alert-danger"),           # 부트스트랩 경고 박스
    ("css", ".invalid-feedback"),       # 폼 밑 에러
    ("css", ".help-block"),
]
LOGIN_POSTWAIT_SEC = 5                  # 로그인 클릭 후 최대 대기
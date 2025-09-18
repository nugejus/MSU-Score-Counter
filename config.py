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

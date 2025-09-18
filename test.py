import sys
import pytest

def main():
    # 루트에서 pytest 실행
    # -q : 간결한 출력
    # test/ 폴더 아래 모든 test_*.py 실행
    sys.exit(pytest.main(["-q", "test"]))

if __name__ == "__main__":
    main()

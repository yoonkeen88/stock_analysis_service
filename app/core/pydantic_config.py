"""
Pydantic 공통 설정
"""
from pydantic import ConfigDict

# 모든 Pydantic 모델에서 사용할 공통 설정
COMMON_PYDANTIC_CONFIG = ConfigDict(
    protected_namespaces=(),  # model_name 같은 필드 사용 허용
    from_attributes=True,  # SQLAlchemy 모델에서 자동 변환
    validate_assignment=True,  # 할당 시 검증
)


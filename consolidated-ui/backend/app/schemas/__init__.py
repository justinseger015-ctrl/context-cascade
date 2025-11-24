"""
Pydantic Schemas Package
API request/response models
"""

from .agent_schemas import (
    AgentBase,
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentDetailedResponse,
    AgentListResponse,
    AgentActivityLog,
    AgentActivityResponse,
    ExecutionHistoryItem,
)

from .task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskDeleteResponse,
    TaskStatus,
    TaskSortField,
    SortOrder,
    TaskQueryParams,
    ExecutionResultResponse
)

__all__ = [
    # Agent schemas
    "AgentBase",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    "AgentDetailedResponse",
    "AgentListResponse",
    "AgentActivityLog",
    "AgentActivityResponse",
    "ExecutionHistoryItem",
    # Task schemas
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskListResponse",
    "TaskDeleteResponse",
    "TaskStatus",
    "TaskSortField",
    "SortOrder",
    "TaskQueryParams",
    "ExecutionResultResponse"
]

from .user_schemas import (
    UserRegister,
    UserLogin,
    UserUpdate,
    PasswordChange,
    RefreshTokenRequest,
    UserResponse,
    TokenResponse,
    TokenVerifyResponse,
    LoginResponse,
    MessageResponse,
)

# Add to __all__
__all__.extend([
    "UserRegister",
    "UserLogin",
    "UserUpdate",
    "PasswordChange",
    "RefreshTokenRequest",
    "UserResponse",
    "TokenResponse",
    "TokenVerifyResponse",
    "LoginResponse",
    "MessageResponse",
])

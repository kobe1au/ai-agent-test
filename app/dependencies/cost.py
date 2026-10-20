from fastapi import Depends,Query

from app.schemas.user import CurrentUser
from app.dependencies.auth import get_current_user

class CostContext:
    def __init__(self,user_id: str,max_tokens: int):
        self.user_id = user_id
        self.max_tokens = max_tokens

async def get_cost_context(
    current_user: CurrentUser = Depends(get_current_user),
    max_tokens: int = Query(default=1000,description="最大消耗token数")
) -> CostContext:
    return CostContext(current_user.user_id,max_tokens)
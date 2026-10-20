from fastapi import Header,HTTPException,status

async def get_workspace_id(
        x_workspace_id: str | None = Header(default=None)
)-> str:
    if not x_workspace_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少请求头 x-workspace-id"
        )

    return x_workspace_id
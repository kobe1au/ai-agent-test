from pydantic import BaseModel,ValidationError

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

request = ChatRequest(message="Hi")
print(request.message)
print(request.session_id)
print(request.model_dump())

try:
    request1 = ChatRequest(message=1234)
except ValidationError as e:
    print(e)
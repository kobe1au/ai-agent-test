from contextvars import ContextVar

trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default="-")
user_id_var: ContextVar[str | None] = ContextVar("user_id", default="-")

def set_trace_id(trace_id: str) -> None:
    trace_id_var.set(trace_id)

def get_trace_id() -> str | None:
    return trace_id_var.get()

def set_user_id(user_id: str):
    user_id_var.set(user_id)

def get_user_id() -> str:
    return user_id_var.get()
from fastapi import Query

class PaginationParams:
    def __init__(
            self,
            page: int = Query(default=1, description="页码"),
            page_size: int = Query(default=10, description="每页数量"),
    ):
        self.page = page
        self.page_size = page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
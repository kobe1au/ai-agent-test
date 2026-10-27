from typing import Literal
from pydantic import BaseModel, Field

class QueryOrderArgs(BaseModel):
    order_id: str = Field(...,min_length=1, description="订单ID")

class QueryOrderResult(BaseModel):
    order_id: str = Field(...,min_length=1, description="订单ID")
    status: Literal[
        "pending",
        "paid",
        "shipped",
        "delivered",
        "cancelled",
        "refunding",
        "refunded",
        "not_found",
    ] = Field(..., description="订单状态")

    status_text: str = Field(..., description="订单状态描述")
    tracking_company: str | None = Field(None, description="物流公司")
    tracking_no: str | None = Field(None, description="物流单号")
    latest_event: str | None = Field(None, description="最新物流事件")

class QueryLogisticsArgs(BaseModel):
    tracking_no: str | None = Field(None, description="物流单号")

class QueryLogisticsResult(BaseModel):
    tracking_no: str | None = Field(None, description="物流单号")
    tracking_company: str | None = Field(None, description="物流公司")
    latest_event: str | None = Field(None, description="最新物流事件")
    status: Literal[
        "in_transit",
        "delivered",
        "exception",
        "not_found",
    ] = Field(..., description="物流状态")

class TransferHumanArgs(BaseModel):
    reason: str = Field(..., description="转人工原因")

class TransferHumanResult(BaseModel):
    ticket_id: str = Field(..., description="人工客服工单 ID")
    message: str = Field(..., description="提示信息")
    status: Literal["created"] = Field(default="created",description="工单状态")

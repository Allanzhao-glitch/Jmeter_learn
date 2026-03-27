from fastapi import FastAPI, HTTPException, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import time
import random
import uuid
import os

app = FastAPI(title="JMeter学习后端API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

users_db = [
    {"id": 1, "name": "张三", "email": "zhangsan@example.com", "age": 25},
    {"id": 2, "name": "李四", "email": "lisi@example.com", "age": 30},
    {"id": 3, "name": "王五", "email": "wangwu@example.com", "age": 28},
    {"id": 4, "name": "赵六", "email": "zhaoliu@example.com", "age": 35},
    {"id": 5, "name": "钱七", "email": "qianqi@example.com", "age": 22}
]

products_db = [
    {"id": 1, "name": "iPhone 15", "price": 5999, "category": "手机", "stock": 100},
    {"id": 2, "name": "MacBook Pro", "price": 12999, "category": "电脑", "stock": 50},
    {"id": 3, "name": "AirPods Pro", "price": 1899, "category": "耳机", "stock": 200},
    {"id": 4, "name": "iPad Air", "price": 4399, "category": "平板", "stock": 80},
    {"id": 5, "name": "Apple Watch", "price": 2999, "category": "手表", "stock": 120}
]

orders_db = []
order_id_counter = 1

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = 20

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class OrderItem(BaseModel):
    id: int
    name: str
    price: int
    quantity: int = 1

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]
    total: int

class UploadRequest(BaseModel):
    filename: str
    size: Optional[int] = 1024

@app.get("/")
def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "JMeter学习后端服务正在运行", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/users")
def get_users(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_users = users_db[start_index:end_index]
    return {
        "total": len(users_db),
        "page": page,
        "limit": limit,
        "data": paginated_users
    }

@app.get("/api/users/{user_id}")
def get_user(user_id: int = Path(..., ge=1)):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="用户不存在")

@app.post("/api/users")
def create_user(user: UserCreate):
    new_id = max([u["id"] for u in users_db]) + 1 if users_db else 1
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
    users_db.append(new_user)
    return new_user

@app.put("/api/users/{user_id}")
def update_user(user_id: int = Path(..., ge=1), user: UserUpdate = None):
    for u in users_db:
        if u["id"] == user_id:
            if user.name:
                u["name"] = user.name
            if user.email:
                u["email"] = user.email
            if user.age:
                u["age"] = user.age
            return u
    raise HTTPException(status_code=404, detail="用户不存在")

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int = Path(..., ge=1)):
    for i, u in enumerate(users_db):
        if u["id"] == user_id:
            users_db.pop(i)
            return {"message": "用户删除成功"}
    raise HTTPException(status_code=404, detail="用户不存在")

@app.get("/api/products")
def get_products(
    category: Optional[str] = None,
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0)
):
    filtered_products = products_db.copy()
    
    if category:
        filtered_products = [p for p in filtered_products if p["category"] == category]
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] >= min_price]
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]
    
    return filtered_products

@app.get("/api/products/{product_id}")
def get_product(product_id: int = Path(..., ge=1)):
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="产品不存在")

@app.post("/api/login")
def login(request: LoginRequest):
    if not request.username or not request.password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")
    
    if request.username == "admin" and request.password == "admin123":
        return {
            "success": True,
            "token": f"mock-jwt-token-{uuid.uuid4()}",
            "user": {"id": 1, "username": "admin", "role": "admin"}
        }
    raise HTTPException(status_code=401, detail="用户名或密码错误")

@app.post("/api/orders")
def create_order(order: OrderCreate):
    global order_id_counter
    
    if not order.items or not order.total:
        raise HTTPException(status_code=400, detail="订单信息不完整")
    
    new_order = {
        "id": order_id_counter,
        "user_id": order.user_id,
        "items": [item.dict() for item in order.items],
        "total": order.total,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    orders_db.append(new_order)
    order_id_counter += 1
    return new_order

@app.get("/api/orders")
def get_orders(user_id: Optional[int] = Query(None)):
    if user_id:
        return [o for o in orders_db if o["user_id"] == user_id]
    return orders_db

@app.get("/api/orders/{order_id}")
def get_order(order_id: int = Path(..., ge=1)):
    for order in orders_db:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="订单不存在")

@app.get("/api/slow")
def slow_endpoint(delay: int = Query(2000, ge=0, le=30000)):
    time.sleep(delay / 1000)
    return {"message": "慢接口响应", "delay_ms": delay}

@app.get("/api/random-delay")
def random_delay_endpoint(
    min_delay: int = Query(100, ge=0),
    max_delay: int = Query(3000, ge=0)
):
    random_delay = random.randint(min_delay, max_delay)
    time.sleep(random_delay / 1000)
    return {"message": "随机延迟响应", "delay_ms": random_delay}

@app.post("/api/upload")
def upload_file(upload: UploadRequest):
    time.sleep(0.5)
    return {
        "success": True,
        "message": "文件上传成功",
        "filename": upload.filename,
        "size": upload.size
    }

@app.get("/api/error")
def error_endpoint(code: int = Query(500, ge=400, le=599)):
    error_messages = {
        400: "请求参数错误",
        401: "未授权",
        403: "禁止访问",
        404: "资源不存在",
        500: "服务器内部错误",
        502: "网关错误",
        503: "服务不可用"
    }
    raise HTTPException(status_code=code, detail=error_messages.get(code, "未知错误"))

@app.get("/api/stream/{count}")
def stream_endpoint(count: int = Path(..., ge=1, le=1000)):
    result = [{"id": i, "data": f"item-{i}", "timestamp": datetime.now().isoformat()} for i in range(1, count + 1)]
    return result

@app.get("/api/concurrent-test")
def concurrent_test():
    return {
        "message": "并发测试接口",
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
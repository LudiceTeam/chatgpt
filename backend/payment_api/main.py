from fastapi import FastAPI,Depends,Request,HTTPException,Header,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from dotenv import load_dotenv
import sys 
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.util import get_remote_address
from jose import JWTError,jwt
import time
import hmac
import hashlib
from backend.payment_api.auth import create_refresh_token,create_access_token 
from backend.database.jwt_db.jwt_core import safe_first_refresh_token,get_user_refresh_token,update_refresh_token
from backend.database.payment_db.payment_core import create_payment ,change_payment_state,get_payment_by_id
from backend.database.core import subscribe,subscribe_basic
import requests
import uvicorn
import base64
import json

pay_app = FastAPI()
limiter = Limiter(key_func=get_remote_address)



class CreatePayment(BaseModel):
    user_id:str
    tarif:str


load_dotenv()



CLOUDPAYMENTS_PUBLIC_ID = os.getenv("CLOUDPAYMENTS_PUBLIC_ID")
CLOUDPAYMENTS_API_SECRET = os.getenv("CLOUDPAYMENTS_API_SECRET")
api_token = os.getenv("API_TOKEN")



def generate_cloudpayments_link(
    payment_id: str,
    user_id: str,
    price: int,
    tariff: str,
) -> str:
    url = "https://api.cloudpayments.ru/orders/create"

    payload = {
        "Amount": price,
        "Currency": "RUB",
        "Description": f"Оплата тарифа {tariff}",
        "InvoiceId": payment_id,
        "AccountId": f"tg_{user_id}",
        "SuccessRedirectUrl": "https://your-site.com/payment/success",
        "FailRedirectUrl": "https://your-site.com/payment/fail",
        "JsonData": {
            "tg_user_id": user_id,
            "tariff": tariff
        }
    }

    resp = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(CLOUDPAYMENTS_PUBLIC_ID, CLOUDPAYMENTS_API_SECRET),
        timeout=15
    )

    data = resp.json()

    if not resp.ok or not data.get("Success"):
        raise HTTPException(status_code=500, detail="CloudPayments error")

    return data["Model"]["Url"]

def verify_token(recieved_token:str) -> bool:
    if api_token != recieved_token:
        return False
    return True

@limiter.limit("20/minute")
@pay_app.post("/create-payment")
async def create_payment_api(request:Request,req:CreatePayment,token:str = Header(...)):
    if not verify_token(token):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "FORBIDDEN")
    price = None
    if req.tarif == "basic":
        price = 400
    elif req.tarif == "premium":
        price = 1000
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Invalid json")
    

    payment_id:str = await create_payment(
        price = price,
        user_id = req.user_id
    )

    link = generate_cloudpayments_link(
        payment_id,
        req.user_id,
        price,
        req.tarif
    )
    return {
        "status":"ok",
        "link":link
    }
    


def verify_cloudpayments_hmac(raw_body: bytes, received_hmac: str | None) -> bool:
    if not received_hmac or not CLOUDPAYMENTS_API_SECRET:
        return False

    digest = hmac.new(
        CLOUDPAYMENTS_API_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).digest()

    calculated_hmac = base64.b64encode(digest).decode("utf-8")
    return hmac.compare_digest(calculated_hmac, received_hmac)


class CloudPaymentsPayWebhook(BaseModel):
    TransactionId: int | None = None
    Amount: float
    InvoiceId: str | None = None
    AccountId: str | None = None
    Email: str | None = None
    Data: dict | None = None


@limiter.limit("20/minute")
@pay_app("/webhook/pay")
async def webhook_api(request:Request):
    raw_body = await request.body()

    received_hmac = request.headers.get("X-Content-HMAC") or request.headers.get("Content-HMAC")
    if not verify_cloudpayments_hmac(raw_body, received_hmac):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook signature"
        )

    try:
        payload_dict = json.loads(raw_body.decode("utf-8"))
        payload = CloudPaymentsPayWebhook(**payload_dict)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook payload"
        )

    if not payload.InvoiceId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="InvoiceId is required"
        )

    payment = await get_payment_by_id(payload.InvoiceId)
    if payment == {}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    # idempotency: если уже оплачен, просто отвечаем успехом
    if payment["status"] == "paid":
        return JSONResponse(content={"code": 0})

    # сверяем сумму
    if float(payment["price"]) != float(payload.Amount):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount"
        )

    # сверяем account id
    expected_account_id = payment["user_id"]
    if payload.AccountId != expected_account_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account id"
        )
    

    await change_payment_state(payment["payment_id"],"paid")

    if payment["price"] == 400:
        await subscribe_basic(payment["user_id"])
    elif payment["price"] == 1000:
        await subscribe(payment["user_id"])

    return JSONResponse(content={"code": 0})



if __name__ == "__main__":
    uvicorn.run(pay_app,host = "0.0.0.0",port = 1487)




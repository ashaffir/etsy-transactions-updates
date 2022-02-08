import requests
import shutil
import csv
from fastapi import FastAPI, Request, UploadFile
import starlette.status as status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import (
    ETSY_X_API_KEY,
    ETSY_SHOP_ID,
)
from generate_code import CODEGEN
from utils import update_transactions

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
code_gen = CODEGEN()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "x-api-key": f"{ETSY_X_API_KEY}",
}


@app.get("/", response_class=HTMLResponse)
@app.post("/")
async def home(request: Request):
    context = {"request": request}
    if request.method == "POST":
        context["uploaded"] = True

    listings_url = code_gen.listing_code_generator()
    user_url = code_gen.user_code_generator()
    transactions_url = code_gen.transactions_generator()

    context["transactions_url"] = transactions_url
    context["listings_url"] = listings_url
    context["user_url"] = user_url

    return templates.TemplateResponse(
        "index.html",
        context=context,
    )


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    with open(f"./csv_files/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    code_gen.file_path = f"./csv_files/{file.filename}"

    return RedirectResponse("/")


@app.get("/ping", response_class=HTMLResponse)
async def app_ping(request: Request):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": f"{ETSY_X_API_KEY}",
    }

    response = requests.get(
        "https://api.etsy.com/v3/application/openapi-ping", headers=headers
    )

    return templates.TemplateResponse(
        "test.html", {"request": request, "ping_result": response}
    )


@app.get("/oauth/redirect", response_class=HTMLResponse)
async def oauth_redirect(request: Request, code: str):

    context = {"request": request}
    token_url = "https://api.etsy.com/v3/public/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": f"{ETSY_X_API_KEY}",
        "redirect_uri": "http://localhost:8000/oauth/redirect",
        "code": f"{code}",
        "code_verifier": f"{code_gen.code_verifier}",
    }

    response = requests.post(token_url, data=payload)
    bearer_token = response.json()["access_token"]

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": f"{ETSY_X_API_KEY}",
        "Authorization": f"Bearer {bearer_token}",
    }

    user_id = int(bearer_token.split(".")[0])
    user_url = f"https://api.etsy.com/v3/application/users/{user_id}"
    # response = requests.get(user_url, headers=headers)

    listings_url = (
        f"https://openapi.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/listings"
    )

    # response = requests.get(listings_url, headers=headers)

    response = update_transactions(code_gen.file_path, headers)

    context["response"] = response

    return templates.TemplateResponse(
        "result.html",
        context=context,
    )


@app.get("/test")
def test():
    return RedirectResponse("/ping")


@app.get("/shop", response_class=HTMLResponse)
def get_shops(request: Request):
    shops_url = f"https://api.etsy.com/v3/application/shops?shop_name=REDCHERRYBLVD"
    response = requests.get(shops_url, headers=headers)
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "response": response,
            "response_type": "shop description",
        },
    )


@app.get("/shop-info", response_class=HTMLResponse)
def get_shops(request: Request):
    shops_url = f"https://api.etsy.com/v3/application/shops/{ETSY_SHOP_ID}"
    response = requests.get(shops_url, headers=headers)
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "response": response,
            "response_type": "shop information",
        },
    )

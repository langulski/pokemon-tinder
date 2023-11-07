from fastapi import APIRouter, Request, Depends
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.database.database import fetch_data_paginated, save_selected_pokemons,retrive_saved_pokemons
from src.auth.auth import get_current_user_from_cookie, User


last_id = 1

router = APIRouter(tags=["pokemons"])
templates = Jinja2Templates(directory="templates")


@router.get("/home", response_class=HTMLResponse)
def home(
    request: Request, user: Annotated[User, Depends(get_current_user_from_cookie)]
):
    context = {"request": request, "user": user}
    return templates.TemplateResponse("home.html", context)




@router.get("/get_more_cards", response_class=JSONResponse)
def get_more_cards(
    request: Request, user: Annotated[User, Depends(get_current_user_from_cookie)]
):
    new_cards = fetch_data_paginated(
        sql_file="./src/database/sql/retrive_pokemons.sql",
        user_id=user["id"],
        limit=5,
        offset=5,
    )
    return {"cards": new_cards}


@router.get("/index", response_class=HTMLResponse)
def index(
    request: Request, user: Annotated[User, Depends(get_current_user_from_cookie)]
):
    cards = fetch_data_paginated(
        sql_file="./src/database/sql/retrive_pokemons.sql", user_id=user["id"], limit=5
    )
    context = {"request": request, "cards": cards, "user": user}
    return templates.TemplateResponse("index.html", context)


@router.get("/gallery", response_class=HTMLResponse)
def gallery(
    request: Request, user: Annotated[User, Depends(get_current_user_from_cookie)]
):
    cards = retrive_saved_pokemons(
        sql_file="./src/database/sql/retrive_saved_pokemons.sql", user_id=user["id"])
    context = {"request": request, "cards": cards, "user": user}
    return templates.TemplateResponse("gallery.html", context)


class CardID(BaseModel):
    id: int
    love: bool


@router.post("/save_liked_card")
def save_liked_card(
    card: CardID,
    request: Request,
    user: Annotated[User, Depends(get_current_user_from_cookie)],
):
    save_selected_pokemons(
        sql_file="./src/database/sql/save_selected_pokemons.sql",
        user_id=user["id"],
        pokemon_id=card.id,
        love=card.love
    )
    return {"message": "Card saved successfully"}

#!/usr/bin/env python3
from typing import Optional

from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui
from . import home

@ui.page('/shopping/list')
async def shopping_list(request: Request) -> Optional[RedirectResponse]:
    ui.button('Change page title', on_click=lambda: ui.page_title('New Title'))

    return await home.render(request)

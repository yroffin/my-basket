from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from authlib.integrations.starlette_client import OAuth, OAuthError
import os

oauth = OAuth()

def logout() -> None:
    del app.storage.user['user_data']
    ui.navigate.to('/')

@app.get('/auth')
async def google_oauth(request: Request) -> RedirectResponse:
    try:
        user_data = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f'OAuth error: {e}')
        return RedirectResponse('/')  # or return an error page/message
    app.storage.user['user_data'] = user_data
    return RedirectResponse('/')

async def render(request: Request) -> Optional[RedirectResponse]:
    user_data = app.storage.user.get('user_data', None)
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('HEADER')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        if user_data:
            ui.label(f'Welcome {user_data.get("userinfo", {}).get("name", "")}!')
            ui.button('Logout', on_click=logout)
    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
        ui.label('LEFT DRAWER')
    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        ui.label('RIGHT DRAWER')
        ui.button(icon='savings',
            on_click=lambda: ui.navigate.to('/shopping/list'))
    with ui.footer().style('background-color: #3874c8'):
        if 'HOSTNAME' in os.environ:
            ui.label(os.environ['HOSTNAME'])
        else:
            ui.label("no hostname")


    if not user_data:
        url = request.url_for('google_oauth')
        return await oauth.google.authorize_redirect(request, url)

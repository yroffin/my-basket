#!/usr/bin/env python3
from typing import Optional

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui

oauth = OAuth()

@app.get('/auth')
async def google_oauth(request: Request) -> RedirectResponse:
    try:
        user_data = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f'OAuth error: {e}')
        return RedirectResponse('/')  # or return an error page/message
    app.storage.user['user_data'] = user_data
    return RedirectResponse('/')


def logout() -> None:
    del app.storage.user['user_data']
    ui.navigate.to('/')


@ui.page('/')
async def main(request: Request) -> Optional[RedirectResponse]:
    user_data = app.storage.user.get('user_data', None)
    if user_data:
        ui.label(f'Welcome {user_data.get("userinfo", {}).get("name", "")}!')
        ui.button('Logout', on_click=logout)
        return None
    else:
        url = request.url_for('google_oauth')
        return await oauth.google.authorize_redirect(request, url)

import os
import logging

from core.config_manager import ConfigManager

if __name__ in {"__main__", "__mp_main__"}:
    # Configure basic logging to the console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('__main__')
    logger.info(f'Load configuration from {os.environ['CONFIG_YAML']}')

    # Get the singleton instance (will create if it doesn't exist)
    config_manager = ConfigManager(os.environ['CONFIG_YAML'])
    config = config_manager.get("config")
    logging.basicConfig(level=logging.INFO, format=config['logging']['format'])

    # Get the credentials from the Google Cloud Console
    # https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id
    oauth.register(
        name='google',
        server_metadata_url=config['google']['server_metadata_url'],
        client_id=os.environ['CONFIG_GOOGLE_CLIENT_ID'],
        client_secret=os.environ['CONFIG_GOOGLE_CLIENT_SECRET'],
        client_kwargs={'scope': config['google']['scope']},
        redirect_uri=config['google']['redirect_uri']
    )

    ui.run(
        uvicorn_reload_includes=config['ui']['uvicorn_reload_includes'],
        reload=config['ui']['reload'],
        reconnect_timeout=config['ui']['reconnect_timeout'],
        host=config['ui']['host'],
        storage_secret=config['storage']['secret']
    )

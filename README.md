# my-basket
Tiny basket application

# configuration

```yaml
config:
  google:
    client-id: xxxxxxx.apps.googleusercontent.com
    client-secret: xxxxxxxxxxxxxxxxxxx
    scope: openid email profile
    server_metadata_url: https://accounts.google.com/.well-known/openid-configuration
  storage:
    secret: my secret
  logging:
    format: "%(asctime)s - %(levelname)s - %(message)s"
  ui:
    host: localhost
```

# dev

```shell
python3 -m venv .env
. .env/bin/activate
pip3 install -r requirements.txt
```

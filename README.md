# vbbot

### Переменные окружения

- VB_TOKEN
- [HOOK](https://developers.viber.com/docs/api/python-bot-api/#setting-a-webhook)*
- API_BASE_URL
- START_DAY
- END_DAY
- [SECRET_KEY](https://docs.djangoproject.com/en/5.0/ref/settings/#secret-key)
- [DEBUG](https://docs.djangoproject.com/en/5.0/ref/settings/#debug)
- [ALLOWED_HOSTS](https://docs.djangoproject.com/en/5.0/ref/settings/#allowed-hosts)

```bash
$ cat .env
VB_TOKEN=47a...
HOOK=mackerel-cuddly-deadly.ngrok-free.app
API_BASE_URL=lk-api...
ALLOWED_HOSTS='127.0.0.1,mackerel-cuddly-deadly.ngrok-free.app'
SECRET_KEY=django-insecure-9...
START_DAY=15
END_DAY=25
```

*Вебук должен ставиться на любой HTTPS сервер

### Как запустить вебхук

```bash
python sethook.py
```
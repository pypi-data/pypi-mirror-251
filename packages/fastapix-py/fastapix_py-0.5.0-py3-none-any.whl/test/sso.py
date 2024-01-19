# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : sso.py
# @Time     : 2023/11/28 14:50
import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import fastapix
from fastapix import offline
from fastapix.sso.plugin.casdoor import Casdoor

app = FastAPI(
    swagger_ui_oauth2_redirect_url='/callback',
    swagger_ui_init_oauth={
        'useBasicAuthenticationWithAccessCodeGrant': True,
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': '11777dc9921e886dbf82',
        'clientSecret': '47d2d7fc76522848e3efd2b9965f6c14ed4c76a2',
    },
)


sso = Casdoor(
    endpoint='http://45.251.240.110:8000',
    redirect_url='http://127.0.0.1:1990/a',
    client_id='11777dc9921e886dbf82',
    client_secret='47d2d7fc76522848e3efd2b9965f6c14ed4c76a2',
    certificate="""-----BEGIN CERTIFICATE-----
MIIE3TCCAsWgAwIBAgIDAeJAMA0GCSqGSIb3DQEBCwUAMCgxDjAMBgNVBAoTBWFk
bWluMRYwFAYDVQQDEw1jZXJ0LWJ1aWx0LWluMB4XDTIzMTIwNTA2NDA0NFoXDTQz
MTIwNTA2NDA0NFowKDEOMAwGA1UEChMFYWRtaW4xFjAUBgNVBAMTDWNlcnQtYnVp
bHQtaW4wggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDiUburEApwq4rt
rVvwgYNBOhnztND94qhO5vBaNvoApLk8iMv4B+E+YElRq5BwHlWnUcX8yxxxjkvr
Pic6tR6hRAWDaUdRvhhYIBllom8y6+NsxJoWyB8Fqt5jAOXZpbZ2KOv56EHfRVNn
jjRGCvZn6iE/A2WHAe0iY4Hk177MDnFe1T++4EcksB8s8otwO1Rf28ld5bEl33/S
s5YwJNQiMZD9tM8YIaitlw2fnFiuMBsy6GUrVFLXt8Sn1J47vKal+QLPV1SxpwZb
tJ+KujQ6fbVoQIOmvkKOD4wmzbBsxfNrd8OkFuUi0MpgN5ZVKx1gosgQE2jX+s6L
6S/WnAUzuFmEZI2HwjykxypjK0GNiHk5z90elqiIEMgdx69tLu1pkIEcuO6egtBf
b742Kem7pfMBxnKXjGomah9GgJnzAVzlazEmxfuGPgHY9+GTP2QxpesDuQx31/Fk
tw/a42CVX3SmsXjHe3mpHEBtgpws3d5U81RFFDzwjjnDaamgwFh/YKtB4vX8iTVP
U6t/ZaMt7Vz+0ibzOGRkHylKRgRjHax1OjgwZ589uJ1jgVcfxpqSpXjPvqsv1FeB
3qVbhgnjHiz1cfSj0IsLQSDcBkSaLzEqOD6+AntsmVSxmc4qWjnKxz7EHE5G/NEC
WI/MUrBAhRYrsKc8IXygYxQKHUCG/QIDAQABoxAwDjAMBgNVHRMBAf8EAjAAMA0G
CSqGSIb3DQEBCwUAA4ICAQAaHG0bvCmBCsg5FySn5zeo1WMUddZyxJURoqo5uV+b
WtgELJ4+00zGj7DWWJ9I1iUufYBiqaUCvAfsJdJ1UhXmlthtX51h515Ne9OhJrJX
KyRsrT0xyG07ZvZKPsw5KbK8Vw50eEUmz+8CjQKbwI41e/vcqh2vW3fguXDW4t1s
yWGXBg6gE24u3QQkFge74yLoFOHOYVMsIMe3nmrEeq/Q7xTVyI8W9j6HgoKyVkQA
HzzooIF9+d/ApTYNxzCNpDSCLA2rxQdNZ12DoGK+mwwRvkE8qgEJsdQI1TD9PE90
AYMrTrY9kgVl16COcSWu0THWFTB+SxcLiKCWOzcj24SuTS4oXQjWM7fEm5G/P00g
999Yyp0ZWGaBUlAadO/iusj8EMV5wU0Zkcw976jJhJRXzsY1Y+8xVoS2z2uOhOlt
g8er5omN++bic1DQ6zyaJquOASnBW0Mbf8yXIDjaxFRoFLgnPaNF0GtLNTNyzsqe
YI73w8t7nC3CCzDQM4JnONfgvulmTdYM0yMdzHClxD/cUSjy0AZ3xrEGhyrsbemp
N3uYQYbU1IhrtJj8WlhdJm3280kb1TneZrG95DKmnkSKyUW6O5gIGXmLE8nnbuRZ
/yowZVXSeMkpFCKcVxRnSQF8uDqtIm/SR966gnDSbnGF/9uGo36o3RWdBbqmvgqE
ag==
-----END CERTIFICATE-----""",
    org_name='built-in',
    application_name='ipv6'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(24),
    max_age=60 * 5,
)


app.include_router(sso.router())

offline.register_offline_openapi(app)


@app.get('/a')
async def get(user=Depends(sso.authenticate_user)):
    return user


if __name__ == '__main__':
    fastapix.run(app, port=1990, host="0.0.0.0")

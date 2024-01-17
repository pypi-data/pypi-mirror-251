import os
from inspect import signature

import fastapi
from starlette.websockets import WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi import FastAPI, Request, WebSocket, APIRouter
import sys
import time
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from toolboxv2 import tbef

from ..utils.state_system import get_state_from_app
from ..utils.toolbox import get_app

app = FastAPI()

origins = [
    "http://194.233.168.22:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://0.0.0.0",
    "http://localhost",
    "http://194.233.168.22",
    "https://simpelm.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # if response.body.get("info", {}).get("exec_code", 0) != 0:
    return response


@app.get("/")
async def index():
    return RedirectResponse(url="/app/core0/index.html")


@app.get("/favicon.ico")
async def index():
    return RedirectResponse(url="/app/favicon.ico")
    # return "Willkommen bei Simple V0 powered by ToolBoxV2-0.0.3"


# @app.get("/exit")
# async def exit_code():
#     tb_app.exit()
#     exit(0)


@app.websocket("/ws/{ws_id}")
async def websocket_endpoint(websocket: WebSocket, ws_id: str):
    websocket_id = ws_id
    print(f'websocket: {websocket_id}')
    if not await manager.connect(websocket, websocket_id):
        await websocket.close()
        return
    try:

        while True:
            try:
                data = await websocket.receive_text()
            except WebSocketDisconnect as e:
                print(e)
                break
            try:
                res = await manager.manage_data_flow(websocket, websocket_id, data)
                print("manage_data_flow")
            except Exception as e:
                print(e)
                res = '{"res": "error"}'
            if res is not None:
                print(f"RESPONSE: {res}")
                await websocket.send_text(res)
                print("Sending data to websocket")
            print("manager Don  ->")
    except Exception as e:
        print("websocket_endpoint - Exception: ", e)
    finally:
        await manager.disconnect(websocket, websocket_id)


print("API: ", __name__)  # https://www.youtube.com/watch?v=_Im4_3Z1NxQ watch NOW
if __name__ == 'toolboxv2.api.fast_api_main':

    config_file = ".config"
    id_name = ""
    for i in sys.argv[2:]:
        if i.startswith('data'):
            d = i.split(':')
            mods_list_len = d[1]
            id_name = d[2]
            config_file = id_name + config_file

    tb_app = get_app(from_="init-api", name=id_name)

    if "HotReload" in tb_app.id:
        @app.get("/HotReload")
        async def exit_code():
            if tb_app.debug:
                tb_app.remove_all_modules()
                tb_app.load_all_mods_in_file()
                return "OK"
            return "Not found"

    if id_name == tb_app.id:
        print("🟢 START")
    with open(f"./.data/api_pid_{id_name}", "w") as f:
        f.write(str(os.getpid()))
        f.close()

    tb_app.load_all_mods_in_file()
    tb_app.save_load("welcome")
    tb_app.save_load("WebSocketManager")
    manager = tb_app.get_mod("WebSocketManager")

    if "modInstaller" in tb_app.id:
        print("ModInstaller Init")
        from .fast_api_install import router as install_router

        cm = tb_app.get_mod("cloudM")
        all_mods = tb_app.get_all_mods()
        provider = os.environ.get("MOD_PROVIDER", default="http://127.0.0.1:5000/")
        tb_state = get_state_from_app(tb_app, simple_core_hub_url=provider)
        for mod_name in all_mods:
            ret = cm.save_mod_snapshot(mod_name, provider=provider, tb_state=tb_state)
            # app.get('/' + mod_name)(lambda: f"./installer/{mod_name}-installer.json")
        tb_func, error = tb_app.get_function(("cloudm.modmanager", "list_modules"), state=True, specification="app")

        if error == 0:
            install_router.add_api_route('/' + "cloudm.modmanager", tb_func, methods=["POST"],
                                         description="get all mods")
        app.include_router(install_router)
        app.get('/app/core0/index.html')(lambda: RedirectResponse(url="/docs"))

    else:

        from .fast_app import router as app_router
        from .fast_api import router as api_router

        app.include_router(app_router)
        app.include_router(api_router)

        for mod_name, functions in tb_app.functions.items():
            router = APIRouter(
                prefix=f"/api/{mod_name}",
                tags=["token", mod_name],
                # dependencies=[Depends(get_token_header)],
                # responses={404: {"description": "Not found"}},
            )
            # "type": type_,
            # "level": level,
            # "restrict_in_virtual_mode": restrict_in_virtual_mode,
            # "func": func,
            # "api": api,
            # "helper": helper,
            # "version": version,
            # "initial": initial,
            # "exit_f": exit_f,
            # "__module__": func.__module__,
            # "signature": sig,
            # "params": params,
            # "state": (False if len(params) == 0 else params[0] in ['self', 'state']) if state is None else state,
            # "do_test": test,
            # "samples": samples,

            for function_name, function_data in functions.items():
                if not isinstance(function_data, dict):
                    continue
                api: list = function_data.get('api')
                if api is False:
                    continue
                params: list = function_data.get('params')
                sig: signature = function_data.get('signature')
                state: bool = function_data.get('state')

                tb_func, error = tb_app.get_function((mod_name, function_name), state=state, specification="app")

                if tb_app.debug:
                    print(f"Loading fuction {function_name} , intern_error:{error}")

                if error != 0:
                    continue
                try:
                    if tb_func:
                        if len(params):
                            router.add_api_route('/' + function_name, tb_func, methods=["POST"],
                                                 description=function_data.get("helper", ""))
                        else:
                            router.add_api_route('/' + function_name, tb_func, methods=["GET"],
                                                 description=function_data.get("helper", ""))
                except fastapi.exceptions.FastAPIError as e:
                    raise SyntaxError(f"fuction '{function_name}' prove the signature error {e}")

            app.include_router(router)

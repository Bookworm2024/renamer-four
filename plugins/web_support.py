from aiohttp import web
from config import VERSION

trinity_routes = web.RouteTableDef()


@trinity_routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({
        "status": "running",
        "bot": "Trinity Mods · File Renamer",
        "version": VERSION,
    })


async def web_server():
    web_app = web.Application(client_max_size=50 * 1024 * 1024)
    web_app.add_routes(trinity_routes)
    return web_app

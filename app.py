from aiohttp import web
from canlib import canlib, Frame

ch = None


def open_channel(channel):
    global ch
    ch = canlib.openChannel(
        channel=channel,
        flags=canlib.Open.REQUIRE_INIT_ACCESS,
        bitrate=canlib.canBITRATE_125K,
    )
    ch.busOn()


def send_disconnect():
    f = Frame(id_=0x4FF, dlc=0, data=[])
    if ch is not None:
        ch.writeWait(f, 200)


async def handle(request):
    # Serve the video file
    filename = "harvest.webm"
    headers = {"Content-Type": "video/webm"}
    return web.FileResponse(filename, headers=headers)


async def index(request):
    # Serve the HTML page
    with open("index.html", "r") as file:
        html_content = file.read()
    return web.Response(text=html_content, content_type="text/html")


async def video_events_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        print("received:", msg)
        send_disconnect()

    return ws


async def javascript(request):
    # Serve the JavaScript file
    with open("script.js", "r") as file:
        js_content = file.read()
    return web.Response(text=js_content, content_type="application/javascript")


async def css(request):
    # Serve the CSS file
    with open("styles.css", "r") as file:
        css_content = file.read()
    return web.Response(text=css_content, content_type="text/css")


async def init():
    app = web.Application()
    app.router.add_get("/video", handle)
    app.router.add_get("/", index)
    app.router.add_get("/video-events", video_events_handler)
    app.router.add_get("/script.js", javascript)
    app.router.add_get("/styles.css", css)
    return app


if __name__ == "__main__":
    # Create the aiohttp app and run the server
    app = init()

    open_channel(1)

    web.run_app(app, port=8080)

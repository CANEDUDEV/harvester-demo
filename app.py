import binascii
import time

from aiohttp import web
from canlib import Frame, canlib

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


async def wait_for_connect():
    if ch is None:
        return False

    try:
        ch.iocontrol.flush_rx_buffer()
        ch.read(timeout=1000)
        print("received CAN message.")
        return True
    except canlib.exceptions.CanNoMsg:
        pass

    return False


def disable_car_controls():
    if ch is None:
        return

    disable_steering = Frame(id_=0x0, dlc=8, data=[4, 2, 0, 1, 0, 0, 0, 0])
    ch.write(disable_steering)
    disable_throttle = Frame(id_=0x0, dlc=8, data=[4, 2, 1, 1, 0, 0, 0, 0])
    ch.write(disable_throttle)


def enable_car_controls():
    if ch is None:
        return

    enable_steering = Frame(id_=0x0, dlc=8, data=[4, 2, 0, 1, 0, 0, 0, 1])
    ch.write(enable_steering)
    enable_throttle = Frame(id_=0x0, dlc=8, data=[4, 2, 1, 1, 0, 0, 0, 1])
    ch.write(enable_throttle)


async def get_airbridge_serial():
    if ch is None:
        return 0

    f = Frame(id_=0x500, dlc=8, data=[0x03, 0x02, 0xE0, 0x41])
    ch.iocontrol.flush_rx_buffer()
    ch.write(f)
    ch.readSyncSpecific(0x501, timeout=1000)
    received = ch.readSpecificSkip(0x501)
    serial = binascii.hexlify(received.data[5:]).decode()
    return serial


async def handle(request):
    # Serve the video file
    filename = "harvest.webm"
    headers = {"Content-Type": "video/webm"}
    return web.FileResponse(filename, headers=headers)


async def index(request):
    # Serve the HTML page
    with open("index.html", "r") as file:
        html_content = file.read()

    send_disconnect()

    return web.Response(text=html_content, content_type="text/html")


async def connection_event_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.data == "connect":
            connected = await wait_for_connect()
            if connected:
                disable_car_controls()
                await ws.send_str("connected")
            else:
                await ws.send_str("disconnected")

        if msg.data == "identify":
            serial = await get_airbridge_serial()
            await ws.send_str(f"identified:{serial}")

        if msg.data == "disconnect":
            try:
                enable_car_controls()
                send_disconnect()

            except canlib.exceptions.CanTimeout:
                print("Air bridge not connected, timed out.")

            finally:
                time.sleep(3)
                await ws.send_str("disconnected")

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
    app.router.add_get("/connection-events", connection_event_handler)
    app.router.add_get("/script.js", javascript)
    app.router.add_get("/styles.css", css)
    return app


if __name__ == "__main__":
    # Create the aiohttp app and run the server
    app = init()

    open_channel(1)

    web.run_app(app, port=8080)

# harvester-demo

This is a demo application for showcasing how grain carts can connect to a
combine harvester. The grain carts are emulated by 2 CanEduDev Rovers with an
Air Bridge each, configured in Master Mode. The combine harvester is
represented by a PC connected to an Air Bridge configured in Slave Mode.

## Quickstart

1. Install Kvaser drivers and CANlib. Install Python 3.11
2. Connect Air Bridge X to PC with a Kvaser CAN interface.
3. Run `pip install -r requirements.txt`
4. Run `python app.py` and connect to `127.0.0.1:8080` in your web browser.

## How it works
TODO

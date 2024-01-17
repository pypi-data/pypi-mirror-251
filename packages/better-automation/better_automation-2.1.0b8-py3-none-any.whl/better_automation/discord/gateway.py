from enum import IntEnum
import websocket

from .client import DiscordClient


class OPCODE(IntEnum):
    #                                    Client Action  Description
    DISPATCH =                      0  # Receive        dispatches an event
    HEARTBEAT =                     1  # Send/Receive   used for ping checking
    IDENTIFY =                      2  # Send           used for client handshake
    PRESENCE_UPDATE =               3  # Send           used to update the client status
    VOICE_STATE_UPDATE =            4  # Send           used to join/move/leave voice channels
    VOICE_SERVER_PING =             5  # Send           used for voice ping checking
    RESUME =                        6  # Send           used to resume a closed connection
    RECONNECT =                     7  # Receive        used to tell when to reconnect (sometimes...)
    REQUEST_GUILD_MEMBERS =         8  # Send           used to request guild members (when searching for members in the search bar of a guild)
    INVALID_SESSION =               9  # Receive        used to notify client they have an invalid session id
    HELLO =                        10  # Receive        sent immediately after connecting, contains heartbeat and server debug information
    HEARTBEAT_ACK =                11  # Sent           immediately following a client heartbeat that was received
    GUILD_SYNC =                   12  # Receive        guild_sync but not used anymore
    DM_UPDATE =                    13  # Send           used to get dm features
    LAZY_REQUEST =                 14  # Send           discord responds back with GUILD_MEMBER_LIST_UPDATE type SYNC...
    LOBBY_CONNECT =                15  # ??
    LOBBY_DISCONNECT =             16  # ??
    LOBBY_VOICE_STATES_UPDATE =    17  # Receive
    STREAM_CREATE =                18  # ??
    STREAM_DELETE =                19  # ??
    STREAM_WATCH =                 20  # ??
    STREAM_PING =                  21  # Send
    STREAM_SET_PAUSED =            22  # ??
    REQUEST_APPLICATION_COMMANDS = 24  # Send           request application/bot cmds (user, message, and slash cmds)


class DiscordGatewayServer:
    # API_VERSION = 9
    # WEBSOCKET_URL = f"wss://gateway.discord.gg/?encoding=json&compress=zlib-stream&v={API_VERSION}"
    DEFAULT_HEADERS = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    }

    def __init__(self, client: DiscordClient):
        self.rest_client = client

        # gateway
        auth = {
            "token": self.rest_client.account.auth_token,
            "capabilities": 509,
            "properties": self.rest_client.x_super_properties,
            "presence": {
                "status": "online",
                "since": 0,
                "activities": [],
                "afk": False
            },
            "compress": False,
            "client_state": {
                "guild_hashes": {},
                "highest_last_message_id": "0",
                "read_state_version": 0,
                "user_guild_settings_version": -1,
                "user_settings_version": -1
            }
        }
        self.keepData = ("guilds",)  # keep data even after leaving "dms", "guilds", or "guild_channels"
        self.interval = None
        self.session_id = None
        self.sequence = 0
        self.READY = False  # becomes True once READY_SUPPLEMENTAL is received

        headers = self.DEFAULT_HEADERS
        headers["User-Agent"] = self.rest_client.session.user_agent
        self.ws = websocket.WebSocketApp(
                f"wss://gateway.discord.gg/?encoding=json&compress=zlib-stream&v={self.rest_client.API_VERSION}",
                header=headers,
                on_open=lambda ws: self.on_open(ws),
                on_message=lambda ws, msg: self.on_message(ws, msg),
                on_error=lambda ws, msg: self.on_error(ws, msg),
                on_close=lambda ws, close_code, close_msg: self.on_close(ws, close_code,
                                                                         close_msg)
            )

        # discum: https://github.com/websocket-client/websocket-client/blob/master/websocket/_app.py#L84
        def _get_ws_app(self, websocketurl):
            headers = {
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
                "User-Agent": self.x_super_properties["browser_user_agent"]
            }  # more info: https://stackoverflow.com/a/40675547

            ws = websocket.WebSocketApp(
                websocketurl,
                header=headers,
                on_open=lambda ws: self.on_open(ws),
                on_message=lambda ws, msg: self.on_message(ws, msg),
                on_error=lambda ws, msg: self.on_error(ws, msg),
                on_close=lambda ws, close_code, close_msg: self.on_close(ws, close_code,
                                                                         close_msg)
            )
            return ws

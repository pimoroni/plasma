import network
import asyncio
from micropython import const


class LogLevel:
    INFO = const(0)
    WARNING = const(1)
    ERROR = const(2)

    text = ["info", "warning", "error"]


class EzWiFi:
    def __init__(self, **kwargs):
        get = kwargs.get

        self._last_error = None

        self._verbose = get("verbose", False)

        self._events = {
            "connected": get("connected", None),
            "failed": get("failed", None),
            "info": get("info", None),
            "warning": get("warning", None),
            "error": get("error", None)
        }

        self._if = network.WLAN(network.STA_IF)
        self._if.active(True)
        # self._if.config(pm=0xa11140) # TODO: ???
        self._statuses = {v: k[5:] for (k, v) in network.__dict__.items() if k.startswith("STAT_")}

    async def _callback(self, handler_name, *args, **kwargs):
        handler = self._events.get(handler_name, None)
        if callable(handler):
            # TODO: This is ugly, but we don't want to force users to supply async handlers
            if str(type(handler))[8:-2] == "generator":
                await handler(self, *args, **kwargs)
            else:
                handler(self, *args, **kwargs)
            return True
        return False

    async def _log(self, text, level=LogLevel.INFO):
        await self._callback(LogLevel.text[level], text) or (self._verbose and print(text))

    def on(self, handler_name, handler=None):
        if handler_name not in self._events.keys():
            raise ValueError(f"Invalid event: \"{handler_name}\"")

        def _on(handler):
            self._events[handler_name] = handler

        if handler is not None:
            _on(handler)
            return True

        return _on

    def error(self):
        if self._last_error is not None:
            return self._last_error, self._statuses[self._last_error]
        return None, None

    async def connect(self, ssid=None, password=None, timeout=60, retries=10):
        if not ssid and not password:
            ssid, password = self._secrets()
        elif password and not ssid:
            raise ValueError("ssid required!")

        for retry in range(retries):
            await self._log(f"Connecting to {ssid} (Attempt {retry + 1})")
            try:
                self._if.connect(ssid, password)
                if await asyncio.wait_for(self._wait_for_connection(), timeout):
                    return True

            except asyncio.TimeoutError:
                await self._log("Attempt failed...", LogLevel.WARNING)

        await self._callback("failed")
        return False

    async def disconnect(self):
        if self._if.isconnected():
            self._if.disconnect()

    async def _wait_for_connection(self):
        while not self._if.isconnected():
            await self._log("Connecting...")
            status = self._if.status()
            if status in [network.STAT_CONNECT_FAIL, network.STAT_NO_AP_FOUND, network.STAT_WRONG_PASSWORD]:
                await self._log(f"Connection failed with: {self._statuses[status]}", LogLevel.ERROR)
                self._last_error = status
                return False
            await asyncio.sleep_ms(1000)
        await self._log(f"Connected! IP: {self.ipv4()}")
        await self._callback("connected")
        return True

    def ipv4(self):
        return self._if.ipconfig("addr4")[0]

    def ipv6(self):
        return self._if.ipconfig("addr6")[0][0]

    def isconnected(self):
        return self._if.isconnected()

    def _secrets(self):
        try:
            from secrets import WIFI_SSID, WIFI_PASSWORD
            if not WIFI_SSID:
                raise ValueError("secrets.py: WIFI_SSID is empty!")
            return WIFI_SSID, WIFI_PASSWORD
        except ImportError:
            raise ImportError("secrets.py: missing or invalid!")


def connect(**kwargs):
    return asyncio.get_event_loop().run_until_complete(EzWiFi(**kwargs).connect(retries=kwargs.get("retries", 10)))

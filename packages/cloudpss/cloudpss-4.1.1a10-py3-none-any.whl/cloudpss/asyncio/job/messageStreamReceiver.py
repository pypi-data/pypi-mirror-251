import logging
from urllib.parse import urlparse

from aiohttp import WSMsgType
from cloudpss.asyncio.utils.httpAsyncRequest import websocket_connect
from cloudpss.job.messageStreamReceiver import MessageStreamReceiver
from cloudpss.utils.IO import IO


class MessageStreamReceiver(MessageStreamReceiver):
    async def connect(self):
        self._status = 0
        self.receiver= self.__receive(
            self.job.output,
            None,
        )
    
    async def __receive(self, id, fr0m):
        """
        读取消息流中的数据
        id: 消息流id
        fr0m: 从哪个位置开始读取，如果为0则从头开始读取
        on_open: 连接建立时的回调函数
        on_message: 收到消息时的回调函数
        on_error: 发生错误时的回调函数
        on_close: 连接关闭时的回调函数
        """
        if id is None:
            raise Exception("id is None")
        u = list(urlparse(self.origin))
        head = "wss" if u[0] == "https" else "ws"

        path = head + "://" + str(u[1]) + "/api/streams/id/" + id
        if fr0m is not None:
            path = path + "&from=" + str(fr0m)
        logging.info(f"MessageStreamReceiver data from websocket: {path}")
        async for msg in websocket_connect(
            path,
            open_func=self.__on_open,
        ):
            if msg.type == WSMsgType.BINARY:
                decode =await self.__on_message(msg.data)
                yield decode
            elif msg.type == WSMsgType.TEXT:
                decode =await self.__on_message(msg.data)
                yield decode
            elif msg.type == WSMsgType.CLOSED:
                logging.debug("WebSocket连接已关闭")
                self.__on_close()
                
                break
            elif msg.type == WSMsgType.ERROR:
                logging.debug(f"WebSocket连接发生错误：{msg.data}")
                self.__on_error(msg.data)
                break
        self._status=1
        
        
    async def close(self, ws):
        self._status = 1
        await ws.close()
    
    async def __on_message(self, message):
        
        data = IO.deserialize(message, "ubjson")
        msg = IO.deserialize(data["data"], "ubjson")
        self.messages.append(msg)
        # print(msg['type'])
        if(msg['type']=='terminate'):
            await self.close(self.ws)
        return msg
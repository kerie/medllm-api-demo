import asyncio
import websockets
import base64
import streamlit.proto.BackMsg_pb2
import streamlit.proto.WidgetStates_pb2
import streamlit.proto.ForwardMsg_pb2


WIDGET_ID = "$$WIDGET_ID-3b4d36b78df30224cebc74176fdd0182-None"

async def receiver(websocket):
    while True:
        try:
            message = await websocket.recv()
            forward_msg = streamlit.proto.ForwardMsg_pb2.ForwardMsg.FromString(message)
            text = forward_msg.delta.new_element.markdown.body
            # 除了ForwardMsg，ws还有其他消息，如果是其他消息，上面2行代码返回为空，空字符不做打印
            if (len(text)):
                print(f"Received: {text}")
        except Exception as e:
            print(e)

async def send(websocket, message):
    back_msg = streamlit.proto.BackMsg_pb2.BackMsg()
    widget_state = streamlit.proto.WidgetStates_pb2.WidgetState()
    widget_state.id = WIDGET_ID
    widget_state.string_trigger_value.data = message
    back_msg.rerun_script.widget_states.widgets.append(widget_state)

    question = back_msg.SerializeToString()
    print(f"Send: {message}")
    await websocket.send(question)


async def main():
    async with websockets.connect("ws://110.43.208.196:20047/_stcore/stream") as websocket:
        asyncio.create_task(receiver(websocket))

        # 建立websocket后，初始化消息
        init_msg = base64.b64decode("WggKABIAGgAiAA==")
        await websocket.send(init_msg)

        # 等待第一个问题的回答
        await send(websocket, "鼻炎怎么办？")
        await asyncio.sleep(20)

        # 等待第二个问题的回答
        await send(websocket, "有什么药可以用吗？")
        await asyncio.sleep(20)

asyncio.run(main())

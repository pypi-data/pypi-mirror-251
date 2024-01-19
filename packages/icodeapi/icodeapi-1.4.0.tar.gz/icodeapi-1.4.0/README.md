## icodeapi, the The second generation of IcodeYoudao API framework.  
**More Powerful and Faster than [TuringAPI](https://github.com/xbzstudio/TuringAPI) and TuringIO.**  
icodeapi is easy to use, and it supports for sync and async.  
```python
from icodeapi import *
import asyncio
cookie = input('Enter cookie: ')
syncAPI = IcodeAPI(cookie = cookie)
print(syncAPI.updateIntro('hello, icodeapi!'))
asyncAPI = AsyncIcodeAPI(cookie = cookie)

async def main(api : AsyncIcodeAPI):
    await api.login()
    print(await api.updateIntro('hello, async icodeapi!'))
    await api.closeClient()

asyncio.run(main(asyncAPI))
```  
Use icodeapi to build your server  
```python
import icodeapi
from icodeapi import server
cookie = input("Enter cookie: ")
api = icodeapi.AsyncIcodeAPI(cookie = cookie)
Server = server.IcodeServer(api = api)
@Server.CheckMessage()
async def AutoReply(userId, bot):
    try:
        await bot.fastReply(userId, 'Hello world!')
    except AssertionError:
        pass
    except:
        print('Unknown Error')
server.RunServer(Server)
```  
Use pip to install  
```
pip install icodeapi
```  
[Documentation](https://xbzstudio.github.io/icodeapi/docs)  
[Github](https://github.com/xbzstudio/icodeapi)
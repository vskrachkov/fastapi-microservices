import httpx
from fastapi import Request, FastAPI
from fastapi.responses import StreamingResponse
from httpx import AsyncClient
from starlette.background import BackgroundTask

application = FastAPI()


@application.get("/hello-service/say-hello")
async def reverse_proxy(request: Request) -> StreamingResponse:
    return await proxy_request(request, "http://hello-service", "/hello")


async def proxy_request(request: Request, host: str, path: str) -> StreamingResponse:
    url = httpx.URL(path=path, query=request.url.query.encode("utf-8"))
    async with AsyncClient(base_url=host) as http:
        rp_req = http.build_request(
            request.method,
            url,
            headers=request.headers.raw,
            content=await request.body(),
        )
        rp_resp = await http.send(rp_req, stream=True)
        return StreamingResponse(
            rp_resp.aiter_raw(),
            status_code=rp_resp.status_code,
            headers=rp_resp.headers,
            background=BackgroundTask(rp_resp.aclose),
        )

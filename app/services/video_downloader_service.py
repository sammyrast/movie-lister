"""Download the video lists from API , clean it up and made it ready to be inserted to DB."""

from typing import Optional
import httpx


# i don't think i needed this but let us keep it for now.
api_key: Optional[str] = None


API_URL = "https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json"


async def get_videos():
    """Makes a request to download the video lists from the external API."""
    async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(API_URL)
            if resp.status_code != 200:
                print( {"message": f"HTTP error looks like API is not available let's get data from db.{resp.status_code}"})
                
            else:
                return resp.json()
        




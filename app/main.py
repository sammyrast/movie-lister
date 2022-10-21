"""Main application entry point file for the app. """
import httpx
from typing import List, Optional
from fastapi.responses import HTMLResponse

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse

from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, Request
# Decided to use sqlmodel since I get the best of both the Pydantic and SQLAlchemy world at once. 
from sqlmodel import Field, SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from services import video_downloader_service

templates = Jinja2Templates(directory="templates")


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    iconUri: str = Field(index=True) 
    shortName: Optional[str] = None
    manifestUri: Optional[str] = None
    source: Optional[str] = None
    focus: Optional[bool] = False
    disabled: Optional[bool] = False
    certificateUri: Optional[str] = None
    description: Optional[str] = None
    isFeatured: Optional[bool] = False
    requestFilter: Optional[str] = None 
    responseFilter: Optional[str] = None 
    extraConfig: Optional[str] = None 
    adTagUri: Optional[str] = None
    imaVideoId: Optional[str] = None
    imaAssetKey:Optional[str] = None
    imaContentSrcId: Optional[str] = None
    mimeType: Optional[str] = None
    mediaPlaylistFullMimeType: Optional[str] = None
    storedProgress: Optional[int] = None

# FIXME NOT GOOD 
DATABSAE_URL = "postgresql+asyncpg://postgres:postgres@postgres/postgres"

async_engine = create_async_engine(DATABSAE_URL, echo=True)

async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.get("/videos/")
async def read_videos():
    """Retrieve the video items from database."""
    async with async_session() as session:
        result = await session.execute(select(Video))
        videos = result.all()
        return videos
    

@app.get("/", response_class=HTMLResponse)
async def external_videos(request: Request):
    """Retrieves all videos available from the external API."""

    video : Video = await video_downloader_service.get_videos()
    if video is not None: 
        for vid in video:
            data = Video(**vid)
            async with async_session() as session:
                session.add(data)
                await session.commit()  

        json_compatible_data = jsonable_encoder(video)
        return templates.TemplateResponse("index.html", {"request": request, "data": json_compatible_data})
    elif video is None:
        # in this case we need to get the data from db.
       async with async_session() as session:
        result = await session.execute(select(Video))
        videos = result.all() 
        json_compatible_data = jsonable_encoder(videos)
        return templates.TemplateResponse("index.html", {"request": request, "data": json_compatible_data})


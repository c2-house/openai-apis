from contextlib import asynccontextmanager
from fastapi import FastAPI
from supabase import create_client, Client
from supabase.client import SupabaseException
from app.core.config import settings


supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield {"supabase": supabase}
    except SupabaseException as e:
        raise e

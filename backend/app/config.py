import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

print(SUPABASE_URL)
print(SUPABASE_KEY)
print("-----------  ------------")
print(os.getenv("NEXT_PUBLIC_SUPABASE_URL"))
print(os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"))

# Shared Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
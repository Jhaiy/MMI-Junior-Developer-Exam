from supabase import create_client
from common.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def scan(column_name):
  response = (
    supabase
    .table("pokemon-ocr")
    .select("id, filepath, " + column_name)
    .is_(column_name, "null" or "")
    .limit(1)
    .execute()
  )

  return response.data

def get_card_image(card_id, category):
  response = (
    supabase
    .table("pokemon-ocr")
    .select(category)
    .eq("id", card_id)
    .execute()
  )

  return response.data
 
def get_card(card_id):
  response = (
    supabase.table("pokemon-ocr")
    .select("*")
    .eq("id", card_id)
    .single()
    .execute()
  )

  return response.data

def fetch_card_ids():
  response = (
    supabase
    .table("pokemon-ocr")
    .select("id")
    .execute()
  )

  return response.data

def update_card(card_id, data):
  return (
    supabase
    .table("pokemon-ocr")
    .update(data)
    .eq("id", card_id)
    .execute()
  )


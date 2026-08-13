from supabase import create_client
from common.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_card(card_id):
  response = (supabase.table("pokemon-ocr")
              .select("*")
              .eq("id", card_id)
              .single()
              .execute()
            )

  return response.data

def update_card(card_id, data):
  return (supabase
          .table("pokemon-ocr")
          .update(data)
          .eq("id", card_id)
          .execute()
        )


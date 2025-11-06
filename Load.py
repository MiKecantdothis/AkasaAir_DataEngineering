import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client


class Load:
    def __init__(self):
        load_dotenv()
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        # Store the supabase client on the instance
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    def chunk_upload(self, table, df, size=500):

        # ✅ Ensure df is actually a dataframe
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Expected DataFrame, got {type(df)} instead.")

        for i in range(0, len(df), size):
            chunk = df.iloc[i:i + size].copy()

            # Convert datetime columns
            for col in chunk.columns:
                if str(chunk[col].dtype).startswith("datetime64"):
                    chunk[col] = chunk[col].apply(
                        lambda x: x.strftime("%Y-%m-%dT%H:%M:%SZ") if pd.notnull(x) else None
                    )

            # Convert NaN to None
            chunk = chunk.where(pd.notnull(chunk), None)

            # Convert Timestamp objects
            for col in chunk.columns:
                chunk[col] = chunk[col].apply(
                    lambda v: v.isoformat() if isinstance(v, pd.Timestamp) else v
                )

            records = chunk.to_dict(orient="records")

            print("UPLOADING CHUNK SAMPLE:", records[:1])

            self.supabase.table(table).upsert(records).execute()

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

from app import routes
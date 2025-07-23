# Entrypoint for API server, delegates to model.api FastAPI app
from model.api import app

# Optionally, you can add CORS middleware here if you want to override or extend the CORS settings from model.api
# But model.api already sets up CORS for all origins.
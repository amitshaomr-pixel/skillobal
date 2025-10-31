class Settings:
    ALLOW_ORIGINS = ["*"]  # change to ["https://your-frontend.com"] in prod
    ALLOW_CREDENTIALS = True
    ALLOW_METHODS = ["*"]
    ALLOW_HEADERS = ["*"]

settings = Settings()

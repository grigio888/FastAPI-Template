"""
Application settings module.
"""

from decouple import config


class Settings:
    """
    Application settings.
    """

    # -- Configuration variables --
    PATH_IMAGE_USER: str = config("PATH_IMAGE_USER", cast=str)
    PAGE_SIZE: int = config("PAGE_SIZE", cast=int, default=10)

    # -- Application variables --
    APP_NAME: str = config("APP_NAME", default="MangaGr.id", cast=str)
    APP_VERSION: str = config("APP_VERSION", default="0.0.1", cast=str)
    APP_URL: str = config("APP_URL", default="http://localhost:8000", cast=str)

    ASYNC_SCRAPING_ENABLE: bool = config(
        "ASYNC_SCRAPING_ENABLE",
        default=False,
        cast=bool,
    )
    ASYNC_SCRAPING_MAX_WORKERS: int = config(
        "ASYNC_SCRAPING_MAX_WORKERS",
        default=2,
        cast=int,
    )

    MANGAS_CACHE_KEY: str = config(
        "MANGAS_CACHE_KEY",
        default="mangas_list_key",
        cast=str,
    )
    MANGAS_CACHE_EXPIRE_SECONDS: int = config(
        "MANGAS_CACHE_EXPIRE_SECONDS",
        default=3600,  # 1 hour
        cast=int,
    )

    MANGAS_HIGHLIGHTS_CACHE_KEY: str = config(
        "MANGAS_HIGHLIGHTS_CACHE_KEY",
        default="mangas_highlights_list_key",
        cast=str,
    )
    MANGAS_HIGHLIGHTS_CACHE_EXPIRE_SECONDS: int = config(
        "MANGAS_HIGHLIGHTS_CACHE_EXPIRE_SECONDS",
        default=3600,  # 1 hour
        cast=int,
    )

    MANGA_CHAPTERS_CACHE_KEY: str = config(
        "MANGA_CHAPTERS_CACHE_KEY",
        default="manga_chapters_list_key",
        cast=str,
    )
    MANGA_CHAPTERS_CACHE_EXPIRE_SECONDS: int = config(
        "MANGA_CHAPTERS_CACHE_EXPIRE_SECONDS",
        default=3600,  # 1 hour
        cast=int,
    )

    MANGA_CHAPTER_CHACHE_KEY: str = config(
        "MANGA_CHAPTER_CHACHE_KEY",
        default="manga_chapter_key",
        cast=str,
    )
    MANGA_CHAPTER_CACHE_EXPIRE_SECONDS: int = config(
        "MANGA_CHAPTER_CACHE_EXPIRE_SECONDS",
        default=3600,  # 1 hour
        cast=int,
    )

    # -- Email variables --
    EMAIL_USER: str = config("EMAIL_USER")
    EMAIL_PASS: str = config("EMAIL_PASS")
    EMAIL_TEMPLATE_DIR: str = config(
        "EMAIL_TEMPLATE_DIR",
        default="src/libs/email/templates",
        cast=str,
    )
    SMTP_HOST: str = config("SMTP_HOST")
    SMTP_PORT: int = config("SMTP_PORT", cast=int)
    IMAP_HOST: str = config("IMAP_HOST")
    IMAP_PORT: int = config("IMAP_PORT", cast=int)

    # -- JWT variables --
    SECRET_KEY: str = config("SECRET_KEY", default="")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    EXCLUDED_PATHS: list[str] = config(
        "EXCLUDED_PATHS",
        default="",
        cast=lambda x: x.split(","),
    )
    AUTH_SERVICE_URL: str = config("AUTH_SERVICE_URL", default="")
    AUTH_VERIFY_ENDPOINT: str = config(
        "AUTH_VERIFY_ENDPOINT",
        default="v1/token/validate",
    )

    TOKEN_ACCESS_UNIT: str = config("ACCESS_UNIT", default="hours", cast=str)
    TOKEN_ACCESS_VALUE: int = config("ACCESS_VALUE", default=1, cast=int)
    TOKEN_REFRESH_UNIT: str = config("REFRESH_UNIT", default="days", cast=str)
    TOKEN_REFRESH_VALUE: int = config("REFRESH_VALUE", default=7, cast=int)

    # -- CORS variables --
    CORS_ALLOWED_ORIGINS: list[str] = config(
        "ALLOWED_ORIGINS",
        default="*",
        cast=lambda x: [origin.strip() for origin in x.split(",")],
    )  # type: ignore[assignment]
    CORS_ALLOWED_METHODS: list[str] = config(
        "ALLOWED_METHODS",
        default="*",
        cast=lambda x: [method.strip() for method in x.split(",")],
    )  # type: ignore[assignment]
    CORS_ALLOWED_HEADERS: list[str] = config(
        "ALLOWED_HEADERS",
        default="*",
        cast=lambda x: [header.strip() for header in x.split(",")],
    )  # type: ignore[assignment]
    CORS_ALLOWED_CREDENTIALS: bool = config(
        "ALLOW_CREDENTIALS",
        default=True,
        cast=bool,
    )

    # -- Database variables --
    DB_DIALECT: str = config("DB_DIALECT", cast=str)
    DB_USER: str = config("DB_USER", cast=str)
    DB_PASS: str = config("DB_PASS", cast=str)
    DB_HOST: str = config("DB_HOST", cast=str)
    DB_NAME: str = config("DB_NAME", cast=str)

    # -- Logging variables --
    LOG_THRESHOLD_UNIT: str = config("LOG_THRESHOLD_UNIT", default="minutes", cast=str)
    LOG_THRESHOLD_VALUE: int = config("LOG_THRESHOLD_VALUE", default=1, cast=int)
    LOG_LEVEL: str = config("LOG_LEVEL", default="DEBUG", cast=str)
    LOG_FORMAT: str = config(
        "LOG_FORMAT",
        default="[%(asctime)s - %(levelname)s] %(name)s %(message)s",
    )
    LOG_NAME: str = config("LOG_NAME", default="backend")

    # -- Redis variables --
    REDIS_HOST: str = config("REDIS_HOST", cast=str)
    REDIS_PORT: int = config("REDIS_PORT", cast=int)
    REDIS_DB: int = config("REDIS_DB", cast=int)
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    # -- File Paths variables --
    DEFAULT_COVER_PATH: str = config(
        "DEFAULT_COVER_PATH",
        default="/static/manga/no_cover.webp",
        cast=str,
    )

    MANGA_UPLOAD_FOLDER: str = config(
        "MANGA_UPLOAD_FOLDER",
        default="/static/manga",
        cast=str,
    )

    BLOG_UPLOAD_FOLDER: str = config(
        "BLOG_UPLOAD_FOLDER",
        default="/static/blog",
        cast=str,
    )

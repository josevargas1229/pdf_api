from databases import Database
from app.core.config import settings
from urllib.parse import urlparse, quote_plus, urlunparse

db = None
if hasattr(settings, "DATABASE_URL") and settings.DATABASE_URL:
    parsed_url = urlparse(settings.DATABASE_URL)
    
    # Si la contraseña tiene caracteres especiales (como #, &), los codificamos
    if parsed_url.password:
        encoded_password = quote_plus(parsed_url.password)
        
        # Reconstruir la parte "user:password@hostname:port"
        netloc = f"{parsed_url.username}:{encoded_password}@{parsed_url.hostname}"
        if parsed_url.port:
            netloc += f":{parsed_url.port}"
            
        # Generar la nueva URL segura
        safe_url = urlunparse((
            parsed_url.scheme,
            netloc,
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment,
        ))
        db = Database(safe_url)
    else:
        db = Database(settings.DATABASE_URL)

from .services.hello import HelloService
from .services.whisper import WhisperService

def load_services():
    services = []

    # Register all services here
    print("Loading services...")
    services.append(HelloService())
    services.append(WhisperService())

    # Preload services
    for service in services:
        service.preload()

    return services
from .services.hello import HelloService

def load_services():
    services = []

    # Register all services here
    print("Loading services...")
    services.append(HelloService())

    # Preload services
    for service in services:
        service.preload()

    return services
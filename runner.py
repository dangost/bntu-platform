import waitress
from dotenv import load_dotenv

from src import Config
from src.app import create_app


def main():
    load_dotenv()
    config = Config()
    app = create_app(config)
    protocol = "http"
    app.config.logger.log(f"Server started at {protocol}://{config.server_config.host}:{config.server_config.port}")
    waitress.serve(
        app,
        host=config.server_config.host,
        port=config.server_config.port,
        threads=config.server_config.workers
    )


if __name__ == "__main__":
    main()

from application import Application
from data_processing.fabrics import Sources_factory, Handler_factory
from config import AppConfig
from data_processing.parser import Demo_parser

def main():
    conf = AppConfig()

    handler = Handler_factory.get_handler(
        conf.handler_type,
        **conf.handler_param,
    )

    sources = (
        Sources_factory.get_source(**src_conf)
        for src_conf in conf.get_sources()
    )

    app = Application(sources, handler)
    app.run()

if __name__ == "__main__":
    main()

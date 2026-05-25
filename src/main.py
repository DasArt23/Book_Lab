from application import Application
from data_processing.fabrics import Sources_factory, Handler_factory
from config import AppConfig, ExecutionMode
import asyncio


def main():
    conf = AppConfig()
    handler = Handler_factory.get_handler(conf.handler_type, **conf.handler_param)
    sources = [Sources_factory.get_source(**src_conf) for src_conf in conf.get_sources()]
    app = Application(sources, handler)

    if conf.is_async_mode:
        asyncio.run(app.run_async())
    elif conf.execution_mode in [ExecutionMode.THREAD, ExecutionMode.PROCESS]:
        asyncio.run(app.run_hybrid())
    else:
        app.run()

    return app


if __name__ == "__main__":
    main()

from application import Application
from data_processing.source import Demo_source, Rand_source, FileJSON_source
from data_processing.engine import Text_handler

def main():
    sources = [
        FileJSON_source("json_files/proba.json"),
        Demo_source(),
        Rand_source(amount=6),
        #Rand_source(amount=8),
        #FileJSON_source("json_files/good.json"),
    ]
    handler = Text_handler()
    app = Application(sources, handler)
    app.run()

if __name__ == "__main__":
    main()

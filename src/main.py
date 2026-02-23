from application import Application
from data_processing.source import Demo_source, Rand_source, FileJSON_source
from data_processing.engine import Books_handler

def main():
    sources = [
        FileJSON_source("json_files/proba.json"),
        Demo_source(),
        Rand_source(amount=6),
        #Rand_source(amount=8, title_len=14),
        #FileJSON_source("json_files/good.json"),
    ]
    handler = Books_handler()
    app = Application(sources, handler)
    app.run()

if __name__ == "__main__":
    main()

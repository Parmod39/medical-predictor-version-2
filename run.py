from pywebio import start_server
from app import DiseasePredictorApp

if __name__ == '__main__':
    app = DiseasePredictorApp()
    start_server(app.run, port=8081, debug=True)
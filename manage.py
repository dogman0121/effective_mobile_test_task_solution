from effective_mobile_task import create_app
from config import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
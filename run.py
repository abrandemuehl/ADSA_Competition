#!flask/bin/python
from app import app, socketio

if __name__ == "__main__":
    app.run()
    # socketio.run(app, host='0.0.0.0', port=5000)

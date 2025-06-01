import webview
from tracker import app
import threading


def run_server():
    """Run the Flask server in a separate thread"""
    app.run(port=5000)


def main():
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()

    window = webview.create_window(
        "Work Tracker",
        "http://localhost:5000",
        width=1024,
        height=768,
        resizable=True,
        min_size=(800, 600),
    )

    webview.start(debug=True)


if __name__ == "__main__":
    main()

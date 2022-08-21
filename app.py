from dashboard.content import app

# Imports and assembles everything dashboard/content.py
sever = app.server

if __name__ == "__main__":
    app.run_server(debug = True)

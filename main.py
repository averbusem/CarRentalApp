from gui.mainApp import App
from db.initialize_db import initialize_db
initialize_db()
app = App()
app.loop()

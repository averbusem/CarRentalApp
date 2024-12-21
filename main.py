from db.initialize_db import initialize_db
from gui.mainApp import App

initialize_db()
app = App()
app.loop()

from dotenv import load_dotenv
from backend.app import create_app, db
import os

load_dotenv()
app = create_app()

# Criar o banco de dados se não existir
with app.app_context():
    if not os.path.exists('database/app.db'):
        db.create_all()
        print("Banco de dados criado com sucesso!")

if __name__ == '__main__':
    app.run(debug=True)
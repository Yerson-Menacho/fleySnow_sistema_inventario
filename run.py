from app import create_app

app = create_app()


def index():
    return "¡Sistema de inventario funcionando correctamente!"

if __name__ == "__main__":
    app.run(debug=True)

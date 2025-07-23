## PRPs/ai_docs/flask.md

### Flask Web Framework Documentation

- **Overview**: Flask is a lightweight WSGI web application framework for building APIs and servers.
- **Key Features**:
  - app = Flask(__name__): Initializes the app.
  - @app.route('/path', methods=['POST']): Defines endpoints.
  - request.json: Parses JSON inputs.
- **Best Practices**: Use blueprints for modularity; implement error handlers.
- **Gotchas**: Default to development mode; secure with API keys for production.
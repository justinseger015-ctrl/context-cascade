#!/usr/bin/env python3
"""
Export OpenAPI schema to static HTML for offline viewing
Generates Swagger UI and ReDoc HTML files
"""

import json
import os
from pathlib import Path

# HTML template for Swagger UI
SWAGGER_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RUV SPARC API Documentation - Swagger UI</title>
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
  <style>
    body {{
      margin: 0;
      padding: 0;
    }}
    .topbar {{
      background-color: #2c3e50;
    }}
    .topbar .download-url-wrapper {{
      display: none;
    }}
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = function() {{
      const spec = {spec_json};

      window.ui = SwaggerUIBundle({{
        spec: spec,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout",
        syntaxHighlight: {{
          theme: "monokai"
        }},
        defaultModelsExpandDepth: 3,
        defaultModelExpandDepth: 3,
        displayRequestDuration: true,
        filter: true,
        persistAuthorization: true
      }});
    }};
  </script>
</body>
</html>
"""

# HTML template for ReDoc
REDOC_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RUV SPARC API Documentation - ReDoc</title>
  <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
  <style>
    body {{
      margin: 0;
      padding: 0;
    }}
  </style>
</head>
<body>
  <div id="redoc"></div>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
  <script>
    const spec = {spec_json};

    Redoc.init(spec, {{
      scrollYOffset: 50,
      hideDownloadButton: false,
      theme: {{
        colors: {{
          primary: {{
            main: '#2c3e50'
          }}
        }},
        typography: {{
          fontFamily: 'Roboto, sans-serif',
          headings: {{
            fontFamily: 'Montserrat, sans-serif'
          }}
        }}
      }}
    }}, document.getElementById('redoc'));
  </script>
</body>
</html>
"""

def fetch_openapi_schema():
    """
    Fetch OpenAPI schema from running FastAPI server
    Falls back to generating from app if server not running
    """
    import requests
    import sys

    try:
        # Try to fetch from running server
        response = requests.get("http://localhost:8000/api/openapi.json", timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, Exception):
        # Fallback: generate from app
        print("Server not running, generating schema from app...")

        # Add backend directory to Python path
        backend_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(backend_dir))

        try:
            from app.main import app
            return app.openapi()
        except ImportError as e:
            print(f"❌ Failed to import app: {e}")
            print("⚠️  Please start the server first: uvicorn app.main:app --reload")
            print("   Then run this script again.")
            sys.exit(1)

def export_html(output_dir: Path):
    """
    Export OpenAPI schema to static HTML files

    Args:
        output_dir: Directory to save HTML files
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch OpenAPI schema
    print("Fetching OpenAPI schema...")
    spec = fetch_openapi_schema()

    # Save raw OpenAPI JSON
    json_path = output_dir / "openapi.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    print(f"✅ Saved OpenAPI JSON: {json_path}")

    # Generate Swagger UI HTML
    swagger_html = SWAGGER_HTML_TEMPLATE.format(
        spec_json=json.dumps(spec, indent=2)
    )
    swagger_path = output_dir / "swagger-ui.html"
    with open(swagger_path, "w", encoding="utf-8") as f:
        f.write(swagger_html)
    print(f"✅ Saved Swagger UI: {swagger_path}")

    # Generate ReDoc HTML
    redoc_html = REDOC_HTML_TEMPLATE.format(
        spec_json=json.dumps(spec, indent=2)
    )
    redoc_path = output_dir / "redoc.html"
    with open(redoc_path, "w", encoding="utf-8") as f:
        f.write(redoc_html)
    print(f"✅ Saved ReDoc: {redoc_path}")

    print(f"\n📦 Static HTML documentation exported to: {output_dir.absolute()}")
    print(f"\n🌐 Open in browser:")
    print(f"   Swagger UI: file://{swagger_path.absolute()}")
    print(f"   ReDoc:      file://{redoc_path.absolute()}")

if __name__ == "__main__":
    # Export to docs/api-static/
    backend_dir = Path(__file__).parent.parent
    output_dir = backend_dir / "docs" / "api-static"

    export_html(output_dir)

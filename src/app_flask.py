#!/usr/bin/env python3
"""
Flask wrapper for deployment
This file serves as the main entry point for production deployment
"""

import os
import sys
from flask import Flask, redirect, jsonify
from datetime import datetime
import subprocess
import threading
import time

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-production')

# Global variable to track Streamlit process
streamlit_process = None
streamlit_port = 8501

@app.route('/')
def index():
    """Redirect to Streamlit app or show status"""
    # Check if running in production (Railway/Heroku)
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('DYNO'):
        # In production, return instructions
        return """
        <html>
        <head>
            <title>Sistema de Verificação - IN SEGES 65/2021</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 { color: #1e3a8a; }
                .info { 
                    background: #e0f2fe; 
                    padding: 15px; 
                    border-radius: 5px;
                    margin: 20px 0;
                }
                .button {
                    display: inline-block;
                    background: #3b82f6;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                }
                code {
                    background: #f3f4f6;
                    padding: 2px 5px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Sistema de Verificação Automática</h1>
                <h2>IN SEGES nº 65/2021</h2>
                
                <div class="info">
                    <p><strong>✅ Sistema implantado com sucesso!</strong></p>
                    <p>Para executar o sistema completo com interface Streamlit, use:</p>
                    <code>streamlit run src/app.py</code>
                </div>
                
                <h3>📌 Configuração Railway</h3>
                <p>Para executar o Streamlit no Railway, adicione estas variáveis:</p>
                <ul>
                    <li><code>RAILWAY_RUN_CMD = streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0</code></li>
                    <li><code>GEMINI_API_KEY = sua_chave_aqui</code></li>
                </ul>
                
                <h3>🔧 Endpoints da API</h3>
                <ul>
                    <li><code>GET /api/status</code> - Status do sistema</li>
                    <li><code>GET /api/health</code> - Health check</li>
                </ul>
                
                <a href="/api/status" class="button">Ver Status da API</a>
            </div>
        </body>
        </html>
        """
    else:
        # In development, redirect to Streamlit
        return redirect(f'http://localhost:{streamlit_port}')

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    try:
        import config
        return jsonify({
            'status': 'online',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'environment': os.environ.get('ENVIRONMENT', 'development'),
            'security_enabled': hasattr(config, 'SECURITY_ENABLED') and config.SECURITY_ENABLED,
            'ai_enabled': bool(os.environ.get('GEMINI_API_KEY'))
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

def start_streamlit():
    """Start Streamlit app in background (development only)"""
    global streamlit_process
    if not os.environ.get('RAILWAY_ENVIRONMENT') and not os.environ.get('DYNO'):
        try:
            # Kill any existing Streamlit process
            if sys.platform == "win32":
                subprocess.run(['taskkill', '/F', '/IM', 'streamlit.exe'], capture_output=True)
            else:
                subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True)
            
            # Start new Streamlit process
            cmd = [sys.executable, '-m', 'streamlit', 'run', 'app.py', 
                   '--server.port', str(streamlit_port),
                   '--server.address', 'localhost']
            
            streamlit_process = subprocess.Popen(cmd, cwd=os.path.dirname(__file__))
            
            # Wait for Streamlit to start
            time.sleep(3)
            
        except Exception as e:
            print(f"Failed to start Streamlit: {e}")

if __name__ == '__main__':
    # Start Streamlit in development
    if not os.environ.get('RAILWAY_ENVIRONMENT') and not os.environ.get('DYNO'):
        streamlit_thread = threading.Thread(target=start_streamlit)
        streamlit_thread.daemon = True
        streamlit_thread.start()
    
    # Get port from environment or default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('ENVIRONMENT', 'development') == 'development'
    
    # Run Flask app
    app.run(debug=debug, host='0.0.0.0', port=port) 
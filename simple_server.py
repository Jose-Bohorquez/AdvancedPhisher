#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor simple para mostrar templates
"""

from flask import Flask, render_template, request
import os
from pathlib import Path

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('facebook.html')

@app.route('/facebook')
def facebook():
    return render_template('facebook.html')

@app.route('/google')
def google():
    return render_template('google.html')

@app.route('/instagram')
def instagram():
    return render_template('instagram.html')

@app.route('/microsoft')
def microsoft():
    return render_template('microsoft.html')

if __name__ == '__main__':
    print("Servidor iniciado en http://localhost:5000")
    print("Templates disponibles:")
    print("- Facebook: http://localhost:5000/facebook")
    print("- Google: http://localhost:5000/google")
    print("- Instagram: http://localhost:5000/instagram")
    print("- Microsoft: http://localhost:5000/microsoft")
    app.run(debug=True, host='0.0.0.0', port=5000)
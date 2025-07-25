from flask import Flask, render_template, request, redirect, url_for, session
import os
import re

app = Flask(__name__, template_folder='web/templates')

def is_xss(input_text):
    # Basic blacklist-based detection
    pattern = re.compile(r"<.*?>|script|onerror|onload|alert", re.IGNORECASE)
    return bool(pattern.search(input_text))

def is_sql_injection(input_text):
    # Look for common SQLi patterns
    pattern = re.compile(r"('|--|\b(OR|AND|SELECT|DROP|INSERT|DELETE|UPDATE|UNION)\b)", re.IGNORECASE)
    return bool(pattern.search(input_text))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        term = request.form.get('search_term', '')

        if is_xss(term):
            return render_template('home.html', error="Possible XSS attack detected. Input cleared.", search_term='')
        elif is_sql_injection(term):
            return render_template('home.html', error="Possible SQL Injection detected. Input cleared.", search_term='')
        else:
            return redirect(url_for('result', term=term))
    return render_template('home.html')

@app.route('/result')
def result():
    term = request.args.get('term', '')
    print(f"[DEBUG] Term = {term}")
    return render_template('result.html', term=term)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)

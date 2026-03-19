from flask_blog import app

if __name__ == '__main__':
    app.run(debug=True)
    # This condition ensures that the Flask development server runs only when the script is executed directly. 
    # The debug mode allows automatic reload when code changes and provides detailed error messages.
```python
pip install "python-jose[cryptography]" "passlib[bcrypt]" 
```

OAuth2PasswordBearer takes two required parameters. tokenUrl is the URL in your application that handles user login and return tokens. scheme_name set to JWT will allow the frontend swagger docs to call tokenUrl from the frontend and save tokens in memory. Then each subsequent request to the protected endpoints will have the token sent as Authorization headers so OAuth2PasswordBearer can parse it.
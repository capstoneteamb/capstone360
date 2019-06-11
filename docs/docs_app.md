# App .py CAS config and Port numbering

### function create_app

To change the CAS Server, modify this code with the new server address:
```
app.config['CAS_SERVER'] = 'https://auth.cecs.pdx.edu/cas/login'
```i

To change the route of login and logout for CAS, change the code before for either login or logout

```
   app.config['CAS_AFTER_LOGIN'] = 'dashboard'
   app.config['CAS_AFTER_LOGOUT'] = 'logout'
```

When running locally, port number can be changed in this piece of code:
```
if __name__ == '__main__':
   app = create_app(debug=True)
   app.run(host='0.0.0.0', port=8000)
```
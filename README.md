# capstone360

### After Flask-CAS Implementation
To log in using your CAT credentials you have to add your cat CAS username as the id into the student database with session_id of 0.  Other columns can be any value.

### Note for Flask-CAS extension to work
Modify routing.py in the Flask-CAS extension folder.
Comment out line 125 and add line of code below.
```python
125     #attributes = xml_from_dict["cas:attributes"]
126     attributes = xml_from_dict.get("cas:attributes",{})
```
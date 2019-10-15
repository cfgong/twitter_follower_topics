# setup
- install dependencies
```
pip install -r requirements.txt
```
- put access token credentials are in auth.py
- to run flask server:
```
python3 api.py
```
- to test input to flask server:
```
curl http://localhost:5000/predict -d "twitter_handle=thisIsMyTwitterHandle" -X POST -v
```
- to run test file:
```
python3 test.py
```
# generating a requirements file
- create and activate a virtual environment
```
python3 -m venv env
source env/bin/activate
```
- Install packages: `pip install <package>`
- Run python file to make sure all necessary packages are installed `python3 test.py`
- Save all the packages in the file: `pip freeze > requirements.txt`
# references
- [How to Create a Simple Frontend, API, and Model with Python + Vue.js](https://medium.com/uptake-tech/how-to-create-a-simple-frontend-api-and-model-with-python-vue-js-a51841c66f8a)
- [Better Python dependency while packaging your project](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1)

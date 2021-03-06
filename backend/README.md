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
- run with debugging:
```
python3 api.py runserver -d
```
- to test input to flask server:
```
curl http://localhost:5000/predict -d "twitter_handle=AndrewYang" -X POST -v
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
- Can also check version of a specific package by running: `python -c "import some_package; print(some_package.__version__)"`
# references
- [How to Create a Simple Frontend, API, and Model with Python + Vue.js](https://medium.com/uptake-tech/how-to-create-a-simple-frontend-api-and-model-with-python-vue-js-a51841c66f8a)
- [Better Python dependency while packaging your project](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1)
- [Solve Cross Origin Resource Sharing with Flask](https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask)

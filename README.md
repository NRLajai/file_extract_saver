# file_extract_saver
## Code to upload a csv file and extract and save data in sqlite

git clone git@github.com:NRLajai/file_extract_saver.git <br>
git switch master <br>
pipenv install <br>
pipenv shell <br>
uvicorn main:handler.app --reload <br> <br>

Once all done, you can access endpoint through localhost:8000 <br>

Here i have created two endpoints
  1. one is /users/{id} - to read inserted users
  2. second is /uploadfile  - to upload a csv file

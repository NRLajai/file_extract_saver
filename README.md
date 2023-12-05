# file_extract_saver
## Code to upload a csv file and extract and save data in sqlite

git clone git@github.com:NRLajai/file_extract_saver.git <br>
cd file_extract_saver <br>
git switch master <br>
pipenv install <br>
pipenv shell <br>
uvicorn main:handler.app --reload <br> <br>

Once all done, you can access endpoint through localhost:8000 <br>

Here i have created three endpoints
  1.  first is / (at root path), you can access in browser with http://localhost:8000 - used to upload file
  2. YOU DONT HAVE TO ACCESS IT DIRECTLY, /uploadfile [POST method]- Once file uploaded in / (root path), its do further process
  3. third is /users/{id} - to read inserted user.
  

# extract-date--from-receipts

## What the repo is all about?
* It solves of the major accounting challenge, to extract the expense date from a given receipt. 
* I have implemented the same with the help of OCR and image processing. 
* The API is build on Django platform.
* The user input the **Base64 string** as POST request.
* I haven't used GET because of the heavy payload (It would through 414 error)

## How to run the API
* Activate your virtual environment (Eg -env)
* Install the requiremnts using the command
```pip install -r requirements.txt```
* Clone the repo usimg 
``` git clone <repo url>```
* Start the server using command ```python manage.py runserver```
* You might see the warning/error stating unapplied migrations, stop the server and run ```python manage.py migrate```
* Copy the http url in browser.
* viola !

## API in action 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
![POST base64 string](https://drive.google.com/file/d/0B9kSEIlZqe2-b2NJNkthLXJmMWE5ZzNiOWMxQl8zN3BOLS1J/view?usp=sharing "POST base64 string")
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")







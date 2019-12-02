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
![f1](https://github.com/shubagr/extract-date--from-receipts/blob/master/f1.png "user inut")
![POST base64 string](https://github.com/shubagr/extract-date--from-receipts/blob/master/f2.png "POST base64 string")
![f2](https://github.com/shubagr/extract-date--from-receipts/blob/master/f3.png "Date result =null if not present")
![f3](https://github.com/shubagr/extract-date--from-receipts/blob/master/f4.png "If date present")







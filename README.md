# face_rec
 Create virtual environment
 run 'pip install -r pip-depedencies.txt'
 run the file 'python FrMain.py'
After the message below is shown on the console, we may start to send the POST request
```
INFO:     Started server process [3024]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```
- The POST request was tested using Postman
- The json body is shown below:

We require the access token to  be included in the postman in order to use the api
send the request to here to register the user:
```
http://localhost:5000/selfie/photo/face/recognition
```
##  example for registration of user
```

    {   
        "icNumber": "1",
        "selfiePhotoPath1": "C:\\Users\\user\\Downloads\\Telegram Desktop\\selfie.jpeg",
        "processImagePath" :"C:\\Users\\user\\Downloads\\Telegram Desktop\\oke",
        "selfiePhotoPath" :"C:\\Users\\user\\Downloads\\Telegram Desktop\\New folder\\selfie.jpeg"

    }
```
- Icnumber is the id for the image owner, selfiePhotoPath1 is the first selfie image, and the selfiePhotoPath is the second selfie image
- processImagePath is the path where cropped face region is saved.

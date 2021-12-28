# DoorKeeper By Luftig

Hello everyone!
This is a small project I did at my home in order to alert me every time someone is passing through my security camera.
Its uses telegram API to send a message every time someone recognized is passing through a network camera.
Feel free to look and use the code, its working really well :)

QuickStart:
1. Create a Telegram bot using this this tutorial: https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e
   And Fill Telegram Bot Token and Chat Id
2. Add images to ./Images folder, and set the name of each image to person name
3. set IP_CAMERA_URL to your ip camera ip (I used IP Webcam android app), for example "http://192.168.1.24:8080/video"
4. docker-compose up

~ Use INFER_PROVIDERS Only on the first run in order to load all providers to mongo, after that set it to False ~

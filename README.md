# DoorKeeper By Luftig

Hello everyone!
This is a small project I did at my home in order to alert me every time someone is passing through my security camera.
Its uses telegram API to send a message every time someone recognized is passing through a network camera.
Feel free to look and use the code, its working really well :)

QuickStart:
1. Create Empty Redis instance and fill Host, Port and DB
   - Docker command: docker run --name redis-doorkeeper -p 7001:6379 -d redis
2. Create a Telegram bot using this this tutorial: https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e
   And Fill Telegram Bot Token and Chat Id
3. Add images do ./Images folder, and set the name of each image to person name
4. Run Main.py

~ Use INFER_IMAGE_FOLDER Only on the first run in order to load all images to redis, after that set it to False ~

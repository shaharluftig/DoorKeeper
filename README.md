# DoorKeeper   <img src="https://img.icons8.com/dusk/64/000000/dome-camera.png" width="48">


DoorKeeper is a simple and easy to use application that allows you to alert every time someone is passing through your IP Camera.

Feel free to fork and make contributions. I’ll try to get them into the main application.


### Installation
##### using telegram-bot notifier

1. Create a Telegram bot using this tutorial: https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e
2. Fill Telegram Bot Token and Chat ID under ./Config/__init__
3. set IP_CAMERA_URL to your ip camera ip (I used IP Webcam android app) under docker-compose.yml, for example "http://192.168.1.24:8080/video"
4. Add images to ./Images folder, and set the name of each image to person name
5. Run docker-compose up

### Development
#### Todos in the near future

 - Add tests
 - Add more Input/Output streams
 - Multi camera support

License
----

MIT

Dome Camera icon by [Icons8](https://icons8.com/) 
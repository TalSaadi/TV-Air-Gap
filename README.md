# TV-Air-Gap
LG WebOS TV air gap communication using a camera and volume buttons.

This project is a poc of semi-airgap communication using a tv and a web cam.
The idea is to transfer data from a tv to a third party computer by changing the volume on the tv and processing the changes using the web cam.

In LG WebOS TVs, when a volume up \ down button is pressed, a circle pop up is shown with the new volume status.
With this popup, we can transmit information by encoding a message to binary format and changing the volume to 0 / 1 in order to represent the bits.

To control the tv volume I used pywebostv - a wrapper libraray of lg web os client.

The connection to tv is simple:

```
def connect_to_tv():
    """
    Connect to WebOS TV
    :return: client
    """
    client = WebOSClient(TV_IP)
    client.connect()
    store = {}

    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == WebOSClient.REGISTERED:
            print("Registration successful!")

    return client
```

And afterwards the data trasmiting is very straight forward:

```
def leak_data(client, data):
    """
    Leak data over tv
    :param client: client tv
    :param data: data to leak
    """
    media = MediaControl(client)
    bits = to_bits(data)

    for bit in bits:
        media.set_volume(2)
        media.set_volume(bit)
        sleep(2)
```

Before every volume change, we set the volume to a different number (in this case 2) because if the volume is changed to the same number, there will be no pop up.
We also sleep for 2 seconds to wait for the pop up to dismiss.

After We have a video with all the bits represnted as volume changes, We can now split the video to frames every second.
We are splitting the video every second to get a backup for each frame in case that any future frame process will fail.

After having all the bits frames, We will use OpenCv Hough circles to detect and cut the volume circle.
For any frame that will fail, we will use the backup frame and hope for good.

```
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, 100)
```

Now we have all the bits volume circles, and we need to exctract each bit from them.
For that we will use FreeOcrApi Engine2 (for numbers):

```
payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 2,
               'detectOrientation': True
               }

    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    return json.loads(r.content.decode())['ParsedResults'][0]['ParsedText']
```

We will do that for every circle and the result will be a list of bits.
We can now decode the bits back to a string and we are done!

Wrapping all of that up:

```

# Tv leak part (nead to be captured by a video)
tv_client = connect_to_tv()
leak_data(tv_client, "Hey")

#########################################################
In this part we assume that the video is on the computer
#########################################################

split_to_frames()
detect_frames()
result = detect_bits()
print(from_bits(result))
```

POC example:

The Result bits circle after detecting the circles:

![Cirlces](https://raw.githubusercontent.com/TalSaadi/TV-Air-Gap/master/circles.JPG)

Detecting the bits and decoding the message:

![Bits](https://raw.githubusercontent.com/TalSaadi/TV-Air-Gap/master/bits.JPG)

#Note - code has been built for retroflective tape
#4189
import sensor, image, time, pyb

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.            # Create a clock object to track the FPS
sensor.set_contrast(3)                      #settings to increase difference between retrotape and
sensor.set_brightness(-3)
sensor.set_saturation(3)

threshold = (100, 38, 4, -13, 10, -28) # Thresholds for IR Tape when differenced

led = pyb.LED(4); #IR LEDs

extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
pixels = 0 # varible for storing central x values of blobs
while(True):
    #stores one frame with IR leds on and one with IR LEDs off. Differencing the two frames will allow to remove
    #almost all of the background noise while having only the tape visible
    led.on()
    extra_fb.replace(sensor.snapshot())
    led.off()
    img = sensor.snapshot()
    img =  img.difference(extra_fb)
    img = img.mean(3) #blurs the image to further remove background noise
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        pixels = blob.cx();
    print(pixels)

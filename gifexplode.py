import urllib2
import StringIO
from base64 import b64encode
from PIL import Image

class GifExplode:
    def __init__(self, image_url):
        self._image_url = image_url
        self._image = None
        self._frames = []
        self._size = None
        
    def explode(self):
        """ Returns list of base64 encoded frames and size in dictonary"""
        
        if not self._frames:

            self.__fetch_image()

            im = Image.open(self._image)
            self._size = im.size
            try:
                while True:

                    base64_encoded_frame = self.__encode_frame(im)
                    self._frames.append(base64_encoded_frame)

                    # Go to next frame
                    im.seek(im.tell()+1)

            except EOFError:
                # called at end of every gif frame *sequence*:
                self._image.close()
        
        return {'frames':self._frames, 'size': self._size}

    def size(self):
        return self._size
        
    def __fetch_image(self):
        """ Fetches the image from the web, saves to instance var"""
        
        # Note: this can raise a Value Error
        response = urllib2.urlopen(self._image_url)
        
        # Create image file in memory so PIL can use it
        self._image = StringIO.StringIO(response.read())
        
    def __encode_frame(self, frame):
        
        # Save frame to file-like object
        memory_frame = StringIO.StringIO()
        frame.save(memory_frame, format='GIF')

        # Encode
        base64_encoded_frame = b64encode(memory_frame.getvalue())
        
        memory_frame.close()
        
        return base64_encoded_frame
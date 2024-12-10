from app.helpers.pillow import imageSettings
from PIL import Image, ImageOps
from urllib.request import urlopen


url = "coconut.png"
file = Image.open(url)

settings = imageSettings()
settings.set_format(file, 'jpg')


# from PIL import Image, ImageOps
# from urllib.request import urlopen
# url = "https://python-pillow.org/assets/images/pillow-logo.png"
# image = Image.open(urlopen(url))
# size = (1000, 500)

# image_data = list(image.getdata())
# image_without_exif = Image.new(image.mode, image.size)
# image_without_exif.putdata(image_data)

# image_without_exif.save(u"clean_{}".format('hola.png'))

# print(list(image_without_exif.getdata()))

# print('-----------')
# data2 = list(image2.getdata())
# print(data2)

# with img as im:clear

#     ImageOps.contain(im, size).save('hola2.png')

from PIL import Image

path = input('Enter the path to the file: ')
image = Image.open(path)
name = input('Enter the name of the image: ')
edited_name = input('Enter the edited_name name of the image: ')
width, height = image.size
part = height // len(name)

lowest = 0
letters = {}
for let in list(name):
    letters[let] = (lowest, lowest + part)
    lowest += part

bg = image.resize((width, part * len(edited_name)))

last = 0
for let in edited_name:
    bg.paste(image.crop((0, letters[let][0], width, letters[let][1])),
              (0, last))
    last += part

bg.save(path[:path.rfind('\\') + 1] + edited_name + path[path.rfind('.'):])
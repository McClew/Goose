from PIL import Image, ImageGrab
import pytesseract as Tesseract
import pyautogui as Gui

# configurations
screenshot_path = "./goose_snip.png"
screenshot_offset = 150
tesseract_config = ('-l eng --oem 1 --psm 3')

# get mouse coordinates
mouse_position = Gui.position()

# set screenshot coordinates
left_x = mouse_position.x - screenshot_offset
top_y = mouse_position.y + screenshot_offset
right_x = mouse_position.x + screenshot_offset
bottom_y = mouse_position.y - screenshot_offset

# set grab_box (left_x, top_y, right_x, bottom_y)
grab_box = (left_x, top_y, right_x, bottom_y)

print(grab_box)

# get image
screenshot = ImageGrab.grab(bbox = grab_box)
screenshot.save("goose_snip.png")
screenshot = Image.open(screenshot_path)

# convert image to text
text = Tesseract.image_to_string(screenshot, config=pytesseract_config)

# print text
print(text)

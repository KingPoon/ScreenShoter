import os
import keyboard
import pyautogui
from PIL import Image, ImageTk
import tkinter as tk

screenshot_dir = "screenshots"
crop_dir = "crop"
os.makedirs(screenshot_dir, exist_ok=True)
os.makedirs(crop_dir, exist_ok=True)

# Scan for the lowest available number
def get_next_index(folder):
    existing = [f for f in os.listdir(folder) if f.endswith('.png')]
    nums = sorted([int(f.split('.')[0]) for f in existing if f.split('.')[0].isdigit()])
    
    # Find first missing number in sequence
    for i in range(1, len(nums) + 2):  # len+2 ensures it goes one beyond
        if i not in nums:
            return i

# Crop image (return True if saved)
def crop_image(image_path, output_path):
    result = {"saved": False}
    root = tk.Tk()
    root.title("Crop Image")

    img = Image.open(image_path)
    tk_img = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(root, width=img.width, height=img.height, cursor="cross")
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=tk_img)

    rect = None
    start_x = start_y = 0

    def on_press(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red")

    def on_drag(event):
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_release(event):
        end_x, end_y = event.x, event.y
        cropped = img.crop((start_x, start_y, end_x, end_y))
        cropped.save(output_path)
        result["saved"] = True
        print(f"Cropped image saved to: {output_path}")
        root.destroy()

    def on_close():
        print("Crop window closed without saving.")
        root.destroy()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
    return result["saved"]

# Main screenshot + crop logic
def take_screenshot(index):
    screenshot_path = os.path.join(screenshot_dir, f"{index}.png")
    cropped_path = os.path.join(crop_dir, f"{index}.png")

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

    success = crop_image(screenshot_path, cropped_path)
    return success

print("Press 'Q' to take and crop screenshot. Press 'Esc' to exit.")

while True:
    if keyboard.is_pressed("q"):
        index = get_next_index(crop_dir)  # Always get fresh next number
        if take_screenshot(index):
            pass  # success, continue
        while keyboard.is_pressed("q"):
            pass
    elif keyboard.is_pressed("esc"):
        print("Exiting...")
        break

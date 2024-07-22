import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import random

def determine_threshold():
    # Initial parameters
    lower_bound = 0
    upper_bound = 255
    step = 256

    # Create the main window
    root = tk.Tk()
    root.title("Determining the perception threshold")

    # Set the background color of the window to beige
    root.configure(bg='#f5f5dc')  # Beige color

    # Frame to hold the labels and instructions
    frame = tk.Frame(root, bg='#f5f5dc')
    frame.pack(padx=10, pady=10)

    # Create instruction label
    instruction = tk.Label(frame, text="Choose the lightest shade",
                           bg='#f5f5dc', font=('Helvetica', 14))
    instruction.pack(pady=10)

    # Create labels for shades of gray
    label_frame = tk.Frame(frame, bg='#f5f5dc')
    label_frame.pack()

    label1 = tk.Label(label_frame, bg='#f5f5dc')  # Beige background
    label1.grid(row=0, column=0, padx=10)
    label2 = tk.Label(label_frame, bg='#f5f5dc')  # Beige background
    label2.grid(row=0, column=1, padx=10)

    # Initialize these variables as nonlocal
    label1_shade = None
    label2_shade = None

    def update_image():
        nonlocal lower_bound, upper_bound, step, label1_shade, label2_shade
        
        # Generate two shades of gray
        shade1 = np.clip(lower_bound, 0, 255)
        shade2 = np.clip(upper_bound, 0, 255)
        
        # Create images with shades of gray
        img1 = Image.new('L', (200, 200), color=int(shade1))
        img2 = Image.new('L', (200, 200), color=int(shade2))
        
        # Convert images to PhotoImage
        img1_tk = ImageTk.PhotoImage(img1)
        img2_tk = ImageTk.PhotoImage(img2)

        # Randomly assign shades to labels
        if random.choice([True, False]):
            label1.config(image=img1_tk)
            label1.image = img1_tk
            label2.config(image=img2_tk)
            label2.image = img2_tk
            label1_shade, label2_shade = shade1, shade2
        else:
            label1.config(image=img2_tk)
            label1.image = img2_tk
            label2.config(image=img1_tk)
            label2.image = img1_tk
            label1_shade, label2_shade = shade2, shade1

        # Update instructions
        instruction.config(text="Choose the lightest shade\n")

    stop = False
    
    def on_click(event):
        nonlocal label1_shade, label2_shade, lower_bound, upper_bound, step, stop
        clicked_label = event.widget
        
        if clicked_label == label1:
            selected_shade = label1_shade
        elif clicked_label == label2:
            selected_shade = label2_shade
        else:
            return
        
        if selected_shade == max(label1_shade, label2_shade):
            step = step // 2
            upper_bound = min(255, int(lower_bound + step))
        else:
            stop = True
        
        # Check if the range is narrow enough
        if stop:
            step = step * 2
            messagebox.showinfo("Ended", f"Threshold found : {lower_bound + step // 2}")
            root.quit()  # Properly quit the main loop and close the window
        else:
            update_image()

    label1.bind("<Button-1>", on_click)
    label2.bind("<Button-1>", on_click)

    # Initial image update
    update_image()

    try:
        # Run the GUI loop
        root.mainloop()
    except Exception as e:
        print(f"An error has occurred : {e}")
    finally:
        # Ensure the window is closed properly
        root.destroy()
        return lower_bound + step // 2

if __name__ == "__main__":
    print(determine_threshold())

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import random

def determine_threshold(nb_point):
    # Initial parameters
    lower_bound = 0
    upper_bound = 255
    step = 256
    reduction_factor = 0.8  # Initial reduction factor
    growth_factor = 1.2  # Initial growth factor for increasing step
    step_values = []  # To store the step values during transitions
    iteration = 0
    phase = 0  # 0 for reduction phase, 1 for growth phase
    factor_decay = 0.95  # Decay factor for reduction factor in reduction phase
    growth_decay = 0.95  # Decay factor for growth factor in growth phase

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
        instruction.config(text="Choose the lightest shade\n"
                           f"Number of iterations : {iteration}")

    def on_click(event):
        nonlocal label1_shade, label2_shade, lower_bound, upper_bound, step, reduction_factor, growth_factor, iteration, phase, factor_decay, growth_decay
        
        clicked_label = event.widget
        
        if clicked_label == label1:
            selected_shade = label1_shade
        elif clicked_label == label2:
            selected_shade = label2_shade
        else:
            return
        
        correct_selection = (selected_shade == max(label1_shade, label2_shade))

        if phase == 0:  # Reduction phase
            if correct_selection:
                step = int(step * reduction_factor)
                upper_bound = lower_bound + step
                reduction_factor *= factor_decay  # Decay the reduction factor
                update_image()
            else:
                # Transition to the growth phase
                if len(step_values) < nb_point:
                    step_values.append(step)
                phase = 1
                iteration += 1
                # Prepare for the next phase
                lower_bound = np.clip(lower_bound + step, 0, 255)
                upper_bound = np.clip(upper_bound + step, 0, 255)
                step = int(step * growth_factor)  # Increase step size
                growth_factor *= growth_decay  # Decay the growth factor
                update_image()
        else:  # Growth phase
            if correct_selection:
                # Save the value of step and transition back to reduction phase
                if len(step_values) < nb_point:
                    step_values.append(step)
                phase = 0
                iteration += 1
                # Prepare for the next phase
                lower_bound = np.clip(lower_bound - step, 0, 255)
                upper_bound = np.clip(upper_bound - step, 0, 255)
                step = int(step / growth_factor)  # Decrease step size
                reduction_factor *= factor_decay  # Decay the reduction factor
                update_image()
            else:
                step = int(step // reduction_factor)
                upper_bound = lower_bound + step
                update_image()
        if len(step_values) >= nb_point:
            messagebox.showinfo("Ended", f"Threshold values: {step_values}")
            root.quit()
            
    def same_color():
        nonlocal lower_bound, upper_bound, step, iteration, phase, factor_decay, growth_decay, reduction_factor, growth_factor
        
        if phase == 0:  # Reduction phase
            # Save step value and transition to the growth phase
            if len(step_values) < nb_point:
                step_values.append(step)
            phase = 1
            iteration += 1
            # Prepare for the next phase
            lower_bound = np.clip(lower_bound + step, 0, 255)
            upper_bound = np.clip(upper_bound + step, 0, 255)
            step = int(step * growth_factor)  # Increase step size
            growth_factor *= growth_decay  # Decay the growth factor
            update_image()
        else:  # Growth phase
            # Save step value and adjust upper_bound only
            phase = 1
            iteration += 1
            # Only increase the upper bound
            upper_bound = np.clip(upper_bound + step, 0, 255)
            step = int(step / growth_factor)  # Decrease step size
            reduction_factor *= factor_decay  # Decay the reduction factor
            update_image()
        if len(step_values) >= nb_point:
            messagebox.showinfo("Ended", f"Threshold values: {step_values}")
            root.quit()

    # "Same color" button
    button_frame = tk.Frame(frame, bg='#f5f5dc')
    button_frame.pack(pady=10)
    same_color_button = tk.Button(button_frame, text="Same color", command=same_color)
    same_color_button.pack()

    label1.bind("<Button-1>", on_click)
    label2.bind("<Button-1>", on_click)

    # Initial image update
    update_image()

    try:
        # Run the GUI loop
        root.mainloop()
    except Exception as e:
        print(f"An error has occurred: {e}")
    finally:
        # Ensure the window is closed properly
        root.destroy()
        return step_values

if __name__ == "__main__":
    nb_point = 10  # Example number of iterations
    print(determine_threshold(nb_point))

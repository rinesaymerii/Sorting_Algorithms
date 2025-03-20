import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import matplotlib.ticker as mticker

# Initial values and settings
values = []
delay_time = 100
bar_color = '#298c8c'
completed_color = '#298c8c'
pivot_color = '#000000'
sorting_button_color = '#298c8c'

# Create the main window
root = tk.Tk()
root.title("SORTING ALGORITHMS")
root.configure(bg='white')
root.state('zoomed') 

# Create the Matplotlib figure
fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
ax = fig.add_subplot(111)

# Frame for Matplotlib canvas
canvas_frame = tk.Frame(root, bg='white', bd=2, relief='ridge')
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Matplotlib canvas
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to draw the array on the graph
def draw_array(array, colors, title="SORTING ALGORITHMS"):
    ax.clear()
    if array:
        bars = ax.bar(range(len(array)), array, color=colors)
        for i, bar in enumerate(bars):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{int(bar.get_height())}",  # Convert bar height to integer
                ha='center',
                va='bottom',
                fontsize=10,
                color='black',
            )
    
    # Set x-axis ticks and labels to be multiples of 4
    step = 3  
    tick_positions = range(0, len(array), step)
    tick_labels = [str(i) for i in tick_positions]  
    
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    
    # Force x-axis and y-axis labels to be integers
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x)}"))
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))  # Ensures y-axis is integer

    ax.set_title(title, fontsize=16, fontweight='bold', color='#000000')
    ax.set_xlabel("X", fontsize=10, color='#000000' )
    ax.set_ylabel("Y", fontsize=10, color='#000000')
    ax.set_ylim(0, max(array) + 10 if array else 10)
    fig.canvas.draw()

# Function to visualize updates
def visualize_update(array, colors, title):
    draw_array(array, colors, title)
    root.update()
    root.after(delay_time)


is_sorting = False

# BUBBLE SORT
def bubble_sort():
    global is_sorting
    if is_sorting:
        return
    is_sorting = True
    disable_other_sorting_buttons()
    array = values.copy()
    for i in range(len(array)):
        swapped = False
        for j in range(len(array) - i - 1):
            colors = [bar_color] * len(array)
            colors[j], colors[j + 1] = 'red', 'red'
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
            visualize_update(array, colors, "BUBBLE SORT")
        if not swapped:
            break
    draw_array(array, [completed_color] * len(array), "BUBBLE SORT - COMPLETED")
    is_sorting = False
    enable_all_sorting_buttons()
    is_sorting = False

# MERGE SORT
def merge_sort():
    global is_sorting
    if is_sorting:
        return
    is_sorting = True
    disable_other_sorting_buttons()
    array = values.copy()
    merge_sort_helper(array, 0, len(array) - 1)
    draw_array(array, [completed_color] * len(array), "MERGE SORT - COMPLETED")
    is_sorting = False
    enable_all_sorting_buttons()
    
def merge_sort_helper(array, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_helper(array, left, mid)
        merge_sort_helper(array, mid + 1, right)
        merge(array, left, mid, right)

def merge(array, left, mid, right):
    left_part = array[left:mid + 1]
    right_part = array[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            array[k] = left_part[i]
            i += 1
        else:
            array[k] = right_part[j]
            j += 1
        colors = [bar_color] * len(array)
        colors[k] = 'red'
        visualize_update(array, colors, "MERGE SORT")
        k += 1
    while i < len(left_part):
        array[k] = left_part[i]
        i += 1
        colors = [bar_color] * len(array)
        colors[k] = 'red'
        visualize_update(array, colors, "MERGE SORT")
        k += 1
    while j < len(right_part):
        array[k] = right_part[j]
        j += 1
        colors = [bar_color] * len(array)
        colors[k] = 'red'
        visualize_update(array, colors, "MERGE SORT")
        k += 1
is_paused = False 

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="START")
    else:
        pause_button.config(text="PAUSE")

def visualize_update(array, colors, title):
    global is_paused
    while is_paused:
        root.update_idletasks() 
        root.update()
    draw_array(array, colors, title)
    root.update()
    root.after(delay_time)

# QUICK SORT
def quick_sort():
    global is_sorting
    is_sorting = True
    disable_other_sorting_buttons()
    array = values.copy()
    quick_sort_helper(array, 0, len(array) - 1)
    draw_array(array, [completed_color] * len(array), "QUICK SORT - COMPLETED")
    is_sorting = False
    enable_all_sorting_buttons()


def quick_sort_helper(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quick_sort_helper(array, low, pi - 1)
        quick_sort_helper(array, pi + 1, high)

def partition(array, low, high):
    pivot = array[high]  # Pivot is the last element
    i = low - 1
    for j in range(low, high):
        colors = [bar_color] * len(array)
        colors[j] = 'red'  
        colors[high] = 'black'  
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
        visualize_update(array, colors, "QUICK SORT")
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1  

# Function to generate random values
def generate_random_values():
    global values
    try:
        num_values = int(num_values_entry.get().strip())
        if not 1 <= num_values <= 80:
            raise ValueError("Enter a number between 1 and 80.")
        values = [random.randint(1, 100) for _ in range(num_values)]
        draw_array(values, [bar_color] * len(values), "Random Values")
        enable_sorting_buttons()
        # Disable custom values input
        disable_custom_values_input()
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid integer between 1 and 80.")

# Function to input custom values
def input_values():
    global values
    user_input = custom_values_entry.get().strip()
    input_list = [val for val in user_input.split() if val.strip()]
    if len(input_list) < 1 or len(input_list) > 80:
        messagebox.showerror("Input Error", "You must enter between 1 and 80 values.")
        return
    try:
        values = [int(val) for val in input_list]
        draw_array(values, [bar_color] * len(values), "Custom Values")
        enable_sorting_buttons()
        # Disable random values input
        disable_random_values_input()
    except ValueError:
        messagebox.showerror("Input Error", "You must enter only integers (space-separated).")
        
# RESET
def reset():
    global values, is_sorting
    is_sorting = False
    values = []
    ax.clear()
    ax.set_title("", fontsize=14)
    fig.canvas.draw()
    custom_values_entry.delete(0, tk.END)
    num_values_entry.delete(0, tk.END)
    disable_sorting_buttons()
    enable_random_values_input()  
    enable_custom_values_input()  

def set_delay_time(val):
    global delay_time
    delay_time = int(val)

# User Interface
frame = tk.Frame(root, bg='white')
frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

title_label = tk.Label(frame, text="SORTING ALGORITHMS", font=('Arial Black', 25, 'bold'), bg='white', fg='black')
title_label.pack(pady=10)

random_label = tk.Label(frame, text="NUMBER OF RANDOM VALUES:", font=('Arial', 14, 'bold'), bg='white', fg='black')
random_label.pack(anchor="center", padx=10)

num_values_entry = tk.Entry(frame, font=('Arial', 12))
num_values_entry.pack(fill=tk.X, padx=10, pady=5)

generate_button = tk.Button(frame, text="GENERATE", font=('Arial', 14 , 'bold'), bg='black', fg='white', width=10, command=generate_random_values)
generate_button.pack(padx=10, pady=5)

custom_values_label = tk.Label(frame, text="CUSTOM VALUES (space-separated):", font=('Arial', 14, 'bold'), bg='white', fg='black')
custom_values_label.pack(anchor="center", padx=10)

custom_values_entry = tk.Entry(frame, font=('Arial', 12))
custom_values_entry.pack(fill=tk.X, padx=10, pady=5)

custom_values_button = tk.Button(frame, text="SUBMIT", font=('Arial', 14, 'bold'), bg='black', fg='white', width=10, command=input_values)
custom_values_button.pack(padx=10, pady=5)

delay_label = tk.Label(frame, text="DELAY (ms):", font=('Arial', 14, 'bold'), bg='white', fg='black')
delay_label.pack(anchor="center", padx=10)

delay_slider = tk.Scale(frame, from_=1, to=200, orient=tk.HORIZONTAL, command=set_delay_time, bg='black', fg='white')
delay_slider.set(delay_time)
delay_slider.pack(fill=tk.X, padx=10, pady=5)

sorting_frame = tk.Frame(frame, bg='white')
sorting_frame.pack(fill=tk.X, padx=10, pady=10)

# Ensure the parent window resizes along with the buttons
root.grid_columnconfigure(0, weight=1)

# Sorting Buttons in the Center with Fill
bubble_button = tk.Button(sorting_frame, text="BUBBLE SORT", font=('Arial', 16, 'bold'), bg=sorting_button_color, fg='white', command=bubble_sort)
bubble_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

merge_button = tk.Button(sorting_frame, text="MERGE SORT", font=('Arial', 16, 'bold'), bg=sorting_button_color, fg='white', command=merge_sort)
merge_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

quick_button = tk.Button(sorting_frame, text="QUICK SORT", font=('Arial', 16, 'bold'), bg=sorting_button_color, fg='white', command=quick_sort)
quick_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

sorting_frame.grid_columnconfigure(0, weight=1)

# Help Button
def show_help():
    messagebox.showinfo("Help", 
        "Number of random values: \nYou must enter a whole number from 1 to 80. If you enter a number greater than 80 or more than one number, you will receive an error message.\n\n"
        "Custom Values: \nYou must enter up to 80 possible values separated by a space. If you enter more than 80 values, you will receive an error message.\n\n"
        "Delay Time: \nThis is the speed, ranging from 1 to 200 milliseconds.\n\n"
        "Sorting: \nWhen the Bubble Sort, Merge Sort, or Quick Sort buttons are clicked, the corresponding sorting algorithm will be performed on the values.\n\n"
        "Reset: \nClicking the Reset button will clear the current chart and reset all values and inputs.")

help_button = tk.Button(frame, text="HELP", font=('Arial', 14, 'bold'), bg='black', fg='white', relief='flat', width=10, command=show_help)
help_button.pack(side="left", padx=5, pady=5)

reset_button = tk.Button(frame, text="RESET", font=('Arial', 14, 'bold'), bg='black', fg='white', relief='flat', width=10, command=reset)
reset_button.pack(side="right", padx=5, pady=5)

pause_button = tk.Button(frame, text="PAUSE", font=('Arial', 14, 'bold'), bg='#298c8c', fg='white', relief='flat', width=10, command=toggle_pause)
pause_button.pack(side="top", padx=5, pady=5)

# Set both buttons to have the same width
help_button.config(width=10)
reset_button.config(width=10)
pause_button.config(width=10)

# Pack the buttons with equal size and layout
help_button.pack(side="left", padx=5, pady=5)
reset_button.pack(side="right", padx=5, pady=5)
pause_button.pack(side="top", padx=5, pady=5)

def disable_other_sorting_buttons():
    bubble_button.config(state=tk.DISABLED)
    merge_button.config(state=tk.DISABLED)
    quick_button.config(state=tk.DISABLED)

def enable_all_sorting_buttons():
    bubble_button.config(state=tk.NORMAL)
    merge_button.config(state=tk.NORMAL)
    quick_button.config(state=tk.NORMAL)

def disable_sorting_buttons():
    bubble_button.config(state=tk.DISABLED)
    merge_button.config(state=tk.DISABLED)
    quick_button.config(state=tk.DISABLED)
    

def enable_sorting_buttons():
    bubble_button.config(state=tk.NORMAL)
    merge_button.config(state=tk.NORMAL)
    quick_button.config(state=tk.NORMAL)
    

def disable_random_values_input():
    generate_button.config(state=tk.DISABLED)

def enable_random_values_input():
    generate_button.config(state=tk.NORMAL)

def disable_custom_values_input():
    custom_values_button.config(state=tk.DISABLED)

def enable_custom_values_input():
    custom_values_button.config(state=tk.NORMAL)

# Initially disable sorting buttons
disable_sorting_buttons()

# Start the application
root.mainloop()

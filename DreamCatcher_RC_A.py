import tkinter as tk
import math

# To draw a dendrite and grow a new branch
def RC_A(x, y, height, width, angle, branch_level):
    global max_branch_level
    global current_level
    global angle_change
    global limit_angle
    global initial_angle

    if branch_level > max_branch_level:
        return

    if branch_level == 1:
        canvas.create_line(x, y, x, y - height, width=width)
        RC_A(x, y - height, height, width, angle, branch_level + 1)
    elif branch_level <= current_level and current_level > 1:
        # Calculate positions and attributes for child branches
        next_height = height * 0.75
        next_width = width - 2

        # Calculate angles for left and right child branches
        left_angle = angle + angle_change
        right_angle = angle - angle_change

        # print("branch level" + str(branch_level) + ": left-right angle")
        # print(math.degrees(left_angle), math.degrees(right_angle))

        branch_length = get_branch_len(next_height, left_angle, right_angle, branch_level)

        # Calculate the endpoints of the child branches
        x_left_branch = x + branch_length * math.cos(left_angle)
        y_left_branch = y - branch_length * math.sin(left_angle)
        
        x_right_branch = x + branch_length * math.cos(right_angle)
        y_right_branch = y - branch_length * math.sin(right_angle)

        # Draw the left branch
        if left_angle > 0 and left_angle < limit_angle:
            canvas.create_line(x, y, x_left_branch, y_left_branch, width=next_width)
            
            # Recursive call for left branch
            RC_A(x_left_branch, y_left_branch, next_height, next_width, left_angle, branch_level + 1)
        
        # Draw the right branch
        if right_angle > 0 and right_angle < limit_angle:
            canvas.create_line(x, y, x_right_branch, y_right_branch, width=next_width)

            # Recursive call for right branch
            RC_A(x_right_branch, y_right_branch, next_height, next_width, right_angle, branch_level + 1)

def get_stem_height(level):
    global max_branch_level
    global dendrite_height # Total height for the tree
    height = 0 
    branch_height_ratio = 0.75 # Child's height compared to its parent's height

    # If level is more than max branch level (6), height is calculated with max level 6
    level = min(level, max_branch_level)

    if level == 1:
        return dendrite_height
    else:
        height = dendrite_height / (1 + sum(branch_height_ratio ** (i - 1) for i in range(2, level + 1)))
        return height
    
def get_branch_len(next_height, left_angle, right_angle, branch_level):
    global limit_angle

    # If the angle is less than 0 or more than 180 degrees, replace it with 90 degrees for the branch len calculation only (not affecting the drawing part outside of the function)
    if left_angle < 0 or left_angle > limit_angle:
        left_angle = initial_angle
    if right_angle < 0 or right_angle > limit_angle:
        right_angle = initial_angle

    # Calculate the branch length based on the angles
    left_branch_len = next_height / math.sin(left_angle)
    right_branch_len = next_height / math.sin(right_angle)
    branch_length = min(abs(left_branch_len), abs(right_branch_len))

    # print("branch level" + str(branch_level) + ": left-right branch len")
    # print(left_branch_len, right_branch_len)
    # print()

    return branch_length

def increase_level():
    global current_level
    global stem_width
    global initial_angle
    
    if current_level < max_level:
        current_level += 1
        level_label.config(text=f"Level: {current_level}")
        canvas.delete("all")
        height = get_stem_height(current_level)
        RC_A(canvas_width / 2, canvas_height, height, stem_width, initial_angle, 1)

def decrease_level():
    global current_level
    global stem_width
    global initial_angle

    if current_level > 1:
        current_level -= 1
        level_label.config(text=f"Level: {current_level}")
        canvas.delete("all")
        height = get_stem_height(current_level)
        RC_A(canvas_width / 2, canvas_height, height, stem_width, initial_angle, 1)

# Create the main window
window = tk.Tk()
window.title("Dream Catcher")

# Initialize variables
canvas_width = 400
canvas_height = 400
max_level = 8
max_branch_level = 6
current_level = 1
dendrite_height = 150
stem_width = 10
initial_angle = math.pi / 2 # 90 degress in radians
angle_change = math.pi / 6  # 30 degrees in radians 
limit_angle=  math.pi # 180 degrees in radians 

# Create a canvas for drawing
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="orange")
canvas.pack()

# Create buttons and label
level_label = tk.Label(window, text=f"Level: {current_level}")
increase_button = tk.Button(window, text="+ Level Up", command=increase_level)
decrease_button = tk.Button(window, text="- Level Down", command=decrease_level)

# Place buttons and label
level_label.pack()
increase_button.pack()
decrease_button.pack()

# Draw the initial dendrite
RC_A(canvas_width / 2, canvas_height, dendrite_height, stem_width, initial_angle, current_level)

# Start the tkinter main loop
window.mainloop()
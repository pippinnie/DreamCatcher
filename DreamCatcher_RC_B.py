import tkinter as tk
import math

# Function to draw the dreamcatcher frame (circle)
def draw_frame():
    global frame_floor
    global frame_radius
    global frame_width
    global frame_color

    diameter = frame_radius * 2 
    center_x = canvas_width / 2

    # Calculate the coordinates for the oval
    x1 = center_x - frame_radius
    y1 = frame_floor - diameter
    x2 = center_x + frame_radius
    y2 = frame_floor

    canvas.create_oval(x1, y1, x2, y2, width=frame_width, outline=frame_color)

# To draw a dendrite and grow a new branch
def RC_A(x, y, height, width, angle, branch_level = 1):
    global max_branch_level
    global current_level
    global angle_change
    global limit_angle
    global initial_angle
    global dendrite_color
    global branch_height_ratio
    global stem_width_change

    if branch_level > max_branch_level:
        return

    if branch_level == 1:
        canvas.create_line(x, y, x, y - height, width=width, fill=dendrite_color)
        RC_A(x, y - height, height, width, angle, branch_level + 1)
    elif branch_level <= current_level and current_level > 1:
        # Calculate positions and attributes for child branches
        next_height = height * branch_height_ratio
        next_width = width - stem_width_change

        # Calculate angles for left and right child branches
        left_angle = angle + angle_change
        right_angle = angle - angle_change

        branch_length = get_branch_len(next_height, left_angle, right_angle)

        print("next h= " + str(next_height))
        print("branch len = " + str(branch_length))

        # Calculate the endpoints of the child branches
        x_left_branch = x + branch_length * math.cos(left_angle)
        y_left_branch = y - branch_length * math.sin(left_angle)
        
        x_right_branch = x + branch_length * math.cos(right_angle)
        y_right_branch = y - branch_length * math.sin(right_angle)

        # Draw the left branch
        if left_angle > 0 and left_angle < limit_angle:
            canvas.create_line(x, y, x_left_branch, y_left_branch, width=next_width, fill=dendrite_color)
            
            # Recursive call for left branch
            RC_A(x_left_branch, y_left_branch, next_height, next_width, left_angle, branch_level + 1)
        
        # Draw the right branch
        if right_angle > 0 and right_angle < limit_angle:
            canvas.create_line(x, y, x_right_branch, y_right_branch, width=next_width, fill=dendrite_color)

            # Recursive call for right branch
            RC_A(x_right_branch, y_right_branch, next_height, next_width, right_angle, branch_level + 1)

def get_stem_height(level):
    global max_branch_level
    global dendrite_height # Total height for the tree
    global branch_height_ratio
    height = 0 

    # If level is more than max branch level (6), height is calculated with max level 6
    level = min(level, max_branch_level)

    if level == 1:
        return dendrite_height
    else:
        height = dendrite_height / (1 + sum(branch_height_ratio ** (i - 1) for i in range(2, level + 1)))
        return height
    
def get_branch_len(next_height, left_angle, right_angle):
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

    return branch_length

# To draw the feather
def RC_B_1(x, y, leaf_level = 1):
    global current_level
    global feather_len
    global max_leaf_level
    global feather_color
    global feather_width
    global feather_angle
    global leaf_len
    global feather_stem
    global leaf_gap
    global flower_level

    if leaf_level > max_leaf_level: 
        return 
    
    if leaf_level == 1:
        # Draw feather stem
        canvas.create_line(x, y, x, y + feather_len, width=feather_width, fill=feather_color)

        # Recursive call for the leaves  
        RC_B_1(x, y + feather_stem, leaf_level + 1)

        return
    
    # Calculate the endpoints of the leaves
    x_left_leaf = x - leaf_len * math.cos(feather_angle)
    y_left_leaf = y - leaf_len * math.sin(feather_angle)
    
    x_right_leaf = x + leaf_len * math.cos(feather_angle)
    y_right_leaf = y - leaf_len * math.sin(feather_angle)

    # Draw the left leaf
    canvas.create_line(x, y, x_left_leaf, y_left_leaf, width=feather_width, fill=feather_color)
    
    # Draw the right leaf
    canvas.create_line(x, y, x_right_leaf, y_right_leaf, width=feather_width, fill=feather_color)

    # Draw the flower
    if current_level >= flower_level and leaf_level == max_leaf_level:
        # Draw the flowers on the left of the feather
        RC_B_2(x, y, x_left_leaf, y_left_leaf)

        # Draw the flowers on the right of the feather
        RC_B_2(x, y, x_right_leaf, y_right_leaf)

    # Recursive call for the next level leaves
    RC_B_1(x, y + leaf_gap, leaf_level + 1)

# To draw the flowers
def RC_B_2(x_ori, y_ori, x_leaf_end, y_leaf_end, flower_level = 1):
    global flower_radius
    global flower_width
    global flower_color
    global max_leaf_level
    global leaf_gap
    global current_level
    global max_level

    if flower_level == max_leaf_level:
        return
    
    # Find 1/3 point from the end leaf
    x_flower_center = (x_ori - x_leaf_end) / 3 + x_leaf_end
    y_flower_center = (y_ori - y_leaf_end) / 3 + y_leaf_end

    # Calculate coordinates for the main flower 
    x1 = x_flower_center - flower_radius
    y1 = y_flower_center - flower_radius
    x2 = x_flower_center + flower_radius
    y2 = y_flower_center + flower_radius

    # Draw the flower
    canvas.create_oval(x1, y1, x2, y2, width=flower_width, outline=flower_color)

    # Draw the petals at max level 8
    if current_level == max_level:
        RC_B_3(x_flower_center, y_flower_center)

    # Recursive call for the next level leaves
    RC_B_2(x_ori, y_ori - leaf_gap, x_leaf_end, y_leaf_end - leaf_gap, flower_level + 1)

# To draw the petals
def RC_B_3(x_flower_center, y_flower_center, petal_angle=0):
    global flower_radius
    global petal_radius
    global petal_width
    global petal_angle_change
    global petal_color

    # Stop drawing the petal after 1 full circle
    if petal_angle >= math.pi * 2:
        return

    # Find the petal center point
    x_petal_center = x_flower_center + math.cos(petal_angle) * flower_radius
    y_petal_center = y_flower_center - math.sin(petal_angle) * flower_radius

    # print(x_petal_center, y_petal_center)

    # Calculate coordinates for the main flower 
    x1 = x_petal_center - petal_radius
    y1 = y_petal_center - petal_radius
    x2 = x_petal_center + petal_radius
    y2 = y_petal_center + petal_radius

    # Draw the petal
    canvas.create_oval(x1, y1, x2, y2, width=petal_width, outline=petal_color)

    RC_B_3(x_flower_center, y_flower_center, petal_angle + petal_angle_change)

def get_frame_center_point():
    global canvas_width
    global frame_radius
    global frame_floor

    center_x = canvas_width / 2
    center_y = frame_floor - frame_radius

    return center_x, center_y

def get_rim_feather_point():
    feather_angle = math.pi / 4 

    x_delta = frame_radius * math.sin(feather_angle)
    y_delta = frame_radius * math.cos(feather_angle)

    return x_delta, y_delta

# Draw three feathers
def call_RC_B_1():
    global frame_radius

    center_x, center_y = get_frame_center_point()
    x_delta, y_delta = get_rim_feather_point()

    # Draw the left feather
    RC_B_1(center_x - x_delta, center_y + y_delta)

    # Draw the middle feather
    RC_B_1(center_x, center_y + frame_radius)

    # # Draw the right feather
    RC_B_1(center_x + x_delta, center_y + y_delta)

def increase_level():
    global current_level
    global stem_width
    global initial_angle
    
    if current_level < max_level:
        current_level += 1
        level_label.config(text=f"Level: {current_level}")
        canvas.delete("all")
        height = get_stem_height(current_level)
        draw_frame()
        RC_A(canvas_width / 2, frame_floor, height, stem_width, initial_angle)
        
        if current_level > 5:
            call_RC_B_1()

def decrease_level():
    global current_level
    global stem_width
    global initial_angle

    if current_level > 1:
        current_level -= 1
        level_label.config(text=f"Level: {current_level}")
        canvas.delete("all")
        height = get_stem_height(current_level)
        draw_frame()
        RC_A(canvas_width / 2, frame_floor, height, stem_width, initial_angle)

        if current_level > 5:
            call_RC_B_1()

# Create the main window
window = tk.Tk()
window.title("Dream Catcher")

# Initialize variables
## dendrite
frame_floor = 350
max_branch_level = 6
dendrite_height = 150
dendrite_color = "white"
stem_width = 10
stem_width_change = 2
branch_height_ratio = 0.75 # Child's height compared to its parent's height
initial_angle = math.pi / 2 # 90 degress in radians
angle_change = math.pi / 6  # 30 degrees in radians 
limit_angle=  math.pi # 180 degrees in radians 
## circle frame
frame_width = 3
frame_radius = 150
frame_color = "#91A8D0"
## feather
feather_len = 225
max_leaf_level = 9
feather_width = 3
feather_color = "#91A8D0"
feather_angle = math.pi / 6
leaf_len = 45
feather_stem = feather_len * 0.3
leaf_gap = (feather_len - feather_stem) / 7
## flower
flower_radius = 5
flower_width = 5
flower_level = 7
flower_color = "#F7CAC9"
## petal
petal_radius = flower_radius / 2 
petal_width = flower_width - 2
petal_angle_change = math.pi / 3 
petal_color = flower_color
## canvas
canvas_width = frame_radius * 2 + 100
canvas_height = frame_radius * 2 + feather_len + 100
# canvas_bg = "#7B886F" # green
# canvas_bg = "#8B635C" # brown
# canvas_bg = "#090C08" # black
canvas_bg = "#474056" # violet
current_level = 1
max_level = 8

# Create a canvas for drawing
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg=canvas_bg)
canvas.pack()

# Create buttons and label
level_label = tk.Label(window, text=f"Level: {current_level}")
increase_button = tk.Button(window, text="+", command=increase_level)
decrease_button = tk.Button(window, text="-", command=decrease_level)

# Place buttons and label
level_label.pack()
increase_button.pack()
decrease_button.pack()

# Draw the circle frame
draw_frame()

# Draw the initial dendrite
height = get_stem_height(current_level)
RC_A(canvas_width / 2, frame_floor, height, stem_width, initial_angle)

# Start the tkinter main loop
window.mainloop()
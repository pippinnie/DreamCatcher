import tkinter as tk
import math

# To recursively draw a dendrite and grow a new branch
def RC_A(x1, y1, height, width, dendrite_color, angle, branch_level = 1, stem_angle = 0):
    global max_branch_level
    global current_level
    global angle_change
    global limit_angle
    global branch_height_ratio
    global branch_width_change

    if branch_level > max_branch_level:
        return

    if branch_level == 1:
        # Get stem height for the current level
        height = get_stem_height()
        
        # Get RGB from the array
        r = dendrite_color[0]
        g = dendrite_color[1]
        b = dendrite_color[2]

        # Convert dendrite color from RGB to Hex
        dendrite_color_hex = rgb_to_hex(r, g, b)

        # Get the end point of the stem
        x2 = x1 - math.cos(angle) * height
        y2 = y1 + math.sin(angle) * height
        
        # Draw the stem
        canvas.create_line(x1, y1, x2, y2, width=width, fill=dendrite_color_hex)

        # Call the next branch level
        RC_A(x2, y2, height, width, dendrite_color, angle, branch_level + 1, angle)
    elif branch_level <= current_level and current_level > 1:
        # Calculate positions and attributes for child branches
        next_height = height * branch_height_ratio
        next_width = width - branch_width_change
        
        # Get RGB from the array and increases R by 10 and G by 5
        r = dendrite_color[0] + 10
        g = dendrite_color[1] + 5
        b = dendrite_color[2]
        next_dendrite_color = [r, g, b]
        
        # Convert dendrite color from RGB to Hex
        next_dendrite_color_hex = rgb_to_hex(r, g, b)

        # Calculate angles for left and right child branches
        left_angle = angle + angle_change 
        right_angle = angle - angle_change 

        # Get the branch len based on the height and the degrees
        branch_len = get_branch_len(next_height, left_angle, right_angle, stem_angle)

        # Calculate the endpoints of the child branches
        x_left_branch = x1 - branch_len * math.cos(left_angle)
        y_left_branch = y1 + branch_len * math.sin(left_angle)
        
        x_right_branch = x1 - branch_len * math.cos(right_angle)
        y_right_branch = y1 + branch_len * math.sin(right_angle)

        # Change the angle to degrees for comparison
        left_angle_degree = round(math.degrees(left_angle))
        right_angle_degree = round(math.degrees(right_angle))

        # Find limit angles of branches from the stem angle
        limit_left_angle_degree = round(math.degrees(stem_angle + limit_angle / 2))
        limit_right_angle_degree = round(math.degrees(stem_angle - limit_angle / 2))

        # Draw the left branch if within limit of 0 to 180 from the stem branch's direction
        if left_angle_degree <= limit_left_angle_degree and left_angle_degree >= limit_right_angle_degree:
            canvas.create_line(x1, y1, x_left_branch, y_left_branch, width=next_width, fill=next_dendrite_color_hex)
            
            # Recursive call for left branch
            RC_A(x_left_branch, y_left_branch, next_height, next_width, next_dendrite_color, left_angle, branch_level + 1, stem_angle)
        
        # Draw the right branch if within limit of 0 to 180 from the stem branch's direction
        if right_angle_degree <= left_angle_degree and right_angle_degree >= limit_right_angle_degree:
            canvas.create_line(x1, y1, x_right_branch, y_right_branch, width=next_width, fill=next_dendrite_color_hex)

            # Recursive call for right branch
            RC_A(x_right_branch, y_right_branch, next_height, next_width, next_dendrite_color, right_angle, branch_level + 1, stem_angle)

# Get the stem height 
def get_stem_height():
    global max_branch_level
    global dendrite_height # Total height for the tree
    global branch_height_ratio
    global current_level

    height = 0 

    # If level is more than max branch level (6), height is calculated with max level 6
    stem_level = min(current_level, max_branch_level)

    if stem_level == 1:
        return dendrite_height
    else:
        # Formular to calculate the height of the first branch (stem) based on the level
        height = dendrite_height / (1 + sum(branch_height_ratio ** (i - 1) for i in range(2, stem_level + 1)))
        return height

# Convert RGB to Hex (ref: https://www.educative.io/answers/how-to-convert-hex-to-rgb-and-rgb-to-hex-in-python)
def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Get the branch length based on the height and the degrees
def get_branch_len(next_height, left_angle, right_angle, stem_angle):
    global angle_change
    global canvas_height

    # For checking neighbor branches
    left_angle_2 = left_angle + angle_change * 2 
    right_angle_2 = right_angle - angle_change * 2 

    # Change all the angles to degrees for comparison
    stem_angle = round(math.degrees(stem_angle))
    left_angle = round(math.degrees(left_angle))
    right_angle = round(math.degrees(right_angle))
    left_angle_2 = round(math.degrees(left_angle_2))
    right_angle_2 = round(math.degrees(right_angle_2))
    
    # If the left angle and right angle and their neighbors are the same the stem angle, return the height as the branch length
    if left_angle == stem_angle or right_angle == stem_angle or left_angle_2 == stem_angle or right_angle_2 == stem_angle:
        return next_height
    
    return next_height / math.cos(angle_change)

# To recursively draw the feather
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

# To recursively draw the flowers
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

    # Calculate coordinates for the main flower 
    x1 = x_petal_center - petal_radius
    y1 = y_petal_center - petal_radius
    x2 = x_petal_center + petal_radius
    y2 = y_petal_center + petal_radius

    # Draw the petal
    canvas.create_oval(x1, y1, x2, y2, width=petal_width, outline=petal_color)

    RC_B_3(x_flower_center, y_flower_center, petal_angle + petal_angle_change)

def RC_C():
    global x_center
    global y_center
    global frame_radius
    global dendrite_height
    global dendrite_color
    global stem_width
    global current_level
    global max_branch_level

    # Draw the circle frame of the dreamcatcher
    draw_frame()

    # To get the number 1, 1 before starting the sequence at 2, which is the starting number of the dendrites
    # Limit n at the max branch level of 6
    n = min(current_level + 3, max_branch_level + 3)

    # Get the number of the dendrites from the last number of the fibonacci sequence
    dendrite_num = fibonacci(n)[-1]

    # Get the angle change between each dendrite in the full circle
    dendrite_angle_gap = math.pi * 2 / dendrite_num

    # Draw the dendrites
    angle = 0 

    while angle < math.pi * 2:
        # Find the dendrite stem point
        x_stem = x_center + math.cos(angle) * frame_radius
        y_stem = y_center - math.sin(angle) * frame_radius

        # Draw the initial dendrite
        RC_A(x_stem, y_stem, dendrite_height, stem_width, dendrite_color, angle)

        # Increase the angle by the gap
        angle += dendrite_angle_gap

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

    # Draw the oval
    canvas.create_oval(x1, y1, x2, y2, width=frame_width, outline=frame_color)
    
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_sequence = fibonacci(n - 1)
        next_num = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_num)
        return fib_sequence

# Draw three feathers
def call_RC_B_1():
    global frame_radius
    global x_center
    global y_center
    
    x_delta, y_delta = get_rim_feather_point()

    # Draw the left feather
    RC_B_1(x_center - x_delta, y_center + y_delta)

    # Draw the middle feather
    RC_B_1(x_center, y_center + frame_radius)

    # # Draw the right feather
    RC_B_1(x_center + x_delta, y_center + y_delta)

def get_rim_feather_point():
    global frame_radius

    angle = math.pi / 4 # 45 degrees gap from the center of the circle frame

    x_delta = frame_radius * math.sin(angle)
    y_delta = frame_radius * math.cos(angle)

    return x_delta, y_delta

def increase_level():
    global current_level
    global max_level

    if current_level < max_level:
        current_level += 1
        level_label.config(text=f"Level: {current_level}")
        canvas.delete("all")
        RC_C()       

        # Draw the three feathers 
        if current_level > 5:
            call_RC_B_1()

def decrease_level():
    global current_level

    if current_level > 1:
        current_level -= 1
        level_label.config(text=f"Level: {current_level}")
        canvas.delete("all")
        RC_C()       
        
        # Draw the three feathers 
        if current_level > 5:
            call_RC_B_1()

# Create the main window
window = tk.Tk()
window.title("Dream Catcher")

# Initialize variables
## dendrite
frame_floor = 350
dendrite_height = 150
max_branch_level = 6
# dendrite_color = "white"
dendrite_color = [135, 188, 240]
stem_width = 10
branch_width_change = 2
branch_height_ratio = 0.75 # Child's height compared to its parent's height
angle_change = math.pi / 6  # 30 degrees
limit_angle=  math.pi # 180 degrees 
## circle frame
frame_width = 3
frame_radius = 150
frame_color = "#91A8D0"
## feather
feather_len = 225
max_leaf_level = 9
feather_width = 3
feather_color = "#91A8D0"
feather_angle = math.pi / 6 # 30 degrees
leaf_len = 45
feather_stem = feather_len * 0.3
leaf_gap = (feather_len - feather_stem) / 7
## flower
flower_radius = 7
flower_width = 3
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
canvas_bg = "#474056" # violet
max_level = 8
current_level = 1
## points
x_center = canvas_width / 2
y_center = frame_floor - frame_radius

# Create a canvas for drawing
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg=canvas_bg)
canvas.pack()

# Create buttons and current level label
level_label = tk.Label(window, text=f"Level: {current_level}")
increase_button = tk.Button(window, text="+", command=increase_level)
decrease_button = tk.Button(window, text="-", command=decrease_level)

# Place buttons and label
level_label.pack()
increase_button.pack()
decrease_button.pack()

# Draw the frame and the dendrite
RC_C()

# Start the tkinter main loop
window.mainloop()
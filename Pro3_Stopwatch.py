# Hi, this is Zichun from Singapore/China, nice to meet you.
# Thanks for your effort.

import simplegui

# define global variables
t = 0
total_times = 0
whole_second_times = 0
time_m = 0
time_s = 0
time_ms = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global time_m
    global time_s 
    global time_ms
    
    time_m = t // 600
    time_s = (t - time_m * 600) // 10
    time_ms = t - time_m * 600 - time_s * 10      
    
    if time_s >= 10:
        time = str(time_m)+":"+str(time_s)+"."+str(time_ms)
    elif time_s <10:
        time = str(time_m)+":0"+str(time_s)+"."+str(time_ms)
    else:
        print "What happened?"
    
    return time
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def Start_handler():
    global total_times
# if timer is running, start button is useless.    
    if not timer.is_running():
        total_times += 1
        timer.start()
        
def Stop_handler():
    global time_m 
    global time_s
    global time_ms
    global whole_second_times
    
    timer.stop()
# check if the watch stop on a whole second 
    if time_ms == 0 and (time_s != 0 or time_m != 0):
        whole_second_times += 1
    
def Reset_handler():
    global t 
    global total_times
    global whole_second_times
    
    timer.stop()
    t = 0
    total_times = 0
    whole_second_times = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global t
    
    t += 1

# define draw handler
def draw_handler(canvas):
    global t
    
    time = format(t)
    stops = str(whole_second_times) + "/" + str(total_times)
    canvas.draw_text(time, [90,115], 50, "White")
    canvas.draw_text(stops, [230,40], 35, "Green") 
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300,200)

# register event handlers
Start = frame.add_button('Start', Start_handler, 100)
Stop = frame.add_button('Stop', Stop_handler, 100)
Reset = frame.add_button('Reset', Reset_handler, 100)
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

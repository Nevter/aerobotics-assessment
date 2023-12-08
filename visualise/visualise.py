import turtle

screen_width = 800
screen_height = 500

def init_viz():
  screen = turtle.Screen()
  screen.setup(screen_width+100, screen_height+100)

def draw_dot(x, y, size, color):
  turtle.penup()
  turtle.goto(x-screen_width/2, y-screen_height/2)
  turtle.pendown()
  turtle.dot(size, color)

def draw_line(start, end, size, color):
  turtle.width(size)
  turtle.color(color)
  turtle.penup()
  turtle.goto(start[0]-screen_width/2, start[1]-screen_height/2)
  turtle.pendown()
  turtle.goto(end[0]-screen_width/2, end[1]-screen_height/2)
  turtle.penup()


def draw_dots(canvas_locs, size, color):
  turtle.speed("fastest")
  turtle.tracer(0, 0)
  turtle.screensize(canvwidth=screen_width, canvheight=screen_height)
  for (x, y) in canvas_locs: 
    draw_dot(x, y, size, color)
  turtle.hideturtle()
  turtle.update()

def convert_gps_to_screen(latitude, longitude, lat_min, lat_max, lng_min, lng_max):
  x = (screen_width * (latitude - lat_min))/(lat_max-lat_min)
  y = (screen_height * (longitude - lng_min))/(lng_max-lng_min)
  return round(x ), round(y)
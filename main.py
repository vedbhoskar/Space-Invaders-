import turtle
import os
import csv
import time

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

# Draw the border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for _ in range(4):
    border_pen.forward(600)
    border_pen.left(90)
border_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

# Player movement
player_speed = 15


def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)


# Create the player's bullet turtle
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("square")
bullet.penup()
bullet.speed(0)
bullet.shapesize(0.3, 0.6)
bullet.hideturtle()
bullet.setheading(90)
bullet_speed = 40
bullet_state = "ready"  # ready - ready to fire, fire - bullet is firing


def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


def is_collision(t1, t2):
    distance = t1.distance(t2)
    if distance < 15:
        return True
    return False


# Create multiple enemy turtles
number_of_enemies = 12
enemies = []

for i in range(number_of_enemies):
    enemy = turtle.Turtle()
    enemy.color("red")
    enemy.shape("square")
    enemy.penup()
    enemy.speed(0)
    x = -200 + (i % 6) * 80
    y = 250 - (i // 6) * 50
    enemy.setposition(x, y)
    enemies.append(enemy)

enemy_speed = 2

# Score
score = 0
high_score = 0

# Score display
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 260)
score_string = f"Score: {score}  High Score: {high_score}"
score_pen.write(score_string, False, align="left", font=("Courier", 14, "normal"))
score_pen.hideturtle()

# Timer
game_time = 60  # 1 minute in seconds
start_time = time.time()

# Load high score from CSV file
def load_high_score():
    try:
        with open("high_score.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    return int(row[0])
    except (FileNotFoundError, ValueError):
        pass  # No valid high score found
    return 0  # Default value if high score is not loaded

# Check if game time is over
def is_time_up():
    elapsed_time = time.time() - start_time
    return elapsed_time >= game_time

# Update score
def update_score():
    global score, high_score
    score += 10
    if score > high_score:
        high_score = score
    score_pen.clear()
    score_string = f"Score: {score}  High Score: {high_score}"
    score_pen.write(score_string, False, align="left", font=("Courier", 14, "normal"))

# Game over screen
def game_over():
    update_score()
    score_pen.clear()
    score_string = f"Final Score: {score}  High Score: {high_score}\nGame Over"
    score_pen.write(score_string, False, align="center", font=("Courier", 20, "normal"))
    time.sleep(2)
    wn.reset()
# Enemy movement
# Enemy movement
def move_enemies():
    global enemy_speed
    for enemy in enemies:
        x, y = enemy.position()
        x += enemy_speed
        enemy.setposition(x, y)

        # Move the enemies back and down
        if x > 280 or x < -280:
            enemy_speed *= -1
            y -= 40
            enemy.setposition(x, y)



# Keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Load the high score
high_score = load_high_score()

# Main game loop
while True:
    wn.update()

    if is_time_up():
        game_over()
        break

    move_enemies()

    # Move the bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Check for collision between bullet and enemies
    for enemy in enemies:
        if is_collision(bullet, enemy):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            x = -200 + (enemies.index(enemy) % 6) * 80
            y = 250 - (enemies.index(enemy) // 6) * 50
            enemy.setposition(x, y)
            update_score()

    # Check for collision between player and enemies
    for enemy in enemies:
        if is_collision(player, enemy):
            player.hideturtle()
            for e in enemies:
                e.hideturtle()
            game_over()
            break

    # Check if all enemies are defeated
    if all(enemy.isvisible() == False for enemy in enemies):
        game_over()
        break

    # Continuous shooting
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"

    # Display timer
    elapsed_time = time.time() - start_time
    remaining_time = max(0, game_time - elapsed_time)
    timer_string = f"Time: {int(remaining_time)}s"
    score_pen.undo()
    score_pen.write(score_string + "  " + timer_string, False, align="left", font=("Courier", 14, "normal"))

wn.mainloop()

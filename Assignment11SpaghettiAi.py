import arcade
import enum
import random
import math




SCREEN_TITLE = "Snake"
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
SCREEN_HEADER = 50
SNAKE_SEGMENT_RADIUS = 10
SNAKE_LENGTH = 1
SNAKE_SPEED = 1 / 10



class Direction(enum.Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4



class Snake():
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__score = 0
        self.__numMoves = 0
        self.__body = self.GenerateBody()
        self.__food = None
        self.__foodx = 0
        self.__foody = 0
        self.__badfood = None
        self.__direction = Direction.Right
        #self.__paused = False
        self.__dead = False
        #arcade.schedule(self.SpawnFood, random.random() * 2)


        self.SpawnFood()
        arcade.schedule(self.update, SNAKE_SPEED)
        arcade.schedule(self.SpawnBadFood, random.random() * 2)



    def GetScore(self):
        return self.__score

    def GetNumMoves(self):
        return self.__numMoves

    def GetBody(self):
        return self.__body

    def GetBadFood(self):
        return self.__badfood

    def GetFood(self):
        return self.__food

    def GetDead(self):
        return self.__dead

    # def GetPaused(self):
    #     return self.__paused

    def GenerateBody(self):
        body = []
        while len(body) < SNAKE_LENGTH:
            x = int(self.__width / 2 - len(body))
            y = int(self.__height / 2)
            coor = [x, y]
            body.append(coor)
        return body

    # def KeyPressed(self, key):
    #     if key == arcade.key.UP and not self.__direction == Direction.Down:
    #         self.__direction = Direction.Up
    #     elif key == arcade.key.DOWN and not self.__direction == Direction.Up:
    #         self.__direction = Direction.Down
    #     elif key == arcade.key.RIGHT and not self.__direction == Direction.Left:
    #         self.__direction = Direction.Right
    #     elif key == arcade.key.LEFT and not self.__direction == Direction.Right:
    #         self.__direction = Direction.Left
    #
    #     # if key == arcade.key.P:
    #     #     self.__paused = False if self.__paused else True
    #
    #     if key == arcade.key.ENTER:
    #         self.Reset()
    #
    # def Reset(self):
    #     self.__score = 0
    #     self.__numMoves = 0
    #     self.__direction = Direction.Right
    #     self.__dead = False
    #     self.__body = self.GenerateBody()
    #     self.__food = None
    #     self.__badfood = None

    def SpawnFood(self):
        x, y = self.GetRandomCoor()
        self.__foodx = x
        self.__foody = y
        self.__food = [x, y]
        arcade.unschedule(self.SpawnFood)

    def BodyCollisionDetection(self, body):
        head = body[0]
        dead = False
        if head in body[1:]:
            dead = True
        return dead

    def NegativeScore(self):
        dead = False
        if self.__score < 0:
            dead= True
        return dead
    def SpawnBadFood(self, _):
        x,y = self.GetRandomCoor()
        self.__badfood = [x,y]
        arcade.unschedule(self.SpawnBadFood)
    def GetRandomCoor(self):
        x = random.randint(0, self.__width)
        y = random.randint(0, self.__height)

        if [x, y] in self.__body and self.CalcDistanceBetweenPoints(self.__body[0], [x, y]) > 5:
            x, y = self.GetRandomCoor()

        return x, y
    def CalcDistanceBetweenPoints(self, point1, point2):
        x_dist = abs(point1[0] - point2[0])
        y_dist = abs(point2[1] - point2[1])
        x_dist_pow = math.pow(x_dist, 2)
        y_dist_pow = math.pow(y_dist, 2)
        dist = math.sqrt(x_dist_pow + y_dist_pow)
        return int(dist)
    def CheckFoodEaten(self, body):
        head = body[0]
        eaten = False
        if self.__food == head:
            self.__score += 2
            self.__food = None
            eaten = True
            arcade.schedule(self.SpawnFood, random.random() * 2)
        if eaten == True:
            self.SpawnFood()
        return eaten

    def CheckBadFoodEaten(self, body):
        head = body[0]
        bad_eaten = False
        if self.__badfood == head:
            self.__score -= 1
            self.__badfood = None
            bad_eaten = True
            arcade.schedule(self.SpawnBadFood, random.random() * 2)
        return bad_eaten

    def MoveAi(self):
       
        if self.__body[0][0] != self.__foodx and  self.__body[0][1] != self.__foody:
            if self.__body[0][0] > self.__foodx:
                self.__direction = Direction.Left
            elif self.__body[0][0] < self.__foodx:
                self.__direction = Direction.Right
            elif self.__body[0][1] > self.__foody:
                self.__direction = Direction.Down
            elif self.__body[0][1] < self.__foody:
                self.__direction = Direction.Up


        elif   self.__body[0][0] != self.__foodx:
            if self.__body[0][0] > self.__foodx:
                self.__direction = Direction.Left
            elif self.__body[0][0] < self.__foodx:
                self.__direction = Direction.Right

        elif self.__body[0][1] != self.__foody:
            if self.__body[0][1] > self.__foody:
                self.__direction = Direction.Down
            elif self.__body[0][1] < self.__foody:
                self.__direction = Direction.Up


    def MoveSnake(self,):
            new_body = []
            x = 0
            y = 0
            self.MoveAi()
            if self.__direction == Direction.Right or self.__direction == Direction.Left:
                if self.__direction == Direction.Right:
                    x = 1
                else:
                    x = -1
            elif self.__direction == Direction.Up or self.__direction == Direction.Down:
                if self.__direction == Direction.Up:
                    y = 1
                else:
                    y = -1

            head = self.__body[0]
            new_head = [head[0] + x, head[1] + y]
            new_body.append(new_head)

            for i, _ in enumerate(self.__body):
                    if not i == 0:
                        new_body.append(self.__body[i - 1])

            self.__numMoves += 1

            edgeCollision = False
            if new_head[0] < 0 or new_head[0] > self.__width:
                     edgeCollision = True
            if new_head[1] < 0 or new_head[1] > self.__height:
                    edgeCollision = True
            return new_body, edgeCollision

    def update(self, _):
        if not self.__dead:
            new_body, self.__dead = self.MoveSnake()

            if not self.__dead:
                self.__dead = self.BodyCollisionDetection(new_body)
            if not self.__dead:
                self.__dead = self.NegativeScore()
            if not self.__dead:
                new_segment = self.CheckFoodEaten(new_body)
                if new_segment:
                    new_body.append(self.__body[-1])
            if not self.__dead:
                self.CheckBadFoodEaten(new_body)


            if not self.__dead:
                self.__body = new_body



class GameUI(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT + SCREEN_HEADER, SCREEN_TITLE)
        arcade.set_background_color( arcade.color.SMOKY_BLACK )
        GridWidth, GridHeight = self.CalcGrid()
        self.snake = Snake(GridWidth, GridHeight)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_line( 0,SCREEN_HEIGHT+1, SCREEN_WIDTH, SCREEN_HEIGHT+1, arcade.color.DUTCH_WHITE, 2)
        try:
            score = self.snake.GetScore()
            arcade.draw_text("Score = " + str(score), 10, SCREEN_HEIGHT + SCREEN_HEADER / 4, arcade.color.WHITE_SMOKE,
                             24)
        except:
            score = "..."
            arcade.draw_text("Score = " + str(score), 10, SCREEN_HEIGHT + SCREEN_HEADER/4, arcade.color.WHITE_SMOKE, 24)

        try:
            dead = self.snake.GetDead()
        #    paused = self.snake.GetPaused()
            score = self.snake.GetScore()
            score > 0

        except:
            dead = False
        #    paused = False

        if dead:
            arcade.draw_text("GAME OVER!", 0, SCREEN_HEIGHT/2, arcade.color.WHITE_SMOKE, 60, width=SCREEN_WIDTH, align="center")

        elif score < 0:
            arcade.draw_text("NEGATIVE SCORE!", 0, SCREEN_HEIGHT / 2, arcade.color.WHITE_SMOKE, 60, width=SCREEN_WIDTH, align="center")

        # elif paused:
        #     arcade.draw_text("GAME PAUSED!", 0, SCREEN_HEIGHT/2, arcade.color.WHITE_SMOKE, 60, width=SCREEN_WIDTH, align="center")

        self.draw_food()
        self.draw_body()
        self.draw_Badfood()

    # def on_key_press(self, key, modifier):
    #     try:
    #         self.snake.KeyPressed(key)
    #     except:
    #         print("An Error occured with handling the key press.")

    def CalcGrid(self):
        width = ( SCREEN_WIDTH / SNAKE_SEGMENT_RADIUS ) - 1
        height = ( SCREEN_HEIGHT / SNAKE_SEGMENT_RADIUS ) - 1
        return width, height

    def draw_body(self):
        try:
            body = self.snake.GetBody()
        except:
            body = [[0,0]]
        for i, coor in enumerate( body ):
            color = arcade.color.DARK_PASTEL_GREEN
            if i == 0:
                color = arcade.color.GRANNY_SMITH_APPLE
            arcade.draw_circle_filled(
                coor[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                coor[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                SNAKE_SEGMENT_RADIUS / 2,
                color
            )

    def draw_food(self):
        try:
            food = self.snake.GetFood()
        except:
            food = None
        if not food == None:
            arcade.draw_circle_filled(
                food[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                food[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                SNAKE_SEGMENT_RADIUS / 2,
                arcade.color.RED
            )

    def draw_Badfood(self):
        try:
            badfood = self.snake.GetBadFood()
        except:
            badfood = None
        if not badfood == None:
            arcade.draw_circle_filled(
                badfood[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                badfood[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                SNAKE_SEGMENT_RADIUS / 2,
                arcade.color.DARK_BROWN
            )

if __name__ == "__main__":
    gui = GameUI()
    arcade.run()

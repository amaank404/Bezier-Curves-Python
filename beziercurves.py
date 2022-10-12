import arcade
from typing import List, Optional

RESOLUTION = 4
RESCHANGERATE = 2
MOVSPEED = 300

def lerp(t: float, p0, p1) -> float:
    a = 1-t
    return (a*p0[0]+t*p1[0], a*p0[1]+t*p1[1])

def quadbez(t: float, p0, p1, p2) -> float:
    l0 = lerp(t, p0, p1)
    l1 = lerp(t, p1, p2)
    q0 = lerp(t, l0, l1)
    return q0

def cubebez(t: float, p0, p1, p2, p3) -> float:
    q0 = quadbez(t, p0, p1, p2)
    q1 = quadbez(t, p1, p2, p3)
    c0 = lerp(t, q0, q1)
    return c0

def calcbez(p0, p1, p2, p3, resolution: float) -> List[float]:
    ret = []
    for x in range(resolution+1):
        t = x/resolution
        p = cubebez(t, p0, p1, p2, p3)
        ret.append(p)
    return ret

class mainwindow(arcade.Window):
    def __init__(self, width: int = 800, height: int = 600, title: Optional[str] = 'Arcade Window'):
        super().__init__(width, height, title)
        self.background_color = arcade.color.BLACK
        self.showpoints = True
        self.p0 = [50, 50]
        self.p3 = [600, 600]
        self.p1 = [50, 150]
        self.p2 = [610, 300]
        self.curselection = 0
        self.movdirx = 0
        self.movdiry = 0
        self.shifting = False
    
    def on_update(self, delta_time: float):
        speed = delta_time*MOVSPEED* (0.5 if self.shifting else 1)
        if self.curselection == 0:
            self.p0[0] += self.movdirx*speed
            self.p0[1] += self.movdiry*speed
            self.p1[0] += self.movdirx*speed
            self.p1[1] += self.movdiry*speed
        elif self.curselection == 3:
            self.p2[0] += self.movdirx*speed
            self.p2[1] += self.movdiry*speed
            self.p3[0] += self.movdirx*speed
            self.p3[1] += self.movdiry*speed
        elif self.curselection == 1:
            self.p1[0] += self.movdirx*speed
            self.p1[1] += self.movdiry*speed
        elif self.curselection == 2:
            self.p2[0] += self.movdirx*speed
            self.p2[1] += self.movdiry*speed
        elif self.curselection == 4:
            self.p0[0] += self.movdirx*speed
            self.p0[1] += self.movdiry*speed
            self.p1[0] += self.movdirx*speed
            self.p1[1] += self.movdiry*speed
            self.p2[0] += self.movdirx*speed
            self.p2[1] += self.movdiry*speed
            self.p3[0] += self.movdirx*speed
            self.p3[1] += self.movdiry*speed

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.movdiry = 1
        elif symbol == arcade.key.DOWN:
            self.movdiry = -1
        elif symbol == arcade.key.LEFT:
            self.movdirx = -1
        elif symbol == arcade.key.RIGHT:
            self.movdirx = 1

        self.shifting = arcade.key.MOD_SHIFT & modifiers

    def on_key_release(self, symbol: int, modifiers: int):
        global RESOLUTION
        if symbol == arcade.key.P:
            self.showpoints = not self.showpoints
        elif symbol == arcade.key.KEY_1:
            self.curselection = 0
        elif symbol == arcade.key.KEY_2:
            self.curselection = 1
        elif symbol == arcade.key.KEY_3:
            self.curselection = 2
        elif symbol == arcade.key.KEY_4:
            self.curselection = 3
        elif symbol == arcade.key.A:
            self.curselection = 4
        elif symbol == arcade.key.EQUAL:
            RESOLUTION += RESCHANGERATE
        elif symbol == arcade.key.MINUS:
            RESOLUTION -= RESCHANGERATE

        elif symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.movdirx = 0
        elif symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.movdiry = 0

        self.shifting = arcade.key.MOD_SHIFT & modifiers

    def on_draw(self):
        arcade.start_render()

        bezc = calcbez(self.p0, self.p1, self.p2, self.p3, RESOLUTION)
        for x in range(len(bezc)-1):
            arcade.draw_line(*bezc[x], *bezc[x+1], arcade.color.WHITE)
        if self.showpoints:
            arcade.draw_points(bezc, arcade.color.YELLOW, 5)

        # Draw control points, main points
        arcade.draw_line(*self.p0, *self.p1, arcade.color.MAGENTA)
        arcade.draw_line(*self.p2, *self.p3, arcade.color.MAGENTA)
        arcade.draw_line(*self.p1, *self.p2, (*arcade.color.MAGENTA, 100))

        arcade.draw_circle_filled(*self.p3, 5, arcade.color.RED)
        arcade.draw_circle_filled(*self.p0, 5, arcade.color.RED)
        arcade.draw_circle_filled(*self.p1, 3, arcade.color.GREEN)
        arcade.draw_circle_filled(*self.p2, 3, arcade.color.GREEN)

        # Draw a outline around selected
        if self.curselection < 4:
            arcade.draw_circle_outline(*getattr(self, f"p{self.curselection}"), 8, arcade.color.WHITE)

        # Draw Labels
        arcade.draw_text("P0", self.p0[0]+10, self.p0[1]-10, arcade.color.LIGHT_BLUE)
        arcade.draw_text("P1", self.p1[0]+10, self.p1[1]-10, arcade.color.LIGHT_BLUE)
        arcade.draw_text("P2", self.p2[0]+10, self.p2[1]-10, arcade.color.LIGHT_BLUE)
        arcade.draw_text("P3", self.p3[0]+10, self.p3[1]-10, arcade.color.LIGHT_BLUE)

        # Draw Currently Selected

        arcade.draw_text(f"Current Selection: {('P' + str(self.curselection)) if self.curselection < 4 else 'ALL'}  |  Resolution: {RESOLUTION}", 10, self.get_size()[1]-10-12, arcade.color.GRAY)

def main():
    win = mainwindow(800, 800, "Cubic Bezier Curves")
    arcade.run()

main()
import math
from manim import *

def create_axes(): #helper fxn
    ax = Axes(
            x_range=[0, 10], 
            y_range=[0, 10], 
            x_length=12,
            y_length=6
        ).scale(0.8)
    x_label, y_label = ax.get_axis_labels("x", "f(x)")
    return ax, x_label, y_label

class R1cont(Scene):
    def construct(self):
        ax, x_label, y_label = create_axes()
        self.add(ax, x_label, y_label)

        def func1(x):
            return 10*smooth(x/10)
        graph = ax.plot(func1, color=RED)
        graph_label=ax.get_graph_label(graph, "f")
        self.play(Create(graph), FadeIn(graph_label))

        dot = Dot(ax.c2p(0,0))
        x_pointer = Vector(UP).move_to(ax.c2p(0,-2))
        y_pointer =  Vector(RIGHT).move_to(ax.c2p(-1,0))
        self.play(FadeIn(dot, x_pointer, y_pointer))
        self.play(MoveAlongPath(dot, graph), 
                  MoveAlongPath(x_pointer, Line(ax.c2p(0,-2), ax.c2p(10,-2))), 
                  MoveAlongPath(y_pointer, Line(ax.c2p(-1,0), ax.c2p(-1,10))), run_time=3)

        self.play(FadeOut(dot, x_pointer, y_pointer))
        self.play(VGroup(ax, x_label, y_label, graph, graph_label).animate.scale(0.7).to_corner(UR))

        cont = Tex("Continuidad").to_corner(UL)
        self.play(Write(cont))
        dot.move_to(ax.c2p(0,0))
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, graph), run_time=3)
        self.play(FadeOut(dot))
        text1 = MathTex("f \\in C^0([0, 10])", color=YELLOW).to_corner(DOWN*3+RIGHT*3)
        self.play(Write(text1))
        self.wait()
        self.play(Unwrite(text1))
        self.wait(2)

        discont_evitable = Tex("Discontinuidad Evitable").to_corner(UP*3+LEFT)
        self.play(Write(discont_evitable)) #Must be at x=3
        def func2(x):
            return (x**2-9)/(x-3)-2
        func2tex = MathTex(r"f(x)=\frac{x^2 - 9}{x - 3} - 2", color=RED).to_corner(DOWN*3+RIGHT*5)
        self.play(Transform(graph, ax.plot(func2, color=RED, discontinuities=[3])), Write(func2tex))

        dot, hollow_dot = Dot(ax.c2p(0,func2(0))), Dot(ax.c2p(3, func2(3.0001)), fill_opacity=0, stroke_width=2)
        self.play(MoveAlongPath(dot, ax.plot(func2, color=RED, x_range=[0,2.9999])))
        self.add(hollow_dot)
        self.play(MoveAlongPath(dot, ax.plot(func2, color=RED, x_range=[3.0001,10])))
        self.play(FadeOut(dot))

        line = Line(ax.c2p(3,0), ax.c2p(3,10), color=YELLOW)
        line_label = Tex("x=3", color=YELLOW).scale(0.6).to_corner(UP*2+RIGHT*9.5)
        self.play(FadeIn(line), Write(line_label))
        self.wait(2)

        self.play(Transform(func2tex, MathTex(r"f(x) = \begin{cases} \dfrac{x^2 - 9}{x - 3} - 2 & \text{if } x \ne 3 \\ 4 & \text{if } x = 3 \end{cases}",
                              color=YELLOW).to_corner(DOWN*2+RIGHT*2)))
        self.wait(2)
        self.play(FadeOut(line, line_label, hollow_dot, func2tex))

        discont_esencial = Tex("Discontinuidad Esencial").to_corner(UP*5+LEFT)
        self.play(Write(discont_esencial)) #Must be at x=5
        def func3(x):
            return 1/(x-5)+5
        func3tex = MathTex(r"f(x)=\frac{1}{x-5}+5", color=RED).to_corner(DOWN*3+RIGHT*5)
        func3graph_left = ax.plot(func3, x_range=[0,4.8], color=RED)
        func3graph_right = ax.plot(func3, x_range=[5.2, 10], color=RED)
        self.play(Transform(graph, func3graph_left), FadeIn(func3graph_right), Write(func3tex))
        
        dot = Dot(ax.c2p(0, func3(0)))
        self.add(dot)
        self.play(MoveAlongPath(dot, func3graph_left)) 
        self.play(MoveAlongPath(dot, func3graph_right))

        line = Line(ax.c2p(5,0), ax.c2p(5,10), color=YELLOW)
        line_label = Tex("x=5", color=YELLOW).scale(0.6).to_corner(UP*2+RIGHT*9.5)
        self.play(FadeIn(line), Write(line_label))
        text2 = MathTex("f \\notin C^0([0, 10])", color=YELLOW).to_corner(DR)
        self.play(Write(text2))
        self.wait(2)
        self.play(FadeOut(line, line_label), Unwrite(text2))
        self.play(FadeOut(graph, graph_label,func3graph_right, dot, func3tex))
        self.play(FadeOut(cont, discont_evitable, discont_esencial, ax, x_label, y_label))

        self.wait(5)

class R1diff(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=3,
            zoomed_display_width=4,
            zoomed_camera_config={
                "default_frame_stroke_width": 1,
            },
            **kwargs
        )

    def construct(self):
        ax, x_label, y_label = create_axes()
        self.add(ax, x_label, y_label)
        
        def func1(x):
            return 2*math.sin(x)+x
        graph = ax.plot(func1, color=BLUE)
        graph_label=ax.get_graph_label(graph, "f")
        self.play(Create(graph), FadeIn(graph_label))

        self.play(VGroup(ax, x_label, y_label, graph, graph_label).animate.scale(0.7).to_corner(UR))
        dot = Dot(ax.c2p(0,0))
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, graph), run_time=2)
        cont = Tex("Continuidad").to_corner(UP+LEFT*2)
        self.play(Write(cont), FadeOut(dot))

        arrow = Arrow(cont.get_bottom(), cont.get_bottom()+DOWN*2.8, stroke_width=3)
        diff_q = Tex("¿Diferenciablidad?").to_corner(UP*7+LEFT)
        self.play(FadeIn(arrow), Write(diff_q))
        self.play(Wiggle(cont))
        self.play(Wiggle(diff_q))
        self.play(FadeOut(cont, diff_q, arrow))

        diff = Tex("Diferenciabilidad").to_corner(UL)
        self.play(Write(diff))

        dot = Dot(ax.c2p(0,func1(0)))
        def get_tangent1():
            x = ax.p2c(dot.get_center())[0]
            y = func1(x)
            dx = 0.01
            dy = func1(x+dx)-func1(x)
            length = 2 #make a visible line
            x1, x2 = x-length, x+length
            y1, y2 = y-(dy/dx)*length, y+(dy/dx)*length
            return Line(ax.c2p(x1,y1), ax.c2p(x2,y2)).set_color(GREEN)
        tangent = always_redraw(get_tangent1)
        self.add(dot, tangent)
        self.play(MoveAlongPath(dot, graph, run_time=8))
        self.play(FadeOut(dot, tangent))

        def func2(x):
            return abs(x-5)+4
        self.play(Transform(graph, ax.plot(func2, color=BLUE)))
 
        dot = Dot(ax.c2p(0,func1(0)))
        def get_tangent2():
            x = ax.p2c(dot.get_center())[0]
            y = func2(x)
            dx = 0.01
            dy = func2(x+dx)-func2(x)
            length = 2 #make a visible line
            x1, x2 = x-length, x+length
            y1, y2 = y-(dy/dx)*length, y+(dy/dx)*length
            return Line(ax.c2p(x1,y1), ax.c2p(x2,y2)).set_color(GREEN)
        tangent = always_redraw(get_tangent2)
        self.add(dot, tangent)
        self.play(MoveAlongPath(dot, graph, run_time=8))
        self.play(FadeOut(dot, tangent))

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(ORANGE)
        zoomed_display.to_corner(UP*5+RIGHT)
        point_of_interest = ax.c2p(5, 4)
        
        frame.move_to(point_of_interest)

        self.play(Create(frame))
        self.activate_zooming() 
        
        self.play(self.get_zoomed_display_pop_out_animation())
        self.wait() 

        tangent.move_to(20) #out of frame
        self.play(FadeIn(dot, tangent))
        self.play(MoveAlongPath(dot, ax.plot(func2, color=BLUE, x_range=[4,6])), run_time=5)
        prob_pt = Dot(ax.c2p(5, func2(5)))
        self.play(FadeOut(tangent))
        self.play(Create(prob_pt))
        self.play(Indicate(prob_pt, color=YELLOW))

        self.play(FadeOut(*self.mobjects))
        self.clear()

from manim import *
import numpy as np

class R2cont(ThreeDScene):
    def construct(self):
        # Function definition
        def f(x, y):
            return np.sin(x) * np.cos(y)

        # Set up axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 1, 0.5],
        ).scale(0.6)
        labels = axes.get_axis_labels("x", "y", "f(x,y)")
        self.add(axes, labels)
        self.add_fixed_orientation_mobjects(labels)

        # Set camera
        self.set_camera_orientation(phi=45 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Animation: move point in the xy-plane and lift it to f(x,y)
        dots = []
        arrows = []
        for x in np.linspace(-2, 2, 5):
            for y in np.linspace(-2, 2, 5):
                input_point = axes.c2p(x, y, 0)
                output_point = axes.c2p(x, y, f(x, y))

                dot = Dot3D(input_point, color=YELLOW)
                arrow = Arrow3D(start=input_point, end=output_point, color=BLUE, stroke_width=2)

                # Optional: label the first few input points
                if x == 0 and y == 0:
                    label = Tex("input").scale(0.4).next_to(dot, UP)
                    self.add_fixed_orientation_mobjects(label)
                    self.play(Create(dot), Write(label), run_time=0.5)
                    self.play(Create(arrow), dot.animate.move_to(output_point), label.animate.next_to(dot, LEFT), run_time=0.7)
                    self.remove(label)
                else:
                    self.play(Create(dot), Create(arrow), dot.animate.move_to(output_point), run_time=0.3)

                dots.append(dot)
                arrows.append(arrow)

        # Optional: Show surface after plotting many points
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(24, 24),
        )
        surface.set_style(fill_opacity=0.6)
        surface.set_fill_by_checkerboard(ORANGE, BLUE)
        self.play(FadeIn(surface), run_time=2)

        self.wait(3)
        self.stop_ambient_camera_rotation()



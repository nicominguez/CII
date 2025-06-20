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

        t = ValueTracker(0)
        i_pt = ax.c2p(t.get_value(), func1(t.get_value()))

        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), func1(t.get_value()))))
        x_pointer = always_redraw(lambda: Vector(UP).move_to(ax.c2p(t.get_value(),-1.5)))
        y_pointer = always_redraw(lambda: Vector(RIGHT).move_to(ax.c2p(-0.7, func1(t.get_value()))))

        self.play(FadeIn(dot, x_pointer, y_pointer))
        self.play(t.animate.set_value(10), run_time=5)

        self.play(FadeOut(dot, x_pointer, y_pointer))

        t.set_value(5)
        dot.move_to(ax.c2p(5, func1(5)))
        line = always_redraw(lambda: Line(ax.c2p(0,0), ax.c2p(0,10), color=LIGHT_BROWN).move_to(ax.c2p(t.get_value(), 5)))
        self.play(FadeIn(dot, line))
        self.play(t.animate.set_value(10), run_time=2)
        self.play(t.animate.set_value(0), run_time=2)
        self.play(t.animate.set_value(5), run_time=2)
        self.wait(2)
        self.play(FadeOut(dot, line))

        self.play(VGroup(ax, x_label, y_label, graph, graph_label).animate.scale(0.7).to_corner(UR))

        cont = Tex("Continuidad").to_corner(UL)
        self.play(Write(cont))
        
        t.set_value(0)
        dot.move_to(ax.c2p(0,0))
        self.play(FadeIn(dot))
        self.play(t.animate.set_value(10), run_time=4)
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

        patch = Dot(ax.c2p(3, func2(3.0001)), color=DARK_BROWN)
        line.set_opacity(0.6)
        self.play(Transform(func2tex, MathTex(r"f(x) = \begin{cases} \dfrac{x^2 - 9}{x - 3} - 2 & \text{if } x \ne 3 \\ 4 & \text{if } x = 3 \end{cases}",
                              color=YELLOW).to_corner(DOWN*2+RIGHT*2)),
                  DrawBorderThenFill(patch)
                  )
        self.wait()

        dot2 = Dot(ax.c2p(0, func2(0)))
        self.play(MoveAlongPath(dot, graph))

        self.play(FadeOut(line, line_label, patch, dot, hollow_dot, func2tex))

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

        self.wait(2)

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
            return 2*np.sin(x)+x
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

class R2cont(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes().scale(0.6)
        x_label, y_label, z_label = Tex("x"), Tex("y").rotate(-0.5*PI), Tex("f(x,y)").rotate(PI, UP)
        self.add(ax, ax.get_axis_labels(x_label, y_label, z_label))
        self.set_camera_orientation()
        self.wait(3)
        self.move_camera(phi=DEGREES*55, theta=DEGREES*45)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)

        def func(x,y): 
            if x!=0 or y!=0:
                return 6*((x+2*y**2) / (x**2+y**2+1)**2)
            else:
                return 0 #the limit
        surface = ax.plot_surface(
            func,
            u_range=[-5,5],
            v_range=[-5,5],
            resolution=32,
        ).set_style(fill_color=GREEN, fill_opacity=0.9)
        
        pt = [2,2,0]
        dot = Sphere(ax.c2p(*pt), radius=0.05, fill_color=WHITE)
        self.play(DrawBorderThenFill(dot))

        center, radius = np.array([0,0,0]), 2.8
        pt_path = ParametricFunction(
            lambda t: ax.c2p(center[0] + radius * np.cos(t), center[1] + radius * np.sin(t), 0),
            t_range=[PI/4, 9*PI/4],
        )
        self.play(MoveAlongPath(dot, pt_path), run_time=6)
        self.wait(2)

        dot.generate_target()
        dot.target.move_to(ax.c2p(pt[0], pt[1], func(pt[0], pt[1])))

        d_line = DashedLine(ax.c2p(*pt), dot.target)

        self.play(MoveToTarget(dot), Create(d_line))
        self.wait()
        self.play(FadeOut(dot), FadeOut(d_line), FadeIn(surface))
        self.wait(4)

        line = Line(ax.c2p(pt[0], pt[1], -10), ax.c2p(pt[0], pt[1], 10)).set_color(LIGHT_BROWN)
        self.play(MoveAlongPath(line, pt_path), run_time=6)
        self.wait()
        self.play(FadeOut(line))

        self.stop_ambient_camera_rotation
        group = VGroup(ax, x_label, y_label, z_label, surface)
        self.move_camera(phi=DEGREES*55, theta=DEGREES*45)
        self.play(group.animate.scale(0.8).to_corner(UP*3+LEFT))

        # cont_tex = Tex("Continuidad").to_corner(UL)
        # self.play(Write(cont_tex))

        #def func2(x,y):
        #   return ((x**2)*y) / (x**2+y**2)
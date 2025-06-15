from manim import *

class R1(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10], 
            y_range=[0, 10], 
            x_length=12,
            y_length=6
        ).scale(0.8)
        x_label, y_label = ax.get_axis_labels("x", "f(x)")
        self.add(VGroup(ax, x_label, y_label))

        def func1(x):
            return 10*smooth(x/10)
        graph = ax.plot(func1, color=RED)
        graph_label=ax.get_graph_label(graph, "f")
        self.play(FadeIn(graph), FadeIn(graph_label))

        t = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), func1(t.get_value()))))
        x_pointer = always_redraw(lambda: Vector(UP).next_to(ax.c2p(t.get_value()-0.4, -1.2)))
        y_pointer = always_redraw(lambda: Vector(RIGHT).next_to(ax.c2p(-1.4, func1(t.get_value()))))
        self.play(FadeIn(dot, x_pointer, y_pointer))
        self.play(t.animate.set_value(10), run_time=3)

        self.play(FadeOut(dot, x_pointer, y_pointer))
        self.remove(dot, x_pointer, y_pointer)
        self.play(VGroup(ax, x_label, y_label, graph, graph_label).animate.scale(0.7).to_corner(UR))

        self.play(Write(Tex("Continuidad").to_corner(UL)))
        dot.move_to(ax.c2p(0,0))
        t.set_value(0)
        self.play(FadeIn(dot))
        self.play(t.animate.set_value(10), run_time=3)
        self.play(FadeOut(dot))
        text1 = MathTex("f \\in C^0([0, 10])", color=YELLOW).to_corner(DOWN*3+RIGHT*5)
        self.play(Write(text1))
        self.play(Unwrite(text1))
        self.remove(text1)

        self.play(Write(Tex("Discontinuidad Evitable").to_corner(UP*3+LEFT))) #Must be at x=3
        def func2(x):
            return (x**2-9)/(x-3)-2
        func2tex = MathTex(r"f(x)=\frac{x^2 - 9}{x - 3} - 2", color=RED).to_corner(DOWN*3+RIGHT*5)
        self.play(Transform(graph, ax.plot(func2, color=RED, discontinuities=[3])))
        self.play(Write(func2tex))

        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), func2(t.get_value())))
                            if abs(t.get_value()-3)>0.03
                            else Dot(ax.c2p(0,0), fill_opacity=0) #invisible
        )
        hollow_dot = always_redraw(lambda: Dot(ax.c2p(3, func2(3.0001)), fill_opacity=0, stroke_width=2)
                            if abs(t.get_value()-3)<=0.03
                            else Dot(ax.c2p(0,0), fill_opacity=0) #invisible
        )
        t.set_value(0)
        self.add(dot, hollow_dot)
        self.play(t.animate.set_value(2.999), run_time=3)
        self.wait(3)
        self.play(t.animate.set_value(10), run_time=3)
        self.play(FadeOut(dot))
        self.remove(dot)

        line = Line(ax.c2p(3,0), ax.c2p(3,10), color=YELLOW)
        line_label = Tex("x=3", color=YELLOW).scale(0.6).to_corner(UP*2+RIGHT*9.5)
        t.set_value(3) #For hollow_dot (sketch)
        self.play(FadeIn(line), Write(line_label), FadeIn(hollow_dot))
        self.wait(2)
        self.play(FadeOut(line, line_label))
        self.remove(line, line_label, hollow_dot)

        func2tex_pw = MathTex(r"f(x) = \begin{cases} \dfrac{x^2 - 9}{x - 3} - 2 & \text{if } x \ne 3 \\ 4 & \text{if } x = 3 \end{cases}",
                              color=YELLOW).to_corner(DOWN*3+RIGHT*5)
        self.play(Transform(func2tex, func2tex_pw))


        self.play(Write(Tex("Discontinuidad Esencial").to_corner(UP*5+LEFT))) #Must be at x=5
        def func3(x):
            return 1/(x-5)+5
        func3tex = MathTex(r"f(x)=\frac{1}{x-5}+5", color=RED).to_corner(DOWN*3+RIGHT*5)
        func3graph_left = ParametricFunction(lambda t: ax.c2p(t, func3(t)), t_range=[0, 4.8], color=RED)
        func3graph_right = ax.plot(func3, x_range=[5.2, 10], color=RED)
        self.play(Transform(graph, func3graph_left), FadeIn(func3graph_right), Transform(func2tex, func3tex))
        
        dot = Dot(func3graph_left.point_from_proportion(0))
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
        self.remove(line, line_label, text2)
        self.play(FadeOut(graph, graph_label,func3graph_right, dot, func2tex))

        self.wait(4)
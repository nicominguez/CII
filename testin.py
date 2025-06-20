from manim import *

class R1cont(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10], 
            y_range=[0, 10], 
            x_length=12,
            y_length=6
        ).scale(0.8)
        x_label, y_label = ax.get_axis_labels("x", "f(x)")
        self.add(ax, x_label, y_label)

        def func1(x):
            return 10*smooth(x/10)
        
        graph = ax.plot(func1, color=RED)
        graph_label=ax.get_graph_label(graph, "f")
        self.play(Create(graph), FadeIn(graph_label))

        t = ValueTracker(0)
        i_pt = ax.c2p(t.get_value(), func1(t.get_value()))

        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), func1(t.get_value()))))
        x_pointer = always_redraw(lambda: Vector(UP).move_to(ax.c2p(t.get_value(),-1)))
        y_pointer = always_redraw(lambda: Vector(RIGHT).move_to(ax.c2p(-2, func1(t.get_value()))))

        self.play(FadeIn(dot, x_pointer, y_pointer))
        self.play(t.animate.set_value(10))
        self.wait()
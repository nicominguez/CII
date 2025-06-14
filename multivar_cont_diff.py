from manim import *

class R1(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10], 
            y_range=[0, 10], 
            x_length=12,
            y_length=6
        )
        ax.shift(UP*0.5, RIGHT*0.5)

        x_label = ax.get_x_axis_label(
            label = "x",
            direction=DOWN,
            edge=DOWN,
            buff=0.5
        )
        y_label = ax.get_y_axis_label(
            label = "f(x)",
            direction=LEFT,
            edge=LEFT,
            buff=0.5
        )
        labels = VGroup(x_label, y_label)

        def func(x):
            return 10*smooth(x/10)
        g = ax.plot(func,  x_range=ax.x_range, color=RED)
        graph_label = ax.get_graph_label(
            graph = g, 
            label = "f",
            x_val=6,
            buff=0.5, 
            )
        graph = VGroup(g, graph_label)

        t = ValueTracker(0) # Will use t for x, so start at x=0
        initial_point = [ax.coords_to_point(t.get_value(), func(t.get_value()))]
        dot = Dot(point=initial_point)
        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))

        x_pointer=Vector(UP)
        x_pointer.add_updater(lambda m: m.next_to(ax.c2p(t.get_value()-0.3, -1.2))) # -0.3 bc scaling
        y_pointer=Vector(RIGHT)
        y_pointer.add_updater(lambda n: n.next_to(ax.c2p(-1.2, func(t.get_value()))))
        pointers = VGroup(x_pointer, y_pointer)

        self.add(ax, labels, graph, dot, pointers)
        self.play(t.animate.set_value(10), run_time=3)
        self.wait()
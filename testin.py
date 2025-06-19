from manim import *

class SurfaceTest(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        self.add(ax)

        epsilon = 0.001

        def func(x, y):  # removable discontinuity at (0, 0)
            if abs(x) > epsilon or abs(y) > epsilon:
                return x**2 / (x**2 + y**2)
            else:
                return None

        surface = Surface(
            lambda u, v: ax.c2p(u, v, func(u, v)),
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=(16, 16),
            fill_color=ORANGE,
            fill_opacity=0.8,
            checkerboard_colors=None
        )
        self.play(FadeIn(surface))
        self.wait()
        self.play(FadeOut(surface))
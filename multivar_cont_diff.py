from manim import *
import numpy as np

def create_axes():
    ax = Axes(
        x_range=[0, 10],
        y_range=[0, 10],
        x_length=12,
        y_length=6
    ).scale(0.8)
    x_label, y_label = ax.get_axis_labels("x", "f(x)")
    return ax, x_label, y_label

# Scene 1: Continuidad en R¹
class R1cont(Scene):
    def construct(self):
        # Crear ejes y etiquetas
        ax, x_label, y_label = create_axes()
        self.add(ax, x_label, y_label)
        
        # Graficar una función continua (curva roja)
        def func1(x):
            return 10 * smooth(x / 10)
        graph = ax.plot(func1, color=RED)
        graph_label = ax.get_graph_label(graph, "f")
        self.play(Create(graph), Write(graph_label))
        
        # Mostrar correspondencia entrada-salida con un punto móvil
        t = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), func1(t.get_value()))))
        x_pointer = always_redraw(lambda: Vector(UP).move_to(ax.c2p(t.get_value(), -1.2)))
        y_pointer = always_redraw(lambda: Vector(RIGHT).move_to(ax.c2p(-1.2, func1(t.get_value()))))
        self.play(FadeIn(dot, x_pointer, y_pointer))
        self.play(t.animate.set_value(10), run_time=5)
        self.play(FadeOut(dot, x_pointer, y_pointer))
        
        # Test de la recta vertical: línea vertical que barre el gráfico
        t.set_value(5)
        dot.move_to(ax.c2p(5, func1(5)))
        line = always_redraw(lambda: 
            Line(ax.c2p(0, 0), ax.c2p(0, 10), color=LIGHT_BROWN).move_to(ax.c2p(t.get_value(), 5))
        )
        self.play(FadeIn(dot, line))
        self.play(t.animate.set_value(10), run_time=2)
        self.play(t.animate.set_value(0), run_time=2)
        self.play(t.animate.set_value(5), run_time=2)
        self.wait(1)
        self.play(FadeOut(dot, line))
        
        # Etiqueta "Continuidad" y trazar la curva con un punto
        self.play(VGroup(ax, x_label, y_label, graph, graph_label).animate.scale(0.7).to_corner(UR))
        cont_text = Tex("Continuidad", color=WHITE).to_corner(UL)
        self.play(Write(cont_text))
        t.set_value(0)
        dot.move_to(ax.c2p(0, func1(0)))
        self.play(FadeIn(dot))
        self.play(t.animate.set_value(10), run_time=4)
        self.play(FadeOut(dot))
        
        # Indicar f ∈ C^0 (función continua)
        text_cont = MathTex("f \\in C^0([0,10])", color=YELLOW).to_corner(DR)
        self.play(Write(text_cont))
        self.wait(1)
        self.play(Unwrite(text_cont))
        
        # Ejemplo: discontinuidad evitable
        discont_ev = Tex("Discontinuidad Evitable", color=WHITE).to_corner(UL)
        self.play(Write(discont_ev), FadeOut(cont_text))
        def func2(x):
            return (x**2 - 9) / (x - 3) - 2
        func2_expr = MathTex(r"f(x) = \frac{x^2 - 9}{x - 3} - 2", color=YELLOW).to_corner(DOWN*3 + RIGHT*2)
        new_graph = ax.plot(func2, color=RED, discontinuities=[3])
        self.play(Transform(graph, new_graph), Write(func2_expr))
        
        # Trazo con punto (izquierda y derecha de x=3), mostrando hueco
        dot = Dot(ax.c2p(0, func2(0)))
        hollow = Dot(ax.c2p(3, func2(2.999)), fill_opacity=0, stroke_width=2)
        self.play(MoveAlongPath(dot, ax.plot(func2, x_range=[0, 2.999]), run_time=2))
        self.add(hollow)
        self.play(MoveAlongPath(dot, ax.plot(func2, x_range=[3.0001, 10]), run_time=2))
        self.play(FadeOut(dot))
        
        # Línea vertical en x=3 y etiqueta
        vline = Line(ax.c2p(3, 0), ax.c2p(3, 10), color=YELLOW)
        line_label = MathTex("x = 3", color=YELLOW).scale(0.7).next_to(vline, UR)
        self.play(FadeIn(vline), Write(line_label))
        self.wait(1)
        # Llenar el hueco (parche)
        patch = Dot(ax.c2p(3, func2(2.999)), color=DARK_BROWN)
        self.play(Transform(func2_expr, MathTex(
            r"f(x)=\begin{cases}"
            r"\frac{x^2 - 9}{x - 3} - 2 & x \neq 3 \\"
            r"4 & x = 3"
            r"\end{cases}",
            color=YELLOW
        ).to_corner(DOWN*2+RIGHT*2)), DrawBorderThenFill(patch))
        self.wait(1)
        
        # Continuar el trazo ahora que está continua
        dot2 = Dot(ax.c2p(0, func2(0)))
        self.play(MoveAlongPath(dot2, ax.plot(func2, x_range=[0, 2.9], color=RED), run_time=3))
        
        # Limpiar objetos de discontinuidad evitable
        self.play(FadeOut(vline, line_label, patch, hollow, func2_expr, dot2))
        
        # Ejemplo: discontinuidad esencial
        discont_es = Tex("Discontinuidad Esencial", color=WHITE).to_corner(UL)
        self.play(Write(discont_es), FadeOut(discont_ev))
        def func3(x):
            return 1/(x - 5) + 5
        func3_expr = MathTex(r"f(x)=\frac{1}{x-5}+5", color=YELLOW).to_corner(DOWN*3+RIGHT*2)
        graph_left = ax.plot(func3, x_range=[0, 4.8], color=RED)
        graph_right = ax.plot(func3, x_range=[5.2, 10], color=RED)
        self.play(Transform(graph, graph_left), FadeIn(graph_right), Write(func3_expr))
        
        # Trazo con punto en ambas ramas
        dot = Dot(ax.c2p(0, func3(0)))
        self.add(dot)
        self.play(MoveAlongPath(dot, graph_left, run_time=2))
        self.play(MoveAlongPath(dot, graph_right, run_time=2))
        
        # Asintota vertical en x=5
        asym = Line(ax.c2p(5, 0), ax.c2p(5, 10), color=YELLOW)
        asym_label = MathTex("x = 5", color=YELLOW).scale(0.7).next_to(asym, UR)
        self.play(FadeIn(asym), Write(asym_label))
        text_notC = MathTex("f \\notin C^0([0,10])", color=YELLOW).to_corner(DR)
        self.play(Write(text_notC))
        self.wait(1)
        self.play(FadeOut(asym, asym_label, text_notC))
        
        # Fin Escena 1
        self.play(FadeOut(graph, graph_right, graph_label, discont_es, ax, x_label, y_label, text_notC, asym, dot, func3_expr))
        self.wait(1)

# Scene 2: Diferenciabilidad en R¹
class R1diff(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(self,
            zoom_factor=0.3,
            zoomed_display_height=3,
            zoomed_display_width=4,
            zoomed_camera_config={"default_frame_stroke_width": 1},
            **kwargs
        )
    
    def construct(self):
        # Crear ejes y etiquetas
        ax, x_label, y_label = create_axes()
        self.add(ax, x_label, y_label)
        
        # Graficar función suave (diferenciable)
        def func1(x):
            return 2*np.sin(x) + x
        graph = ax.plot(func1, color=BLUE_B)
        graph_label = ax.get_graph_label(graph, "f")
        self.play(Create(graph), Write(graph_label))
        
        # Destacar continuidad de la función
        self.play(VGroup(ax, x_label, y_label, graph, graph_label).animate.scale(0.7).to_corner(UR))
        dot = Dot(ax.c2p(0, func1(0)), color=WHITE)
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, graph), run_time=2)
        cont_label = Tex("Continuidad", color=WHITE).to_corner(UL)
        self.play(Write(cont_label), FadeOut(dot))
        
        # Pregunta sobre diferenciabilidad
        arrow = Arrow(cont_label.get_bottom(), cont_label.get_bottom() + DOWN*2.8, stroke_width=3)
        diff_q = Tex("¿Diferenciabilidad?", color=WHITE).next_to(arrow, DOWN)
        self.play(GrowArrow(arrow), Write(diff_q))
        self.play(Wiggle(cont_label), Wiggle(diff_q))
        self.play(FadeOut(cont_label, diff_q, arrow))
        
        # Etiqueta diferenciabilidad
        diff_label = Tex("Diferenciabilidad", color=WHITE).to_corner(UL)
        self.play(Write(diff_label))
        
        # Trazar tangente en la curva suave
        dot = Dot(ax.c2p(0, func1(0)), color=WHITE)
        def get_tangent1():
            x = ax.p2c(dot.get_center())[0]
            y = func1(x)
            dx = 0.01
            dy = func1(x + dx) - func1(x)
            length = 1
            x1, x2 = x - length, x + length
            y1 = y - (dy/dx) * length
            y2 = y + (dy/dx) * length
            return Line(ax.c2p(x1, y1), ax.c2p(x2, y2), color=GREEN)
        tangent1 = always_redraw(get_tangent1)
        self.add(dot, tangent1)
        self.play(MoveAlongPath(dot, graph), run_time=8)
        self.play(FadeOut(dot, tangent1))
        
        # Función con vértice (continua, no diferenciable)
        def func2(x):
            return abs(x - 5) + 4
        new_graph = ax.plot(func2, color=BLUE_B)
        self.play(Transform(graph, new_graph))
        
        dot = Dot(ax.c2p(0, func2(0)), color=WHITE)
        def get_tangent2():
            x = ax.p2c(dot.get_center())[0]
            y = func2(x)
            dx = 0.01
            dy = func2(x + dx) - func2(x)
            length = 1
            x1, x2 = x - length, x + length
            y1 = y - (dy/dx) * length
            y2 = y + (dy/dx) * length
            return Line(ax.c2p(x1, y1), ax.c2p(x2, y2), color=GREEN)
        tangent2 = always_redraw(get_tangent2)
        self.add(dot, tangent2)
        self.play(MoveAlongPath(dot, graph), run_time=8)
        self.play(FadeOut(dot, tangent2))
        
        # Acercar al punto no diferenciable (x=5)
        zoom_frame = self.zoomed_camera.frame
        zoom_frame.set_color(PURPLE)
        self.activate_zooming()
        point = ax.c2p(5, func2(5))
        zoom_frame.move_to(point)
        self.play(Create(zoom_frame))
        self.wait(1)
        
        # Resaltar punto problemático
        prob_point = Dot(point, color=YELLOW)
        self.play(Create(prob_point))
        self.play(Indicate(prob_point, color=YELLOW))
        no_diff = MathTex(r"f \text{ no es diferenciable en } x = 5", color=YELLOW).to_corner(UR)
        self.play(Write(no_diff))
        self.wait(1)
        
        # Fin Escena 2
        self.play(FadeOut(*self.mobjects))
        self.clear()

# Scene 3: Continuidad en R²
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
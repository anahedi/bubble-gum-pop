from manim import *

class ClusteringPipelineExplanation(Scene):
    def construct(self):
        # Configuration
        config.background_color = "#1E1E1E"
        
        # TITLE
        title = Text("Hey Banco: Pipeline de Segmentacion NLP", font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # STEP 1: RAW DATA
        step1_title = Text("Paso 1: Datos Crudos (Mensajes de Clientes)", font_size=28, color=YELLOW)
        step1_title.next_to(title, DOWN, buff=0.5)
        
        messages = VGroup(
            Text('No puedo entrar a mi app', font_size=24),
            Text('¿Donde hay un cajero?', font_size=24),
            Text('Quiero pedir un credito', font_size=24),
            Text('Me cobran anualidad', font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)
        
        self.play(FadeIn(step1_title))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT) for m in messages], lag_ratio=0.3))
        self.wait(2)

        # STEP 2: EMBEDDINGS (SentenceTransformer)
        step2_title = Text("Paso 2: Generacion de Embeddings", font_size=28, color=YELLOW)
        step2_title.move_to(step1_title)
        
        matrices = VGroup()
        for i in range(4):
            # Simulate a matrix using Text and shapes to avoid LaTeX dependency
            bracket_l = Text("[", font_size=36, color=WHITE)
            values = Text("0.12  -0.85  ...", font_size=20, color=GREEN_C)
            bracket_r = Text("]", font_size=36, color=WHITE)
            matrix = VGroup(bracket_l, values, bracket_r).arrange(RIGHT, buff=0.1)
            
            matrix.move_to(messages[i].get_center())
            matrices.add(matrix)
            
        self.play(
            FadeOut(step1_title), FadeIn(step2_title),
            *[Transform(messages[i], matrices[i]) for i in range(4)]
        )
        self.wait(2)

        # STEP 3: UMAP
        step3_title = Text("Paso 3: Reduccion de Dimensionalidad (UMAP)", font_size=28, color=YELLOW)
        step3_title.move_to(step2_title)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY},
        )
        axes.shift(DOWN * 0.5)

        # Scatter points simulating high dim projected to 2D
        points = VGroup()
        coords = [
            [-1.5, 1.5], [-1.2, 1.8], [-1.8, 1.2], [-1.6, 1.9], [-1.1, 1.4], # Cluster 1
            [1.5, -1.5], [1.2, -1.8], [1.8, -1.2], [1.6, -1.9], [1.1, -1.4], # Cluster 2
            [1.5, 1.5], [1.2, 1.8], [1.8, 1.2], [1.6, 1.9], [1.1, 1.4], # Cluster 3
            [0.1, -2.5], [-2.5, 0.1], [2.2, 0.5], [-1.0, -1.5] # Noise
        ]
        
        for coord in coords:
            dot = Dot(axes.c2p(*coord), color=WHITE, radius=0.08)
            points.add(dot)

        self.play(FadeOut(step2_title), FadeIn(step3_title))
        self.play(FadeOut(messages))
        self.play(Create(axes), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in points], lag_ratio=0.1), run_time=2)
        self.wait(1)

        # STEP 4: HDBSCAN
        step4_title = Text("Paso 4: Clustering por Densidad (HDBSCAN)", font_size=28, color=YELLOW)
        step4_title.move_to(step3_title)

        # Coloring clusters and noise
        self.play(FadeOut(step3_title), FadeIn(step4_title))
        
        animations = []
        for i, p in enumerate(points):
            if i < 5:
                animations.append(p.animate.set_color(RED))
            elif i < 10:
                animations.append(p.animate.set_color(GREEN))
            elif i < 15:
                animations.append(p.animate.set_color(BLUE))
            else:
                animations.append(p.animate.set_color(GREY).set_opacity(0.5))

        # Circles around clusters
        c1 = Circle(radius=0.7, color=RED).move_to(axes.c2p(-1.4, 1.5))
        c2 = Circle(radius=0.7, color=GREEN).move_to(axes.c2p(1.4, -1.5))
        c3 = Circle(radius=0.7, color=BLUE).move_to(axes.c2p(1.4, 1.5))

        self.play(*animations, run_time=2)
        self.play(Create(c1), Create(c2), Create(c3))
        
        noise_text = Text("Ruido (-1)", font_size=20, color=GREY).next_to(axes.c2p(2.2, 0.5), RIGHT)
        self.play(FadeIn(noise_text))
        self.wait(2)

        # STEP 5: INSIGHTS
        step5_title = Text("Paso 5: Insights y Correlaciones", font_size=28, color=YELLOW)
        step5_title.move_to(step4_title)

        label_c1 = Text("App/Conexion", font_size=20, color=RED).next_to(c1, UP)
        label_c2 = Text("Cajeros", font_size=20, color=GREEN).next_to(c2, DOWN)
        label_c3 = Text("Creditos", font_size=20, color=BLUE).next_to(c3, UP)

        self.play(FadeOut(step4_title), FadeOut(noise_text), FadeIn(step5_title))
        self.play(Write(label_c1), Write(label_c2), Write(label_c3))

        insight_box = RoundedRectangle(corner_radius=0.5, width=5, height=2, color=ORANGE, fill_opacity=0.1)
        insight_box.to_edge(RIGHT).shift(DOWN*0.5)
        
        insight_text = VGroup(
            Text("Insights Automaticos", font_size=24, color=ORANGE, weight=BOLD),
            Text("- TF-IDF Keywords", font_size=18),
            Text("- Correlacion Spearman", font_size=18),
            Text("  (Edad vs Uso de Cajeros)", font_size=16, color=LIGHT_GREY),
        ).arrange(DOWN, aligned_edge=LEFT).move_to(insight_box.get_center())

        self.play(axes.animate.shift(LEFT*2.5), 
                  points.animate.shift(LEFT*2.5), 
                  c1.animate.shift(LEFT*2.5), c2.animate.shift(LEFT*2.5), c3.animate.shift(LEFT*2.5),
                  label_c1.animate.shift(LEFT*2.5), label_c2.animate.shift(LEFT*2.5), label_c3.animate.shift(LEFT*2.5))
        
        self.play(Create(insight_box), Write(insight_text))
        self.wait(3)

        # CONCLUSION
        conclusion = Text("Segmentacion Lista para Produccion ✅", font_size=36, color=GREEN_C)
        self.play(FadeOut(axes), FadeOut(points), FadeOut(c1), FadeOut(c2), FadeOut(c3),
                  FadeOut(label_c1), FadeOut(label_c2), FadeOut(label_c3),
                  FadeOut(insight_box), FadeOut(insight_text), FadeOut(step5_title))
        
        self.play(Write(conclusion))
        self.wait(2)

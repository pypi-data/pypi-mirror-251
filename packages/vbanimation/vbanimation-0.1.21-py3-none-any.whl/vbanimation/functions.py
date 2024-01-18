from manim import *
import os
import re
import subprocess
import shutil
from moviepy.video.io.VideoFileClip import VideoFileClip



def solution_to_tikz(file_sol="solution.tex", file_tikz="tikzpicture.tex"):
    with open(file_sol, 'r') as file:
        files = ""
        for i in file:
            files += i
            
        tikz = re.findall(r'\\begin{tikzpicture}.*?\\end{tikzpicture}', files, re.DOTALL)
        
        if tikz:
            tikzpicture = tikz[0]
        else:
            try:
                tikzpicture = open(file_tikz, "r").read()
            except:
                return None
        
        if tikzpicture:
            if not os.path.exists("picture"):
                os.mkdir("picture")
        
            with open("picture/tikz.tex", "w") as tikz_file:
                tikz_file.write(tikzpicture)
                
            with open("picture/main.tex", "w") as main_file:
                main_file.write(r"""
                \documentclass[preview, margin=5mm]{standalone}
                \usepackage{v-test-paper}
                \begin{document}
                \color{black}
                \input{tikz.tex}
                \end{document}
                """)
            
            os.chdir("picture")
            subprocess.call(["pdflatex", "main.tex"])
            subprocess.call(['vbpdf', 'topng', '-t', '-d' , '480'])
            os.chdir("..")
            return 'picture/main.png'
        
        else:
            return None
            
        
    
    
def solution_to_align(file_sol="solution.tex"):
    with open(file_sol, 'r') as file:
        files = ""
        for i in file:
            files += i
            
        align = re.findall(r'\\begin{align\*}.*?\\end{align\*}', files, re.DOTALL)
        with open("align.tex", "w") as al:
            al.write(align[0])
            
    equations = []
    with open("align.tex", "r") as f:
        for n, i  in enumerate(f):
            intertext = re.search(r'\\intertext{.*?}$', i)
            print(intertext)
            if intertext:
                equations.append((intertext[0], n))
            else:
                equations.append(str(i).strip())

    dict_equatons = {}

    intertext_list = []

    for i in equations:
        if type(i) == tuple:
            intertext_list.append(i)

    for i in range(len(intertext_list)):
        start_line = intertext_list[i][1]
        if i == len(intertext_list)-1:
            end_line = len(equations)-1
        else:
            end_line = intertext_list[i+1][1]
        dict_equatons[f'set_{i+1}'] = [equations[i][0] if type(equations[i])==tuple else equations[i] for i in range(start_line, end_line)]
    print(dict_equatons)  
    return dict_equatons

def chunk_words(s, n):
    words = s.split()
    return [' '.join(words[i:i+n]) for i in range(0, len(words), n)]


def copy_animation(frame_height, fps, bg_path):
    source_file = f'./media/videos/{int(frame_height)}p{int(fps)}/EquationAnimation.mp4'
    
    if not os.path.exists(source_file):
        C = f'ffmpeg -i {bg_path} -i ./media/videos/{int(frame_height)}p{int(fps)}/EquationAnimation.mov  -r {fps} -filter_complex "[0:v][1:v] overlay=0:0" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p ./media/videos/{int(frame_height)}p{int(fps)}/EquationAnimation.mp4'
        subprocess.call(C, shell=True)
    
    
    destination_file = "./downloads/EquationAnimation.mp4"
    
    video = VideoFileClip(source_file)
    print(f"Video duration: {video.duration} seconds")
    
    if video.duration > 60:
        part_1 = f'ffmpeg -i {source_file} -r {fps} -t 50 -async 1 -c copy ./downloads/EquationAnimation_first_half.mp4'
        subprocess.call(part_1, shell=True)
        part_2 = f'ffmpeg -i {source_file} -r {fps} -ss 00:00:50 -async 1 -c copy ./downloads/EquationAnimation_second_half.mp4'
        
        subprocess.call(part_2, shell=True)
    else:
        if shutil.copy2(source_file, destination_file):
            print("Copied successfully!")
        


class EquationAnimation(MovingCameraScene):
    fh = 16
    fw = 16
    ph = 1600
    pw = 1600
    fr = 120
    bo = 0
    def __init__(self, file_sol, file_tikz, **kwargs):
        self.file_sol = file_sol
        self.file_tikz = file_tikz  

        super().__init__(**kwargs)
        
    config.frame_height = fh
    config.frame_width = fw
    config.pixel_height = ph
    config.pixel_width = pw
    config.frame_rate = fr
    config.background_opacity = bo
    config.movie_file_extension = '.mov'
    def construct(self):
        Tex.set_default(color=BLACK)
        Mobject.set_default(color=BLACK)
		
        H = 16
        W = 16
        
        custom_template = TexTemplate()
        custom_template.add_to_preamble(r"\usepackage{v-test-paper}")
        equations = solution_to_align(file_sol=self.file_sol)
        image = solution_to_tikz(file_sol=self.file_sol, file_tikz=self.file_tikz)
        title = Tex(r'\texttt{Solution}', tex_template=custom_template).scale(0.8).to_edge(UP)
        self.add(title)
        
        N = len(equations)
        PL = None
        
        if image:
            image = ImageMobject(image)
            if image.height > image.width:
                image.height = 0.5*H
            else:
                image.width = 0.65*W
            PL = image.get_bottom()
            self.play(FadeIn(image))
            self.wait(2)
            N += 1
        else:
            PL = ([0, 0.25*H, 0])
            
        
        for value in equations.values():
            
            if len(value) == 1:
                tex_string = value[0].replace(r'\intertext{', r'{$\Rightarrow \quad$')
                tex_string = '\\\\'.join(chunk_words(tex_string, 15))
                L = Tex(tex_string, tex_template=custom_template).scale(0.7).next_to(([-0.5*W, PL[1] - 1.5, 0]), RIGHT, buff=1)
                
                
                self.play(
                    self.camera.frame.animate.move_to(([0, L.get_y(), 0])),
                    Create(L),
                    run_time=0.03*len(L.get_tex_string())
                )
                PL = L.get_bottom()
            else:
                ML = [i + r'[2mm]' if i.endswith(r'\\') else i for i in value[1:] ]
                tex_string = value[0].replace(r'\intertext{', r'{$\Rightarrow \quad$')
                tex_string = '\\\\'.join(chunk_words(tex_string, 15))
                T = Tex(tex_string, tex_template=custom_template).scale(0.7).next_to(([-0.5*W, PL[1] - 1.5, 0]), RIGHT, buff=1)
                
                PL = T.get_bottom()
                L = MathTex(*ML, tex_template=custom_template).scale(0.8).next_to(([0, PL[1], 0]), DOWN, buff=0.5)
                PL = L.get_bottom()
                     
                self.play(
                    self.camera.frame.animate.move_to(([0, T.get_y(), 0])),
                    Create(T),
                    run_time=0.05*len(T.get_tex_string())
                )
                
                for i in range(len(L)):
                    self.play(
                        self.camera.frame.animate.move_to(([0, L[i].get_y(), 0])),
                        Create(L[i]),
                        run_time=0.05*len(L[i].get_tex_string())
                    )
                    self.wait(0.5)
             
            self.wait(1.5)       
            
                    
        
        self.play(self.camera.frame.animate.move_to(ORIGIN))
        self.wait()
        self.play(self.camera.frame.animate.move_to(([0, PL[1], 0])), run_time=2*N, rate_func=linear)
        circle = Circle(color=WHITE, radius=0.1, fill_opacity=1).move_to(([0, PL[1], 0]))
        self.play(
            circle.animate.scale(120)
            )
        self.play(
            Create(Tex(r'\texttt{@10xphysics}', tex_template=custom_template).scale(0.7).move_to(([0, PL[1], 0])))
        )
        self.wait(1)
        
        
        
        
        

    
    
        

            


       

        



    
import os 
import subprocess

class AutomaticLatex(object):
    def __init__(self, latex_file_directory, latex_name, image_directory):
        
        self.image_directory = image_directory
        os.makedirs(image_directory, exist_ok=True)
        self.latex_file_directory = latex_file_directory
        self.latex_name = latex_name

        # LaTeX document preamble
        self.latex_code = """
                \\documentclass{article}
                \\usepackage{graphicx}
                \\usepackage{subcaption}

                \\begin{document}

                """
    
    
    def _add_image(self, image_name, width_factor, from_image_directory = True):
        # Add image to the LaTeX code
        if from_image_directory:
            image_path = os.path.join(self.image_directory, image_name)
        else:
            image_path = image_name
        self.latex_code += f"\\includegraphics[width={width_factor}\\linewidth]{{{image_path}}}\n"
    
    def _begin_figure(self):     
        self.latex_code += """\\begin{figure}[ht]
                            \\centering\n"""
    
    def _begin_subfigure(self, width_factor): 
        self.latex_code += f"""\\begin{{subfigure}}[b]{{{width_factor}\\linewidth}}
                            \\centering\n"""
    
    def _end_subfigure(self):
        self.latex_code += """\\end{subfigure}
                            \\hfill\n"""
        
    def _vertical_space(self):
        self.latex_code += """\vspace{1em}\n"""
    
    def _add_caption(self, title):
        if title != "":
            self.latex_code += "        \\caption{" + str(title) + "}\n"
    
    def _end_figure(self):
        self.latex_code += """\\end{figure}\n"""
    
    
    def add_text(self, text):
        assert type(text) == str
        self.latex_code += text
    
    def add_figure_one_image(self, image_name, title = "", width_factor=0.95, from_image_directory = True):
        self._begin_figure()
        
        self._add_image(image_name, width_factor, from_image_directory = from_image_directory)
        self._add_caption(title)
        
        self._end_figure()
    
    def add_figure_several_images(self, image_name_list, title="", width_factor_list=None):
        assert len(image_name_list) > 1
        
        if title == None:
            title = ""
        
        if width_factor_list == None:
            width_factor_list = [0.9 / len(image_name_list)] * len(image_name_list)
            
        if type(width_factor_list) in [float, int, torch.float32, torch.int]:
            width_factor_list = [width_factor_list] * len(image_name_list)
        
        assert type(title) == str
        assert len(image_name_list) == len(width_factor_list)
        
        self._begin_figure()
        
        for image_name, width_factor in zip(image_name_list, width_factor_list):
            self._add_image(image_name, width_factor)
        self._add_caption(title)
        
        self._end_figure()
    
    
    def add_figure_subfigures(self, image_name_matrix, title_list = None, width_factor_matrix = None, 
                               width_factor_subfigure_list = 1):
        n_subfigure = len(image_name_matrix)
        assert n_subfigure >= 1
        
        if width_factor_matrix == None:
            width_factor_matrix = [[0.9 / n_subfigure]] * n_subfigure
        
        if type(width_factor_subfigure_list) in [float, int]:
            width_factor_subfigure_list = [width_factor_subfigure_list] * n_subfigure
        
        if title_list == None or title_list == "":
            title_list = [""] * len(image_name_matrix)
        assert n_subfigure == len(title_list)
        assert n_subfigure == len(width_factor_matrix)
        assert n_subfigure == len(width_factor_subfigure_list)
        
        
        for title in title_list:
            assert type(title) == str
        
        self._begin_figure()
        
        for image_name_list, title, width_factor_list, width_factor_subfig in zip(image_name_matrix, title_list, width_factor_matrix, width_factor_subfigure_list):
            self._begin_subfigure(width_factor = width_factor_subfig)
            
            for image_name, width_factor in zip(image_name_list, width_factor_list):
                self._add_image(image_name, width_factor)
            self._add_caption(title)
            
            self._end_subfigure()
        
        self._end_figure()
        
    def save_latex(self):
        # LaTeX document closing
        self.latex_code += """\\end{document}"""

        # Save LaTeX code to a .tex file
        complete_latex_file_path = os.path.join(self.latex_file_directory, self.latex_name + '.tex')
        with open(complete_latex_file_path, 'w') as latex_file:
            latex_file.write(self.latex_code)

        print(f"LaTeX document saved to {complete_latex_file_path}")

    def run_latex(self):
        complete_latex_file_directory = os.path.join(self.latex_file_directory, self.latex_name + '.tex')
        tex_name = complete_latex_file_directory
        # Compile LaTeX document
        subprocess.run(['pdflatex', '-output-directory', self.latex_file_directory, complete_latex_file_directory])

       
        print(os.path.join(self.latex_file_directory, self.latex_name + '.aux'))
        print(os.path.join(self.latex_file_directory, self.latex_name + '.log'))
        # Clean up auxiliary files generated by LaTeX
        subprocess.run(['rm', os.path.join(self.latex_file_directory, self.latex_name + '.aux'), 
                        os.path.join(self.latex_file_directory, self.latex_name + '.log')])

        print("LaTeX document compiled!")

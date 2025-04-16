import sys
import re
import markdown
from markdown.extensions import Extension

class LatexRenderer(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')
        md.postprocessors.deregister('raw_html')

def convert_md_to_tex(md_file, tex_file):
    """Convert markdown file to LaTeX file."""
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    # Convert headers
    latex_content = md_content
    latex_content = re.sub(r'^# (.*)$', r'\\section{\1}', latex_content, flags=re.MULTILINE)
    latex_content = re.sub(r'^## (.*)$', r'\\subsection{\1}', latex_content, flags=re.MULTILINE)
    latex_content = re.sub(r'^### (.*)$', r'\\subsubsection{\1}', latex_content, flags=re.MULTILINE)
    
    # Convert lists
    in_list = False
    lines = latex_content.split('\n')
    for i, line in enumerate(lines):
        if re.match(r'^[\-\*] ', line):
            if not in_list:
                lines[i] = '\\begin{itemize}\n' + line.replace('- ', '\\item ').replace('* ', '\\item ')
                in_list = True
            else:
                lines[i] = line.replace('- ', '\\item ').replace('* ', '\\item ')
        elif re.match(r'^\d+\. ', line):
            if not in_list:
                lines[i] = '\\begin{enumerate}\n\\item ' + line[3:]
                in_list = True
            else:
                lines[i] = '\\item ' + line[3:]
        elif in_list:
            list_type = 'itemize' if lines[i-1].startswith('\\item') and not re.match(r'^\\item \d', lines[i-1]) else 'enumerate'
            lines[i-1] += f'\n\\end{{{list_type}}}'
            in_list = False
    latex_content = '\n'.join(lines)
    
    # Convert formatting
    latex_content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', latex_content)
    latex_content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', latex_content)
    latex_content = re.sub(r'`(.*?)`', r'\\texttt{\1}', latex_content)
    
    # Convert code blocks
    # Handle code blocks with proper verbatim environment
    latex_content = re.sub(r'```.*?\n(.*?)```', r'\\begin{verbatim}\n\1\\end{verbatim}\n', latex_content, flags=re.DOTALL)
    # Convert math expressions
    latex_content = re.sub(r'\\\((.*?)\\\)', r'$\1$', latex_content)
    # Convert display math (handle multi-line equations)
    # Convert display math and remove empty lines in equations
    latex_content = re.sub(r'\\\[(.*?)\\\]', lambda m: '\\begin{equation}' + m.group(1).strip() + '\\end{equation}', latex_content, flags=re.DOTALL)
    
    # Convert markdown horizontal rules to LaTeX
    latex_content = re.sub(r'^---\s*$', r'\\hrulefill', latex_content, flags=re.MULTILINE)
    
    # Clean up all remaining formatting artifacts
    latex_content = re.sub(r'\\texttt\{\}\n?', '', latex_content)
    latex_content = latex_content.replace('`', '')
    
    # Add document structure
    latex_content = f"""\\documentclass{{article}}
\\begin{{document}}
{latex_content}
\\end{{document}}"""
    
    with open(tex_file, 'w') as f:
        f.write(latex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python md2tex.py input.md output.tex")
        sys.exit(1)
    
    input_md = sys.argv[1]
    output_tex = sys.argv[2]
    convert_md_to_tex(input_md, output_tex)
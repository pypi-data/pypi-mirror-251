import os
import subprocess
    

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, "template")

    comando_cookiecutter = f"cookiecutter {template_dir} --output-dir . --no-input"

    subprocess.run(comando_cookiecutter, shell=True, check=True)

    print(f"Template criado com sucesso")

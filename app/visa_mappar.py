import os

def visa_mappstruktur(startpath):
    print(f"\n--- DIN MAPPSTRUKTUR FÖR: {os.path.abspath(startpath)} ---\n")
    
    for root, dirs, files in os.walk(startpath):
        # Vi hoppar över "skräp-mappar" som venv, .git och __pycache__ för att göra det läsbart
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode', 'instance']]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '    ' * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = '    ' * (level + 1)
        for f in files:
            # Visa inte .pyc filer eller .DS_Store (Mac skräp)
            if not f.endswith('.pyc') and not f.startswith('.'):
                print(f"{subindent}{f}")

if __name__ == "__main__":
    # Punkt (.) betyder "denna mapp vi är i nu"
    visa_mappstruktur('.')
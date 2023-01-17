import sys
import subprocess
import importlib
import importlib.metadata
import importlib.util

sys.dont_write_bytecode = True

def install_packages() -> None:
    print(' * Verifying packages', end='\n\n')

    packages = open('data/requirements.txt').readlines()

    for package in packages:
        if package.startswith('#') or '==' not in package:
            continue

        (package, version) = package.strip().split('==')
        redo = importlib.util.find_spec(package.replace('-', '_')) is None

        if not redo and importlib.metadata.version(package) != version:
            subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', package], capture_output=True)
            redo = True

        if redo:
            print(f' * Installing {package} .......... ', end='', flush=True)
            stdout = subprocess.run([sys.executable, '-m', 'pip', 'install', f'{package}=={version}'], capture_output=True, text=True).stdout

            if 'Successfully installed' not in stdout:
                exit('FAIL')
            print('OK')
import os
import subprocess
import shutil
import sys

if __name__ == "__main__":
    force = "--force" in sys.argv

    with open("requirements.txt", "r") as f:
        packages = f.readlines()

    for root, dirs, files in os.walk("."):
        for d in dirs:
            if len(d.split("-")) != 2:
                continue
            for p in packages:
                package = p.strip()
                if package == "" or package[0] == "#":
                    continue
                target_py, target_os = d.split("-")
                target_path = f"./{target_py}-{target_os}/{package}"
                if os.path.exists(target_path):
                    if force:
                        shutil.rmtree(target_path)
                    else:
                        continue
                os.makedirs(target_path)
                result = subprocess.run(["pip-download", "-py", target_py, "-p", target_os, package], cwd=target_path)
                if result.returncode < 0:
                    continue
                with open(f"{target_path}/install.bat", "w") as f:
                    f.write(f"python -m pip install {package} --no-index --find-link .")
        break

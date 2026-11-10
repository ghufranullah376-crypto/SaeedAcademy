import sys, os, subprocess
out = []
out.append(f"python: {sys.version}")
out.append(f"exe: {sys.executable}")
try:
    import PIL
    out.append(f"PIL_OK: {PIL.__version__}")
except Exception as e:
    out.append(f"PIL_FAIL: {type(e).__name__}: {e}")
# try pip show
try:
    r = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True, timeout=60)
    out.append("pip: " + r.stdout.strip() + r.stderr.strip())
except Exception as e:
    out.append(f"pip_fail: {e}")
txt = "\n".join(out)
path = os.path.join(os.path.dirname(__file__), "__check_out.txt")
with open(path, "w") as f:
    f.write(txt)
print("WROTE", path)

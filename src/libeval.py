# Authored by Arjun Guha
import subprocess
from typing import List

def run_without_exn(args: List[str]):
    """
    Runs the given program with a five second timeout. Does not throw an exception
    no matter what happens. The output is a dictionary of the format that we expect
    for our evaluation scripts. The "status" field is "OK" when the exit code is
    zero. If that isn't enough, you may want to tweak the status based on the
    captured stderr and stdout.
    """
    try: 
        output = subprocess.run(args, capture_output=True, timeout=5)
        stdout = output.stdout
        stderr = output.stderr
        exit_code = output.returncode
        status = "OK"
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout
        stderr = exc.stderr
        exit_code = -1
        status = "Timeout"
    except subprocess.CalledProcessError as exc:
        stdout = exc.stdout
        stderr = exc.stderr
        exit_code = exc.returncode
        status = "Exception"

    if stdout is None:
        stdout = b""
    if stderr is None:
        stderr = b""
    return {
        "status": status,
        "exit_code": exit_code,
        "stdout": stdout.decode("utf-8", errors="ignore"),
        "stderr": stderr.decode("utf-8", errors="ignore"),
    }
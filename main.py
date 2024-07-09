import subprocess

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(f"Output of {script_name}:\n{result.stdout}")
    if result.stderr:
        print(f"Errors in {script_name}:\n{result.stderr}")

if __name__ == "__main__":
    scripts_to_run = [
        'teste_infra_s_a.py',
        'teste_porto_são_francisco_do_sul.py'
    ]

    for script in scripts_to_run:
        run_script(script)

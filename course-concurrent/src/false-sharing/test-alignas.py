import subprocess
import csv

source_file = "alignas.cpp"
executable = "./a.out"

output_csv = "output.csv"

headers = ["SIZE", "Output"]

def compile_and_run(size):
    compile_command = ["g++", "-std=c++17", f"-DSIZE={size}", source_file, "-o", executable]
    try:
        subprocess.run(compile_command, check=True)
        print(f"Exécution avec SIZE={size}...")
        result = subprocess.run(executable, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la compilation ou l'exécution avec SIZE={size}: {e}")
        return None

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for size in range(10):
        output = compile_and_run(2**size)
        if output is not None:
            writer.writerow([2**size, output])

print(f"Les résultats ont été enregistrés dans {output_csv}.")

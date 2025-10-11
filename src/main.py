import sys
from typing import List, Dict, Any, Tuple
from . import parser
from .algorithm.hill_climbing import HillClimbing, HillClimbingResult

def print_summary(data: dict) -> None:
    print("Hasil parsing input:\n")

    kelas_list = data['kelas_mata_kuliah']
    print(f"Kelas mata kuliah ({len(kelas_list)}):")
    for k in kelas_list:
        print(f"  - {k['kode']}: jumlah_mahasiswa={k['jumlah_mahasiswa']}, sks={k['sks']}")

    ruangan_list = data['ruangan']
    print(f"\nRuangan ({len(ruangan_list)}):")
    for r in ruangan_list:
        print(f"  - {r['kode']}: kuota={r['kuota']}")

    mahasiswa_list = data['mahasiswa']
    print(f"\nMahasiswa ({len(mahasiswa_list)}):")
    for m in mahasiswa_list:
        print(f"  - {m['nim']}: daftar_mk={m['daftar_mk']}, prioritas={m['prioritas']}")

def print_schedule(schedule: List[Dict[str, Any]], title: str):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

    rooms = {}
    for meeting in schedule:
        room = meeting['room']
        if room not in rooms:
            rooms[room] = []
        rooms[room].append(meeting)

    for room, meetings in sorted(rooms.items()):
        print(f"\nRuang: {room}")
        print(f"{'Jam':<5} {'Senin':<15} {'Selasa':<15} {'Rabu':<15} {'Kamis':<15} {'Jumat':<15}")
        print("-" * 85)
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        for hour in range(7, 18):
            row = [f"{hour:<5}"]
            for day in days:
                meeting_code = ""
                for m in meetings:
                    if m['day'] == day and m['start'] <= hour < m['start'] + m['duration']:
                        meeting_code = m['kode']
                        break
                row.append(f"{meeting_code:<15}")
            print("".join(row))


def print_result_summary(result: HillClimbingResult, algorithm_name: str, run_num: int):
    print(f"\n{'='*60}")
    print(f"{algorithm_name} (Run {run_num}) - HASIL EKSPERIMEN")
    print(f"{'='*60}")
    print(f"Nilai Objective Function Awal: {result.initial_value:.2f}")
    print(f"Nilai Objective Function Akhir: {result.final_value:.2f}")
    print(f"Improvement: {result.initial_value - result.final_value:.2f}")
    print(f"Jumlah Iterasi: {result.iterations}")
    print(f"Durasi: {result.duration:.4f} detik")

    if hasattr(result, 'sideways_moves') and result.sideways_moves > 0:
        print(f"Sideways Moves: {result.sideways_moves}")

    if hasattr(result, 'restarts') and result.restarts > 0:
        print(f"Jumlah Restart: {result.restarts}")
        print(f"Iterasi per Restart: {result.iterations_per_restart}")


def print_statistics(results: List[HillClimbingResult], algorithm_name: str, num_runs: int):
    print(f"\n{'='*60}")
    print(f"RINGKASAN {algorithm_name} ({num_runs} runs)")
    print(f"{'='*60}")

    final_values = [r.final_value for r in results]
    iterations = [r.iterations for r in results]
    durations = [r.duration for r in results]

    print(f"\nNilai Objective Function Akhir:")
    print(f"  Min: {min(final_values):.2f}")
    print(f"  Max: {max(final_values):.2f}")
    print(f"  Rata-rata: {sum(final_values)/len(final_values):.2f}")

    print(f"\nJumlah Iterasi:")
    print(f"  Min: {min(iterations)}")
    print(f"  Max: {max(iterations)}")
    print(f"  Rata-rata: {sum(iterations)/len(iterations):.1f}")

    print(f"\nDurasi:")
    print(f"  Min: {min(durations):.4f} detik")
    print(f"  Max: {max(durations):.4f} detik")
    print(f"  Rata-rata: {sum(durations)/len(durations):.4f} detik")

def get_int_input(prompt: str, default: int, min_val: int = 1) -> int:
    while True:
        try:
            user_input = input(f"{prompt} (default={default}): ").strip()
            if user_input == "":
                return default
            value = int(user_input)
            if value < min_val:
                print(f"Nilai harus >= {min_val}. Coba lagi.")
                continue
            return value
        except ValueError:
            print("Input tidak valid. Masukkan angka.")

def get_objective_type() -> str:
    print("\n" + "="*60)
    print("Pilih Objective Function:")
    print("="*60)
    print("1. Student Conflict")
    print("2. Room Conflict")
    print("3. Room Capacity")
    print("4. Combined (semua)")

    while True:
        choice = input("Pilihan (1-4, default=4): ").strip()
        if choice == "" or choice == "4":
            return "combined"
        elif choice == "1":
            return "student_conflict"
        elif choice == "2":
            return "room_conflict"
        elif choice == "3":
            return "capacity"
        else:
            print("Pilihan tidak valid. Coba lagi.")

def select_algorithm() -> Tuple[str, int]:
    print("\n" + "="*60)
    print("PILIH ALGORITMA HILL CLIMBING")
    print("="*60)
    print("1. Steepest Ascent Hill Climbing")
    print("2. Stochastic Hill Climbing")
    print("3. Hill Climbing with Sideways Move")
    print("4. Random Restart Hill Climbing")
    print("0. Jalankan Semua Algoritma")

    while True:
        choice = input("\nPilihan (0-4): ").strip()
        if choice in ["0", "1", "2", "3", "4"]:
            choice_num = int(choice)
            if choice_num == 0:
                return "ALL", 0
            elif choice_num == 1:
                return "Steepest Ascent Hill Climbing", 1
            elif choice_num == 2:
                return "Stochastic Hill Climbing", 2
            elif choice_num == 3:
                return "Hill Climbing with Sideways Move", 3
            elif choice_num == 4:
                return "Random Restart Hill Climbing", 4
        else:
            print("Pilihan tidak valid. Coba lagi.")

def get_algorithm_parameters(choice_num: int) -> Dict[str, Any]:
    params = {}

    if choice_num == 3:
        print("\n--- Parameter untuk Sideways Move ---")
        params['max_sideways'] = get_int_input("Maximum Sideways Moves", 100, 1)
    elif choice_num == 4:
        print("\n--- Parameter untuk Random Restart ---")
        params['max_restarts'] = get_int_input("Maximum Restarts", 10, 1)
        params['max_iterations_per_restart'] = get_int_input("Maximum Iterations per Restart", 100, 1)

    return params

def run_algorithm(hc: HillClimbing, choice_num: int, params: Dict[str, Any]) -> HillClimbingResult:
    if choice_num == 1:
        return hc.steepest_ascent()
    elif choice_num == 2:
        return hc.stochastic()
    elif choice_num == 3:
        return hc.sideways_move(**params)
    elif choice_num == 4:
        return hc.random_restart(**params)
    else:
        raise ValueError(f"Unknown algorithm choice: {choice_num}")


def run_experiment(data: dict, algorithm_name: str, choice_num: int,
                   params: Dict[str, Any], num_runs: int, objective_type: str):
    print(f"\n{'#'*60}")
    print(f"EKSPERIMEN: {algorithm_name}")
    if params:
        print(f"Parameter: {params}")
    print(f"{'#'*60}")

    results = []
    for run in range(num_runs):
        print(f"\n--- Run {run + 1}/{num_runs} ---")
        hc = HillClimbing(data, objective_type=objective_type)
        result = run_algorithm(hc, choice_num, params)
        results.append(result)
        print_result_summary(result, algorithm_name, run + 1)

        print_schedule(result.initial_state, "STATE AWAL (Run 1)")
        print_schedule(result.final_state, "STATE AKHIR (Run 1)")

        print(f"\n{'='*60}")
        print(f"OBJECTIVE FUNCTION HISTORY (Run 1)")
        print(f"{'='*60}")
        print(f"Iterasi -> Nilai")
        for i, val in enumerate(result.objective_history):
            print(f"{i:3d}     -> {val:.2f}")

    print_statistics(results, algorithm_name, num_runs)
    return results


def run_all_algorithms(data: dict, num_runs: int, objective_type: str):
    algorithms = [
        ("Steepest Ascent Hill Climbing", 1, {}),
        ("Stochastic Hill Climbing", 2, {}),
        ("Hill Climbing with Sideways Move", 3, {'max_sideways': 100}),
        ("Random Restart Hill Climbing", 4, {'max_restarts': 10, 'max_iterations_per_restart': 100}),
    ]

    all_results = {}
    for algo_name, choice_num, params in algorithms:
        results = run_experiment(data, algo_name, choice_num, params, num_runs, objective_type)
        best_result = min(results, key=lambda r: r.final_value)
        all_results[algo_name] = best_result

    print(f"\n{'='*60}")
    print("TABEL PERBANDINGAN HASIL TERBAIK")
    print(f"{'='*60}")
    print(f"{'Algoritma':<40} {'Nilai Akhir':<15} {'Iterasi':<10} {'Durasi (s)':<15}")
    print("-"*80)
    for algo, result in all_results.items():
        print(f"{algo:<40} {result.final_value:<15.2f} {result.iterations:<10} {result.duration:<15.4f}")

def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python -m src.main <input.json>")
        return 1

    path = argv[1]
    try:
        data = parser.load_and_parse(path)
    except Exception as e:
        print(f"Failed to read JSON file '{path}': {e}")
        return 1

    print(f"\nData loaded from: {path}")
    print_summary(data)

    objective_type = get_objective_type()
    num_runs = get_int_input("\nJumlah run per algoritma", 3, 1)
    algorithm_name, choice_num = select_algorithm()

    if algorithm_name == "ALL":
        run_all_algorithms(data, num_runs, objective_type)
    else:
        params = get_algorithm_parameters(choice_num)
        run_experiment(data, algorithm_name, choice_num, params, num_runs, objective_type)

    print("\n" + "="*60)
    print("EKSPERIMEN SELESAI!")
    print("="*60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

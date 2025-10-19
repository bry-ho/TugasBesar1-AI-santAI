from typing import List, Dict, Any, Union
from .algorithm.hill_climbing import HillClimbingResult
from .algorithm.simulated_annealing import SimulatedAnnealingResult
from .algorithm.genetic import GeneticResult

AlgorithmResult = Union[HillClimbingResult, SimulatedAnnealingResult, GeneticResult]

# Summary hasil parsing data
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


# Print schedule dalam format tabel
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


# Print hasil algoritma hill climbing
def print_hill_climbing_result(result: HillClimbingResult, algorithm_name: str, run_num: int):
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

# Print hasil algoritma simulated annealing
def print_simulated_annealing_result(result: SimulatedAnnealingResult, algorithm_name: str, run_num: int):
    print(f"\n{'='*60}")
    print(f"{algorithm_name} (Run {run_num}) - HASIL EKSPERIMEN")
    print(f"{'='*60}")
    print(f"Nilai Objective Function Awal: {result.initial_value:.2f}")
    print(f"Nilai Objective Function Akhir: {result.final_value:.2f}")
    print(f"Improvement: {result.initial_value - result.final_value:.2f}")
    print(f"Jumlah Iterasi: {result.iterations}")
    print(f"Durasi: {result.duration:.4f} detik")
    print(f"Temperature Awal: {result.initial_temperature:.2f}")
    print(f"Temperature Akhir: {result.final_temperature:.2f}")
    print(f"Accepted Moves: {result.accepted_moves}")
    print(f"Rejected Moves: {result.rejected_moves}")
    if result.accepted_moves + result.rejected_moves > 0:
        acceptance_rate = result.accepted_moves / (result.accepted_moves + result.rejected_moves) * 100
        print(f"Acceptance Rate: {acceptance_rate:.2f}%")

# Print hasil algoritma genetic
def print_genetic_result(result: GeneticResult, run_num: int):
    print(f"\n{'='*60}")
    print(f"Genetic Algorithm (Run {run_num}) - HASIL EKSPERIMEN")
    print(f"{'='*60}")
    print(f"Nilai Objective Function Awal: {result.initial_value:.2f}")
    print(f"Nilai Objective Function Akhir: {result.final_value:.2f}")
    print(f"Improvement: {result.initial_value - result.final_value:.2f}")
    print(f"Jumlah Iterasi: {result.iterations}")
    print(f"Durasi: {result.duration:.4f} detik")
    print(f"Ukuran Populasi: {result.population_size}")
    print(f"Final Average Fitness: {result.average_fitness_history[-1]:.2f}")


__all__ = [
    'print_summary', 'print_schedule', 'AlgorithmResult', 'print_hill_climbing_result', 'print_simulated_annealing_result', 'print_genetic_result'
]
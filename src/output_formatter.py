from typing import List, Dict, Any, Union
from .algorithm.hill_climbing import HillClimbingResult
from .algorithm.simulated_annealing import SimulatedAnnealingResult

AlgorithmResult = Union[HillClimbingResult, SimulatedAnnealingResult]

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

# Print result summary untuk semua jenis algoritma
def print_result_summary(result: AlgorithmResult, algorithm_name: str, run_num: int):
    if isinstance(result, HillClimbingResult):
        print_hill_climbing_result(result, algorithm_name, run_num)
    elif isinstance(result, SimulatedAnnealingResult):
        print_simulated_annealing_result(result, algorithm_name, run_num)
    else:
        # buat genetic algorithm nanti
        print(f"\n{'='*60}")
        print(f"{algorithm_name} (Run {run_num}) - HASIL EKSPERIMEN")
        print(f"{'='*60}")
        print(f"Nilai Objective Function Awal: {result.initial_value:.2f}")
        print(f"Nilai Objective Function Akhir: {result.final_value:.2f}")
        print(f"Improvement: {result.initial_value - result.final_value:.2f}")
        print(f"Jumlah Iterasi: {result.iterations}")
        print(f"Durasi: {result.duration:.4f} detik")

# Print statistik
def print_statistics(results: List[AlgorithmResult], algorithm_name: str, num_runs: int):
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

# Print history objective function
def print_objective_history(result: AlgorithmResult, run_num: int):
    print(f"\n{'='*60}")
    print(f"OBJECTIVE FUNCTION HISTORY (Run {run_num})")
    print(f"{'='*60}")
    print(f"Iterasi -> Nilai")
    for i, val in enumerate(result.objective_history):
        print(f"{i:3d}     -> {val:.2f}")

# Print temp history
def print_temperature_history(result: SimulatedAnnealingResult, run_num: int):
    if hasattr(result, 'temperature_history') and result.temperature_history:
        print(f"\n{'='*60}")
        print(f"TEMPERATURE HISTORY (Run {run_num})")
        print(f"{'='*60}")
        print(f"Iterasi -> Temperature")
        for i, temp in enumerate(result.temperature_history):
            if i % max(1, len(result.temperature_history) // 20) == 0:  # Show every nth value
                print(f"{i:3d}     -> {temp:.4f}")

# Print final schedule summary
def print_final_schedule_summary(result: AlgorithmResult, algorithm_name: str, run_num: int = None):
    run_text = f"(Run {run_num})" if run_num else ""
    print(f"\n{'='*80}")
    print(f"RINGKASAN JADWAL AKHIR - {algorithm_name} {run_text}")
    print(f"{'='*80}")
    
    schedule = result.final_state
    
    # Count meetings per day
    day_counts = {}
    room_usage = {}
    for meeting in schedule:
        day = meeting['day']
        room = meeting['room']
        day_counts[day] = day_counts.get(day, 0) + 1
        room_usage[room] = room_usage.get(room, 0) + meeting['duration']
    
    print(f"Total Meetings: {len(schedule)}")
    print(f"Objective Function Value: {result.final_value:.2f}")
    
    print(f"\nDistribusi Pertemuan per Hari:")
    for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']:
        count = day_counts.get(day, 0)
        print(f"  {day}: {count} pertemuan")
    
    print(f"\nPenggunaan Ruangan (total jam):")
    for room, hours in sorted(room_usage.items()):
        print(f"  {room}: {hours} jam")

# Print tabel perbandingan untuk semua jenis algoritma
def print_comparison_table(results_dict: Dict[str, AlgorithmResult]):
    print(f"\n{'='*60}")
    print("TABEL PERBANDINGAN HASIL TERBAIK")
    print(f"{'='*60}")
    print(f"{'Algoritma':<40} {'Nilai Akhir':<15} {'Iterasi':<10} {'Durasi (s)':<15}")
    print("-" * 80)
    for algo, result in results_dict.items():
        print(f"{algo:<40} {result.final_value:<15.2f} {result.iterations:<10} {result.duration:<15.4f}")

# Export public API
__all__ = [
    'print_summary', 'print_schedule', 'print_result_summary', 
    'print_statistics', 'print_objective_history', 'print_temperature_history',
    'print_comparison_table', 'print_final_schedule_summary', 'AlgorithmResult'
]
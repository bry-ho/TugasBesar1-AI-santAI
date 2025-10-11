import sys
from typing import List

from . import parser


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

# Usage: python3 src/main.py <input.json>
def main(argv: List[str]) -> int:
    path = argv[1]
    try:
        data = parser.load_and_parse(path)
    except Exception as e:
        print(f"Failed to read JSON file '{path}': {e}")
        return 1

    print_summary(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

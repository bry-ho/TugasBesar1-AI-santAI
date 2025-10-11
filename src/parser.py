import json
from typing import Any, Dict, List

def load_json(path: str) -> Dict[str, Any]:
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)

def _int_checker(v: Any, default: int = 0) -> int:
	try:
		return int(v)
	except Exception:
		return default

def _normalize_kelas(item: Dict[str, Any]) -> Dict[str, Any]:
	kode = str(item.get("kode", "")).strip()
	jumlah_mahasiswa = _int_checker(item.get("jumlah_mahasiswa"), 0)
	sks = _int_checker(item.get("sks"), 0)
	return {"kode": kode, "jumlah_mahasiswa": jumlah_mahasiswa, "sks": sks}

def _normalize_ruangan(item: Dict[str, Any]) -> Dict[str, Any]:
	kode = item.get("kode")
	if kode is None or str(kode).strip() == "":
		kode = str(item.get("name") or item.get("nama") or "").strip()
	kode = str(kode)
	kuota = _int_checker(item.get("kuota"), 0)
	return {"kode": kode, "kuota": kuota}

def _normalize_mahasiswa(item: Dict[str, Any]) -> Dict[str, Any]:
	nim = str(item.get("nim", "")).strip()
	daftar_mk = item.get("daftar_mk") or item.get("daftar_matkul") or []
	daftar_mk = [str(x) for x in daftar_mk]
	prioritas = item.get("prioritas") or []
	seen = set()
	cleaned: List[int] = []
	for p in prioritas:
		try:
			pi = int(p)
		except Exception:
			continue
		if pi in seen:
			continue
		seen.add(pi)
		cleaned.append(pi)
	return {"nim": nim, "daftar_mk": daftar_mk, "prioritas": cleaned}

def parse_data(data: Dict[str, Any]) -> Dict[str, Any]:
	output: Dict[str, Any] = {}

	kmk = data.get("kelas_mata_kuliah") or data.get("kelas") or []
	output["kelas_mata_kuliah"] = [_normalize_kelas(x) for x in kmk]

	ruangan = data.get("ruangan") or data.get("ruang") or []
	output["ruangan"] = [_normalize_ruangan(x) for x in ruangan]

	mahasiswa = data.get("mahasiswa") or data.get("mahasiswas") or []
	output["mahasiswa"] = [_normalize_mahasiswa(x) for x in mahasiswa]

	return output


def load_and_parse(path: str) -> Dict[str, Any]:
    data = load_json(path)
    return parse_data(data)

__all__ = [
	"load_json",
	"parse_data", 
	"load_and_parse",
]

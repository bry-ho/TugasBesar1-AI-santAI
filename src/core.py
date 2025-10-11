import random
import copy
from typing import List, Dict, Any

class Schedule:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.schedule = []  # List of meeting assignments
        self.days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        self.hours = list(range(7, 18))  # 7-17 (jam mulai)
        
    def initialize_random(self) -> List[Dict[str, Any]]:
        self.schedule = []
        
        for kelas in self.data['kelas_mata_kuliah']:
            sks = kelas['sks']
            
            # Split SKS into sessions
            if sks == 4:
                sessions = [2, 2]
            elif sks == 3:
                sessions = [2, 1]
            else:
                sessions = [2]
            
            for duration in sessions:
                day = random.choice(self.days)
                # Make sure end time doesn't exceed 18
                max_start = 18 - duration
                start_hour = random.randint(7, max_start)
                room = random.choice(self.data['ruangan'])['kode']
                
                self.schedule.append({
                    'kode': kelas['kode'],
                    'day': day,
                    'start': start_hour,
                    'duration': duration,
                    'room': room,
                    'jumlah_mahasiswa': kelas['jumlah_mahasiswa']
                })
        
        return self.schedule
    
    def get_neighbors(self) -> List['Schedule']:
        neighbors = []
        
        # Strategy 1: Swap two meetings
        for i in range(len(self.schedule)):
            for j in range(i + 1, len(self.schedule)):
                neighbor = copy.deepcopy(self)
                # Swap times and rooms
                neighbor.schedule[i]['day'], neighbor.schedule[j]['day'] = \
                    neighbor.schedule[j]['day'], neighbor.schedule[i]['day']
                neighbor.schedule[i]['start'], neighbor.schedule[j]['start'] = \
                    neighbor.schedule[j]['start'], neighbor.schedule[i]['start']
                neighbor.schedule[i]['room'], neighbor.schedule[j]['room'] = \
                    neighbor.schedule[j]['room'], neighbor.schedule[i]['room']
                neighbors.append(neighbor)
        
        # Strategy 2: Move one meeting to random slot
        for i in range(len(self.schedule)):
            for _ in range(3):  # Try 3 random moves per meeting
                neighbor = copy.deepcopy(self)
                meeting = neighbor.schedule[i]
                meeting['day'] = random.choice(self.days)
                max_start = 18 - meeting['duration']
                meeting['start'] = random.randint(7, max_start)
                meeting['room'] = random.choice(self.data['ruangan'])['kode']
                neighbors.append(neighbor)
        
        return neighbors


class ObjectiveFunction:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.priority_weights = {1: 1.75, 2: 1.5, 3: 1.25}
    
    def calculate_student_conflicts(self, schedule: List[Dict[str, Any]]) -> float:
        penalty = 0
        
        for mahasiswa in self.data['mahasiswa']:
            # Get all meetings for this student
            student_meetings = [m for m in schedule if m['kode'] in mahasiswa['daftar_mk']]
            
            # Check for conflicts between all pairs
            for i in range(len(student_meetings)):
                for j in range(i + 1, len(student_meetings)):
                    m1, m2 = student_meetings[i], student_meetings[j]
                    
                    if m1['day'] == m2['day']:
                        end1 = m1['start'] + m1['duration']
                        end2 = m2['start'] + m2['duration']
                        
                        # Check time overlap
                        if not (end1 <= m2['start'] or end2 <= m1['start']):
                            overlap = min(end1, end2) - max(m1['start'], m2['start'])
                            penalty += overlap
        
        return penalty
    
    def calculate_room_conflicts(self, schedule: List[Dict[str, Any]]) -> float:
        penalty = 0
        
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                m1, m2 = schedule[i], schedule[j]
                
                # Check if same room and overlapping time
                if m1['room'] == m2['room'] and m1['day'] == m2['day']:
                    end1 = m1['start'] + m1['duration']
                    end2 = m2['start'] + m2['duration']
                    
                    if not (end1 <= m2['start'] or end2 <= m1['start']):
                        overlap = min(end1, end2) - max(m1['start'], m2['start'])
                        
                        # Calculate weighted penalty based on student priorities
                        for mahasiswa in self.data['mahasiswa']:
                            if m1['kode'] in mahasiswa['daftar_mk']:
                                idx = mahasiswa['daftar_mk'].index(m1['kode'])
                                priority = mahasiswa['prioritas'][idx]
                                weight = self.priority_weights.get(priority, 1.0)
                                penalty += overlap * weight
                            
                            if m2['kode'] in mahasiswa['daftar_mk']:
                                idx = mahasiswa['daftar_mk'].index(m2['kode'])
                                priority = mahasiswa['prioritas'][idx]
                                weight = self.priority_weights.get(priority, 1.0)
                                penalty += overlap * weight
        
        return penalty
    
    def calculate_room_capacity(self, schedule: List[Dict[str, Any]]) -> float:
        penalty = 0
        
        for meeting in schedule:
            room_capacity = next(r['kuota'] for r in self.data['ruangan'] 
                               if r['kode'] == meeting['room'])
            
            if meeting['jumlah_mahasiswa'] > room_capacity:
                overflow = meeting['jumlah_mahasiswa'] - room_capacity
                penalty += overflow * meeting['duration']
        
        return penalty
    
    def calculate(self, schedule: List[Dict[str, Any]], 
                  objective_type: str = 'combined') -> float:
        if objective_type == 'student_conflict':
            return self.calculate_student_conflicts(schedule)
        elif objective_type == 'room_conflict':
            return self.calculate_room_conflicts(schedule)
        elif objective_type == 'capacity':
            return self.calculate_room_capacity(schedule)
        elif objective_type == 'combined':
            return (self.calculate_student_conflicts(schedule) + 
                    self.calculate_room_conflicts(schedule) + 
                    self.calculate_room_capacity(schedule))
        else:
            raise ValueError(f"Unknown objective_type: {objective_type}")


# Export public API
__all__ = ['Schedule', 'ObjectiveFunction']

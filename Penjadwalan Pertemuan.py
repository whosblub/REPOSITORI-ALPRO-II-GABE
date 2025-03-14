import time
import random
import heapq
import sys

class Participant:
    def __init__(self, id, availability):
        self.id = id
        self.availability = availability

class MeetingScheduler:
    def __init__(self):
        self.participants = []
    
    def add_participant(self, participant):
        self.participants.append(participant)
    
    def find_meeting_slot_naive(self, duration):
        start_time = time.time()
        
        all_slots = []
        for participant in self.participants:
            all_slots.extend(participant.availability)
        
        unique_slots = list(set(all_slots))
        unique_slots.sort()
        
        suitable_slots = []
        for slot_start, slot_end in unique_slots:
            if slot_end - slot_start < duration:
                continue
                
            is_suitable = True
            for participant in self.participants:
                participant_available = False
                for p_start, p_end in participant.availability:
                    if p_start <= slot_start and p_end >= slot_start + duration:
                        participant_available = True
                        break
                
                if not participant_available:
                    is_suitable = False
                    break
            
            if is_suitable:
                suitable_slots.append((slot_start, slot_start + duration))
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return suitable_slots, execution_time
    
    def find_meeting_slot_interval_tree(self, duration):
        start_time = time.time()
        
        if not self.participants:
            return [], time.time() - start_time
        
        endpoints = []
        for p_id, participant in enumerate(self.participants):
            for start, end in participant.availability:
                endpoints.append((start, 1, p_id))
                endpoints.append((end, -1, p_id))
        
        endpoints.sort()
        
        available_participants = set()
        suitable_slots = []
        potential_start = None
        
        for time_point, event_type, p_id in endpoints:
            if event_type == 1:
                available_participants.add(p_id)
                if len(available_participants) == len(self.participants) and potential_start is None:
                    potential_start = time_point
            else:
                if potential_start is not None and len(available_participants) == len(self.participants):
                    if time_point - potential_start >= duration:
                        suitable_slots.append((potential_start, potential_start + duration))
                
                available_participants.remove(p_id)
                if len(available_participants) < len(self.participants):
                    potential_start = None
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return suitable_slots, execution_time

def generate_random_availability(num_slots, max_time=100):
    slots = []
    for _ in range(num_slots):
        start = random.randint(0, max_time - 10)
        end = start + random.randint(5, 20)
        slots.append((start, end))
    return slots

def display_results(suitable_slots, execution_time, algorithm_name):
    print(f"\nHasil Pencarian ({algorithm_name}):")
    if suitable_slots:
        print(f"Ditemukan {len(suitable_slots)} slot yang cocok:")
        for i, (start, end) in enumerate(suitable_slots[:5], 1):
            print(f"  Slot {i}: Waktu {start} hingga {end}")
        
        if len(suitable_slots) > 5:
            print(f"  ...dan {len(suitable_slots) - 5} slot lainnya")
    else:
        print("Tidak ditemukan slot yang cocok untuk semua peserta.")
    
    print(f"Waktu eksekusi: {execution_time:.6f} detik")

def main():
    while True:
        print("\n=== Sistem Penjadwalan Pertemuan ===")
        print("Pilih opsi:")
        print("1. Algoritma O(n²) - Solusi Buruk")
        print("2. Algoritma Interval Tree - Solusi Baik")
        print("3. Bandingkan kedua algoritma")
        print("0. Keluar")
        
        choice = input("Masukkan pilihan (0/1/2/3): ")
        
        if choice == "0":
            print("Terima kasih telah menggunakan Sistem Penjadwalan Pertemuan. Sampai jumpa!")
            sys.exit(0)
        
        if choice not in ["1", "2", "3"]:
            print("Pilihan tidak valid. Silakan coba lagi.")
            continue
        
        try:
            num_participants = int(input("Masukkan jumlah peserta: "))
            slots_per_participant = int(input("Masukkan jumlah slot per peserta: "))
            meeting_duration = int(input("Masukkan durasi pertemuan yang dibutuhkan: "))
            
            if num_participants <= 0 or slots_per_participant <= 0 or meeting_duration <= 0:
                print("Input harus berupa angka positif. Silakan coba lagi.")
                continue
        except ValueError:
            print("Input tidak valid. Masukkan angka saja.")
            continue
        
        scheduler = MeetingScheduler()
        
        print("\nMembuat jadwal acak untuk", num_participants, "peserta...")
        for i in range(num_participants):
            availability = generate_random_availability(slots_per_participant)
            participant = Participant(i, availability)
            scheduler.add_participant(participant)
            print(f"Peserta {i}: {availability}")
        
        if choice == "1":
            print("\nMencari slot pertemuan menggunakan Algoritma O(n²)...")
            suitable_slots, execution_time = scheduler.find_meeting_slot_naive(meeting_duration)
            display_results(suitable_slots, execution_time, "Algoritma O(n²)")
            
        elif choice == "2":
            print("\nMencari slot pertemuan menggunakan Algoritma Interval Tree...")
            suitable_slots, execution_time = scheduler.find_meeting_slot_interval_tree(meeting_duration)
            display_results(suitable_slots, execution_time, "Algoritma Interval Tree")
            
        elif choice == "3":
            print("\nMembandingkan kedua algoritma...")
            
            print("\nMencari slot pertemuan menggunakan Algoritma O(n²)...")
            naive_slots, naive_time = scheduler.find_meeting_slot_naive(meeting_duration)
            display_results(naive_slots, naive_time, "Algoritma O(n²)")
            
            print("\nMencari slot pertemuan menggunakan Algoritma Interval Tree...")
            interval_slots, interval_time = scheduler.find_meeting_slot_interval_tree(meeting_duration)
            display_results(interval_slots, interval_time, "Algoritma Interval Tree")
            
            print("\n=== Perbandingan Algoritma ===")
            print(f"Algoritma O(n²): {naive_time:.6f} detik")
            print(f"Algoritma Interval Tree: {interval_time:.6f} detik")
            
            if naive_time > interval_time:
                speedup = naive_time / interval_time
                print(f"Algoritma Interval Tree lebih cepat {speedup:.2f}x dibandingkan Algoritma O(n²)")
            elif interval_time > naive_time:
                speedup = interval_time / naive_time
                print(f"Algoritma O(n²) lebih cepat {speedup:.2f}x dibandingkan Algoritma Interval Tree")
            else:
                print("Kedua algoritma memiliki kecepatan yang sama")
            
            if sorted(naive_slots) == sorted(interval_slots):
                print("Kedua algoritma memberikan hasil yang identik.")
            else:
                print("Perhatian: Kedua algoritma memberikan hasil yang berbeda!")
                print(f"Algoritma O(n²): {len(naive_slots)} slot ditemukan")
                print(f"Algoritma Interval Tree: {len(interval_slots)} slot ditemukan")

if __name__ == "__main__":
    main()
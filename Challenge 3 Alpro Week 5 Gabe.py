import time

class Graph:
    def __init__(self):  # Corrected constructor
        self.graph = {}
        
    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def find_all_paths(self, start, end, max_paths=10):
        def dfs(current, path, visited):
            if len(paths) >= max_paths:
                return
                
            visited.add(current)
            path.append(current)
            
            if current == end and len(path) > 1:
                paths.append(path[:])  # Use path[:] for clarity
                visited.remove(current)  # Allow revisiting for other paths
                return
            
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    dfs(neighbor, path[:], visited)  # Use path[:] for clarity
        
        paths = []
        dfs(start, [], set())
        return paths[:max_paths]
    
    def find_all_cycles(self, start, max_cycles=5):
        cycles = []
        
        def dfs(current, path, visited):
            visited.add(current)
            path.append(current)
            
            for neighbor in self.graph[current]:
                if neighbor == start and len(path) > 2:
                    cycles.append(path[:] + [start])  # Use path[:] for clarity
                    if len(cycles) >= max_cycles:
                        return
                elif neighbor not in visited:
                    dfs(neighbor, path[:], visited)  # Use path[:] for clarity
            
            path.pop()  # Backtrack
            visited.remove(current)  # Allow revisiting for other cycles
        
        dfs(start, [], set())
        
        unique_cycles = []
        cycle_sets = set()
        
        for cycle in cycles:
            cycle_set = frozenset(cycle)
            if cycle_set not in cycle_sets:
                cycle_sets.add(cycle_set)
                unique_cycles.append(cycle)
                
        return unique_cycles[:max_cycles]
    
    def find_circuits(self, start, end):
        all_paths = self.find_all_paths(start, end, max_paths=5)
        
        if start not in self.graph or end not in self.graph[start]:
            return []
            
        circuits = []
        for path in all_paths:
            circuit = path + [start]
            circuits.append(circuit)
                
        shortest = min(circuits, key=len) if circuits else None
        longest = max(circuits, key=len) if circuits else None
        
        result = []
        if shortest:
            result.append(shortest)
        if longest and longest != shortest:
            result.append(longest)
            
        return result

def run_operation(operation_id, g):
    start_time = time.time()
    
    if operation_id == 1:
        paths_a_to_k = g.find_all_paths('A', 'K', max_paths=5)
        print("1. Semua kemungkinan Path dari A ke K:")
        for i, path in enumerate(paths_a_to_k, 1):
            print(f"   Path {i}: {' -> '.join(path)}")
    
    elif operation_id == 2:
        paths_g_to_j = g.find_all_paths('G', 'J', max_paths=5)
        print("\n2. Semua kemungkinan Path dari G ke J:")
        for i, path in enumerate(paths_g_to_j, 1):
            print(f"   Path {i}: {' -> '.join(path)}")
    
    elif operation_id == 3:
        paths_e_to_f = g.find_all_paths('E', 'F', max_paths=5)
        print("\n3. Semua kemungkinan Path dari E ke F:")
        for i, path in enumerate(paths_e_to_f, 1):
            print(f"   Path {i}: {' -> '.join(path)}")
    
    elif operation_id == 4:
        cycles_a = g.find_all_cycles('A', max_cycles=3)
        print("\n4. Semua kemungkinan Cycle jika A adalah titik awal:")
        for i, cycle in enumerate(cycles_a, 1):
            print(f"   Cycle {i}: {' -> '.join(cycle)}")
    
    elif operation_id == 5:
        cycles_k = g.find_all_cycles('K', max_cycles=3)
        print("\n5. Semua kemungkinan Cycle jika K adalah titik awal:")
        for i, cycle in enumerate(cycles_k, 1):
            print(f"   Cycle {i}: {' -> '.join(cycle)}")
    
    elif operation_id == 6:
        circuits_a_to_k = g.find_circuits('A', 'K')
        print("\n6. Circuit terpendek dan terpanjang dari A ke K:")
        if circuits_a_to_k:
            for i, circuit in enumerate(circuits_a_to_k, 1):
                print(f"   Circuit {'terpendek' if i==1 else 'terpanjang'}: {' -> '.join(circuit)} (panjang {len(circuit)-1})")
        else:
            print("   Tidak ada circuit dari A ke K")
    
    elif operation_id == 7:
        circuits_g_to_j = g.find_circuits('G', 'J')
        print("\n7. Circuit terpendek dan terpanjang dari G ke J:")
        if circuits_g_to_j:
            for i, circuit in enumerate(circuits_g_to_j, 1):
                print(f"   Circuit {'terpendek' if i==1 else 'terpanjang'}: {' -> '.join(circuit)} (panjang {len(circuit)-1})")
        else:
            print("   Tidak ada circuit dari G ke J")
    
    elif operation_id == 8:
        circuits_e_to_f = g.find_circuits('E', 'F')
        print("\n8. Circuit terpendek dan terpanjang dari E ke F:")
        if circuits_e_to_f:
            for i, circuit in enumerate(circuits_e_to_f, 1):
                print(f"   Circuit {'terpendek' if i==1 else 'terpanjang'}: {' -> '.join(circuit)} (panjang {len(circuit)-1})")
        else:
            print("   Tidak ada circuit dari E ke F")
    
    elif operation_id == 9:
        run_operation(1, g)
        run_operation(2, g)
        run_operation(3, g)
        run_operation(4, g)
        run_operation(5, g)
        run_operation(6, g)
        run_operation(7, g)
        run_operation(8, g)
        return
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nWaktu eksekusi: {execution_time:.6f} detik")

def main():
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('A', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('D', 'J')
    g.add_edge('E', 'G')
    g.add_edge('E', 'H')
    g.add_edge('F', 'I')
    g.add_edge('G', 'H')
    g.add_edge('G', 'K')
    g.add_edge('H', 'K')
    g.add_edge('I', 'J')
    g.add_edge('I', 'K')
    g.add_edge('J', 'K')
    g.add_edge('C', 'K')
    g.add_edge('E', 'K')
    g.add_edge('F', 'J')
    
    while True:
        print("\nPilih operasi yang ingin dijalankan:")
        print("1. Semua kemungkinan Path dari A ke K")
        print("2. Semua kemungkinan Path dari G ke J")
        print("3. Semua kemungkinan Path dari E ke F")
        print("4. Semua kemungkinan Cycle jika A adalah titik awal")
        print("5. Semua kemungkinan Cycle jika K adalah titik awal")
        print("6. Circuit terpendek dan terpanjang dari A ke K")
        print("7. Circuit terpendek dan terpanjang dari G ke J")
        print("8. Circuit terpendek dan terpanjang dari E ke F")
        print("9. Jalankan semua operasi di atas")
        print("0. Keluar dari program")
        
        try:
            choice = int(input("Masukkan pilihan (0-9): "))
            if choice == 0:
                print("Program selesai. Terima kasih!")
                break
            elif 1 <= choice <= 9:
                run_operation(choice, g)
            else:
                print("Pilihan tidak valid. Masukkan angka 0-9.")
        except ValueError:
            print("Input tidak valid. Masukkan angka 0-9.")

main()
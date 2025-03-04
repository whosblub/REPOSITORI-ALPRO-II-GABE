class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_all_paths(self, start, end, path=None):
        if path is None:
            path = []
        
        path = path + [start]
        
        if start == end and len(path) > 1:
            return [path]
        
        paths = []
        for neighbor in self.graph[start]:
            if neighbor not in path or (neighbor == end and len(path) > 1):
                new_paths = self.find_all_paths(neighbor, end, path)
                paths.extend(new_paths)
        
        return paths

    def find_all_cycles(self, start):
        def dfs(current, path, visited, cycles):
            visited.add(current)
            path.append(current)
            
            for neighbor in self.graph[current]:
                if neighbor == start and len(path) >= 3:
                    cycles.append(path.copy() + [start])
                elif neighbor not in visited:
                    dfs(neighbor, path, visited.copy(), cycles)
        
        cycles = []
        dfs(start, [], set(), cycles)
        return cycles

    def find_circuits(self, start, end):
        all_paths = self.find_all_paths(start, end)
        circuits = []
        
        for path in all_paths:
            if path[-1] in self.graph[start]:
                circuit = path + [start]
                circuits.append(circuit)
                
        return circuits


# Contoh penggunaan
g = Graph()
g.add_edge('A', 'B')
g.add_edge('A', 'D')
g.add_edge('B', 'C')
g.add_edge('B', 'E')
g.add_edge('B', 'F')
g.add_edge('C', 'F')
g.add_edge('D', 'E')
g.add_edge('E', 'F')

# Semua jalur dari A ke C
paths_a_to_c = g.find_all_paths('A', 'C')
print("1. Semua kemungkinan Path dari A ke C:")
for i, path in enumerate(paths_a_to_c, 1):
    print(f"   Path {i}: {' -> '.join(path)}")

# Semua siklus jika C sebagai titik awal
cycles_c = g.find_all_cycles('C')
print("\n2. Semua kemungkinan Cycle jika C adalah titik awal:")
for i, cycle in enumerate(cycles_c, 1):
    print(f"   Cycle {i}: {' -> '.join(cycle)}")

# Semua siklus jika B sebagai titik awal
cycles_b = g.find_all_cycles('B')
print("\n3. Semua kemungkinan Cycle jika B adalah titik awal:")
for i, cycle in enumerate(cycles_b, 1):
    print(f"   Cycle {i}: {' -> '.join(cycle)}")

# Circuit terpendek dan terpanjang dari A ke C
circuits = g.find_circuits('A', 'C')
if circuits:
    shortest = min(circuits, key=len)
    longest = max(circuits, key=len)
    
    print("\n4. Circuit terpendek dan terpanjang dari A ke C:")
    print(f"   Circuit terpendek: {' -> '.join(shortest)} (panjang {len(shortest)-1})")
    print(f"   Circuit terpanjang: {' -> '.join(longest)} (panjang {len(longest)-1})")
else:
    print("\n4. Tidak ada circuit dari A ke C")

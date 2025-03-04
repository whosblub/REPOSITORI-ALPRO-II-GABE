class Graph:
    def __init__(self):  # Perbaikan: __init__ harus menggunakan dua underscore
        self.graph = {}
        
    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def find_trail(self, start, end, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []
        
        path.append(start)
        
        if start == end:
            return path
        
        for neighbor in self.graph[start]:
            edge = tuple(sorted([start, neighbor]))
            if edge not in visited:
                visited.add(edge)
                result = self.find_trail(neighbor, end, visited, path.copy())
                if result:
                    return result
        
        return None
    
    def find_all_paths(self, start, end, path=None):
        if path is None:
            path = []
        
        path = path + [start]
        
        if start == end:
            return [path]
        
        paths = []
        for neighbor in self.graph[start]:
            if neighbor not in path:
                new_paths = self.find_all_paths(neighbor, end, path)
                paths.extend(new_paths)
        
        return paths
    
    def find_all_cycles(self, start):
        def dfs(current, path, visited, min_vertex, cycles):
            visited.add(current)
            path.append(current)
            
            for neighbor in self.graph[current]:
                if neighbor == start and len(path) >= 3:
                    cycles.append(path.copy() + [start])
                elif neighbor not in visited:
                    if neighbor >= min_vertex:
                        dfs(neighbor, path, visited.copy(), min_vertex, cycles)
            
            path.pop()
            
        cycles = []
        dfs(start, [], set(), start, cycles)
        return cycles

g = Graph()
g.add_edge('A', 'B')
g.add_edge('A', 'C')
g.add_edge('B', 'C')
g.add_edge('B', 'D')
g.add_edge('C', 'D')

trail = g.find_trail('A', 'D')
print("1. Trail dari A ke D:", " -> ".join(trail) if trail else "Tidak ada trail")

paths = g.find_all_paths('A', 'D')
print("\n2. Semua kemungkinan Path dari A ke D:")
for i, path in enumerate(paths, 1):
    print(f"   Path {i}: {' -> '.join(path)}")

cycles = g.find_all_cycles('A')
print("\n3. Semua kemungkinan Cycle jika A titik awalnya:")
for i, cycle in enumerate(cycles, 1):
    print(f"   Cycle {i}: {' -> '.join(cycle)}")

import os
import ast
from collections import defaultdict

LOG_FILE = "circular.log"

def find_imports(path):
    with open(path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=path)
    imports = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom) and n.module:
            imports.add(n.module.split('.')[0])
    return imports

def build_graph(base_path):
    graph = defaultdict(set)
    py_files = {}
    
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                name = os.path.splitext(file)[0]
                full_path = os.path.join(root, file)
                py_files[name] = full_path
    
    for mod_name, path in py_files.items():
        for imported in find_imports(path):
            if imported in py_files:
                graph[mod_name].add(imported)
    
    return graph

def detect_cycles(graph):
    visited = set()
    path = []
    cycles = []

    def visit(node):
        if node in path:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            visit(neighbor)
        path.pop()

    for node in graph:
        visit(node)
    
    return cycles

def log_cycles(cycles):
    with open(LOG_FILE, "w") as f:
        if not cycles:
            f.write("✅ No circular imports detected.\n")
        else:
            f.write("🚨 Circular imports found:\n")
            for cycle in cycles:
                f.write(" -> ".join(cycle) + "\n")

if __name__ == "__main__":
    graph = build_graph(".")
    cycles = detect_cycles(graph)
    log_cycles(cycles)
    print(f"📄 Done. Results saved in: {os.path.abspath(LOG_FILE)}")

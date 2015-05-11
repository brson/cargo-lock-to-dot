#!/usr/bin/env python

import sys

lockfile = sys.argv[1]

interesting_crates = []
if len(sys.argv) > 2:
    maybe_interesting = sys.argv[2]
    if maybe_interesting and maybe_interesting.startswith("--interesting="):
        interesting_crates = maybe_interesting[14:].split(",")

# Map from crate name to list of crate names
dep_vec = []

current_crate = None
scanning_deps = False
current_deps = []
root = None
scanning_for_root = False


def commit():
    global current_deps, current_crate, scanning_deps, root, scanning_for_root, dep_vec

    # Sanity check: if there are deps then there should be a crate name
    assert len(current_deps) == 0 or current_crate
    if current_crate:
        dep_vec += [(current_crate, current_deps)]
    if scanning_for_root:
        root = current_crate
    current_crate = None
    scanning_deps = False
    current_deps = []
    scanning_for_root = False

with open(lockfile) as f:
    for line in f:
        line = line.strip()
        if line == "[root]":
            commit()
            scanning_for_root = True
        elif line == "[[package]]":
            commit()
        elif line.startswith("name = \""):
            assert line.endswith("\"")
            line = line[8:]
            line = line[:len(line) - 1]
            current_crate = line
        elif line == "dependencies = [":
            scanning_deps = True
        elif line == "]":
            scanning_deps = False
        elif scanning_deps == True:
            assert line.startswith("\"")
            line = line[1:]
            line = line.split(" ")[0]
            current_deps += [line]
    commit()

root = root.replace("-", "_")
print("digraph " + root + " {")

for (crate, deps) in dep_vec:
    if crate == root:
        print("  " + crate + " [root=true]")
        print("  " + crate + " [fillcolor=red]")
        print("  " + crate + " [fontcolor=white]")
        print("  " + crate + " [style=filled]")

    if crate in interesting_crates:
        print("  " + crate + " [fillcolor=blue]")
        print("  " + crate + " [fontcolor=white]")
        print("  " + crate + " [style=filled]")

    for dep in deps:
        crate = crate.replace("-", "_")
        dep = dep.replace("-", "_")
        print("  " + crate + " -> " + dep + ";")

print("}")

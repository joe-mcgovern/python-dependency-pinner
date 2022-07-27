def main():
    print("Analyzing pyproject.toml...")
    with open("pyproject.toml") as f:
        pyproject_content = f.read()

    deps = []
    is_dependency_section = False
    pyproject_lines = pyproject_content.splitlines()
    for line_number, line in enumerate(pyproject_lines):
        if line.startswith("[") and "dependencies" in line:
            is_dependency_section = True
        elif line.startswith("["):
            is_dependency_section = False
        elif is_dependency_section and line.strip() and "*" in line:
            package = line.split("=")[0].strip()
            deps.append(
                {
                    "name": package,
                    "line_number": line_number,
                }
            )

    print("Analyzing poetry.lock...")
    with open("poetry.lock") as f:
        lock = f.read()

    lock_deps = {}
    current_name = None
    for line in lock.splitlines():
        if line.startswith("name"):
            ugly_name = line.split(" = ")[1]
            current_name = ugly_name.strip('"').strip("'")
            lock_deps[current_name] = ""
        elif line.startswith("version"):
            ugly_version = line.split(" = ")[1]
            version = ugly_version.strip('"').strip("'")
            lock_deps[current_name] = version
        elif line == "[[package]]":
            current_name = None

    for dependency in deps:
        if dependency["name"] in lock_deps:
            lock_version = lock_deps[dependency["name"]]
            line = pyproject_lines[dependency["line_number"]]
            new_line = line.replace("*", f"~{lock_version}")
            pyproject_lines[dependency["line_number"]] = new_line
        else:
            print(
                "Could not update:",
                dependency["name"],
                "(it wasn't found in the lock file. This is likely a bug in "
                "the code that analyzes the lock file)",
            )

    print("Writing changes...")
    with open("pyproject.toml", "w") as f:
        f.write("\n".join(pyproject_lines))


if __name__ == "__main__":
    main()

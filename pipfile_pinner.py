import json
import re
from pprint import pprint

with open("Pipfile.lock") as f:
    content = json.loads(f.read())

# A map of package name to their version
all_package_data = {}

for package_name, package_data in content["default"].items():
    all_package_data[package_name] = package_data["version"].lstrip("=")

for package_name, package_data in content["develop"].items():
    all_package_data[package_name] = package_data["version"].lstrip("=")

with open("Pipfile") as f:
    pipfile = f.read()

print("====== Update logs: ======")

dev_section = False
package_section = False
lines = pipfile.splitlines()
for i, line in enumerate(lines):
    if line.strip().startswith("["):
        if line.strip().lstrip("[").rstrip("]") == "packages":
            package_section = True
            dev_section = False
            continue
        elif line.strip().lstrip("[").rstrip("]") == "dev-packages":
            dev_section = True
            package_section = False
            continue
        else:
            dev_section = False
            package_section = False
    if not package_section and not dev_section:
        continue
    pieces = line.split()
    package = pieces[0].lower() if pieces else None
    if not package:
        continue
    possible_lockfile_package_names = [
        package,
        package.replace("_", "-"),
        package.replace("-", "_"),
    ]
    for possible in possible_lockfile_package_names:
        if possible in all_package_data:
            if pieces[0] != possible:
                print(
                    "Updating Pipfile package name to match Pipfile.lock",
                    pieces[0],
                    "->",
                    possible,
                )
                lines[i] = line.replace(pieces[0], possible)
            search = re.search('\s"(.*)"', line)
            matches = search.groups() if search else []
            if matches:
                version = matches[0]
                if version == "*":
                    new_version = all_package_data[possible]
                    new_str = f"~={new_version}"
                    lines[i] = line.replace(version, new_str)
                    print("Updating version", version, "->", new_str)
            break
    else:
        print(f"Could not update package: {package}")

print("")
print("====== Updated Pipfile contents: ========")
print("")
new_content = "\n".join(lines)
print(new_content)

with open("Pipfile", "w") as f:
    f.write(new_content)

print("")
print("==== Updated pipfile ====")

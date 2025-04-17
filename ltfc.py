import json
import os
import shutil

def sort_modlist():
    with open(".workspace/modlist.html", "r") as f:
        mods = f.readlines()[1:-1]
        mods.sort()
        with open(".workspace/modlist.html", "w") as f:
            f.write("<ul>\n")
            for mod in mods:
                f.write(mod)
            f.write("</ul>")

def sort_manifest():
    with open(".workspace/manifest.json", "r") as f:
        manifest = json.load(f)
        manifest["files"].sort(key=lambda x: x["projectID"])
        with open(".workspace/manifest.json", "w") as f:
            for file in manifest["files"]:
                if "__comment" in file:
                    del file["__comment"]
            json.dump(manifest, f, indent=4)

def compile():
    print("Seting up workspace...")
    if os.path.exists(".workspace"):
        shutil.rmtree(".workspace")
    os.mkdir(".workspace")
    shutil.copytree("modpack", ".workspace", dirs_exist_ok=True)
    print("Sorting modlist...")
    sort_modlist()
    print("Sorting manifest...")
    sort_manifest()
    print("Zipping modpack...")
    shutil.make_archive("modpack", "zip", "modpack")

    print("Done!")


def main():
    compile()

if __name__ == '__main__':
    main()
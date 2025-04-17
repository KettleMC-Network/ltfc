import json
import os
import shutil

BUILD_DIR = ".build"
MODPACK_DIR = "modpack"

def sort_modlist(directory: str):
    with open(f"{directory}/modlist.html", "r") as f:
        mods = f.readlines()[1:-1]
        mods.sort()
        with open(f"{directory}/modlist.html", "w") as f:
            f.write("<ul>\n")
            for mod in mods:
                f.write(mod)
            f.write("</ul>")

def sort_manifest(directory: str, keep_comments: bool = True):
    with open(f"{directory}/manifest.json", "r") as f:
        manifest = json.load(f)
        manifest["files"].sort(key=lambda x: x["projectID"])
        with open(f"{directory}/manifest.json", "w") as f:
            if not keep_comments:
                for file in manifest["files"]:
                    if "__comment" in file:
                        del file["__comment"]
            json.dump(manifest, f, indent=4)

def setup_workspace():
    if os.path.exists(".build"):
        shutil.rmtree(".build")
    os.mkdir(".build")
    shutil.copytree("modpack", ".build", dirs_exist_ok=True)

def compile():
    print("Seting up workspace...")
    setup_workspace()
    print("Sorting modlist...")
    sort_modlist(BUILD_DIR)
    print("Sorting manifest...")
    sort_manifest(BUILD_DIR, keep_comments=False)
    print("Zipping modpack...")
    shutil.make_archive("modpack", "zip", "modpack")
    print("Done!")

def clean():
    print("Cleaning up...")
    sort_modlist(MODPACK_DIR)
    sort_manifest(MODPACK_DIR, keep_comments=True)
    print("Modpack cleaned up!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LTFC Modpack Builder")
    parser.add_argument(
        "action",
        choices=["compile", "clean"],
        help="Action to perform: compile or clean",
    )
    args = parser.parse_args()

    if args.action == "compile":
        compile()
    elif args.action == "clean":
        clean()
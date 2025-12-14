import json
import os
import re
import shutil
from typing import Any

# If this changes, the .gitignore file must be updated accordingly
BUILD_DIR = ".build"
OUTPUT_DIR = ".out"
MODPACK_DIR = "modpack"
LINK_FILE = "links.json"
LINK_FIELD = "__link"
NAME_FIELD = "__name"
AUTHOR_FIELD = "__author"

MODPACK_NAME = "ltfc"

SORT_MANIFEST_AFTER = NAME_FIELD

MODLIST_ENTRY_REGEX = r'<li><a href="(?P<link>[^"]+)">(?P<mod>.+?)(?: \(by (?P<author>[^)]+)\))?</a></li>'


def sort_modlist(directory: str):
    with open(f"{directory}/modlist.html", "r") as f:
        mods = f.readlines()[1:-1]
        mods.sort()
        with open(f"{directory}/modlist.html", "w") as f:
            f.write("<ul>\n")
            for mod in mods:
                f.write(f"    {mod.strip()}\n")
            f.write("</ul>")


def sort_manifest(directory: str, keep_comments: bool = True):
    with open(f"{directory}/manifest.json", "r") as input_file:
        manifest = json.load(input_file)
        manifest["files"].sort(key=lambda x: x[SORT_MANIFEST_AFTER])
        with open(f"{directory}/manifest.json", "w") as output_file:
            if not keep_comments:
                for mod_entry in manifest["files"]:
                    clean_comments(mod_entry)
            json.dump(manifest, output_file, indent=2)


def add_info_to_manifest(directory: str, ids_to_links: dict, links_to_names: dict):
    """
    Adds links to the manifest file in the specified directory.
    :param directory: The directory containing the manifest file.
    :param ids_to_links: A dictionary mapping project IDs to links.
    :param links_to_names: A dictionary mapping links to names and authors.
    :return: None
    """
    with open(f"{directory}/manifest.json", "r") as input_file:
        manifest = json.load(input_file)
        for mod_entry in manifest["files"]:
            clean_comments(mod_entry)
            if mod_entry["projectID"] in ids_to_links:
                mod_entry[LINK_FIELD] = ids_to_links[mod_entry["projectID"]]
            else:
                print("Warning: No link found for project ID", mod_entry["projectID"])
            if LINK_FIELD in mod_entry:
                if mod_entry[LINK_FIELD] in links_to_names:
                    name = links_to_names[mod_entry[LINK_FIELD]][0]
                    author = links_to_names[mod_entry[LINK_FIELD]][1]
                    if name:
                        mod_entry[NAME_FIELD] = name
                    else:
                        print("Warning: No name found for link", mod_entry[LINK_FIELD])
                    if author:
                        mod_entry[AUTHOR_FIELD] = author
                else:
                    print("Warning: No name found for link", mod_entry[LINK_FIELD])
        with open(f"{directory}/manifest.json", "w") as output_file:
            json.dump(manifest, output_file, indent=2)

def clean_comments(dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    Cleans comments from a dictionary by removing keys that start with '__'.
    :param dictionary: The dictionary to clean.
    :return: The cleaned dictionary.
    """
    for key in list(dictionary.keys()):
        if key.startswith("__"):
            del dictionary[key]
    return dictionary

def load_links_from_file(file_path: str) -> dict:
    """
    Loads links from a JSON file and returns them as a dictionary.
    :param file_path:  The path to the JSON file containing links.
    :return: Dictionary mapping project IDs (ints) to links (str).
    """
    return {
        int(project_id): link[:-1] if link.endswith("/") else link for project_id, link in json.load(open(file_path, "r")).items()
    } if os.path.exists(file_path) else {}


def load_names_from_file(file_path: str) -> dict[str, tuple[str, str]]:
    """
    Loads the modlist and maps links to names and authors.
    :param file_path: The path to the modlist html file.
    :return: Dictionary mapping links (str) to names (str) and authors (str).
    """
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        lines = f.readlines()
        links = {}
        for line in lines:
            line = line.strip()
            if line in ("<ul>", "</ul>"):
                continue
            match = re.search(MODLIST_ENTRY_REGEX, line)
            if match:
                link = match.group("link")
                mod = match.group("mod")
                author = match.group("author") if match.group("author") else None
                links[link] = (mod, author)

    return links


def setup_workspace():
    """
    Clears the .build directory and copies the contents of the modpack directory into it.
    :return: None
    """
    if os.path.exists(".build"):
        shutil.rmtree(".build")
    os.mkdir(".build")
    shutil.copytree("modpack", ".build", dirs_exist_ok=True)


def compile():
    """
    Compiles the modpack by setting up the workspace, sorting the modlist and manifest files, and zipping the modpack.
    :return:
    """
    print("Seting up workspace...")
    setup_workspace()
    print("Sorting modlist...")
    sort_modlist(BUILD_DIR)
    print("Sorting manifest...")
    sort_manifest(BUILD_DIR, keep_comments=False)
    print("Zipping modpack into output directory...")
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    shutil.make_archive(f"{OUTPUT_DIR}/{MODPACK_NAME}-{get_version_from_manifest(MODPACK_DIR)}", "zip", BUILD_DIR)
    print("Done!")


def get_version_from_manifest(directory: str) -> str:
    """
    Retrieves the version from the manifest file in the specified directory.
    :param directory: The directory containing the manifest file.
    :return: The version string from the manifest.
    """
    if not os.path.exists(f"{directory}/manifest.json"):
        return "unknown"

    with open(f"{directory}/manifest.json", "r") as input_file:
        manifest = json.load(input_file)
        return manifest.get("version", "unknown")

def clean():
    """
    Cleans up the modpack by sorting the modlist and manifest files in the modpack directory.
    :return:
    """
    print("Sorting modlist...")
    sort_modlist(MODPACK_DIR)
    print("Adding links to manifest...")
    links = load_links_from_file(LINK_FILE)
    names = load_names_from_file(f"{MODPACK_DIR}/modlist.html")
    if links:
        add_info_to_manifest(MODPACK_DIR, links, names)
    else:
        print(f"No links found in {LINK_FILE}. Skipping link addition.")
    print("Sorting manifest...")
    sort_manifest(MODPACK_DIR, keep_comments=True)
    print("Modpack cleaned up!")


if __name__ == "__main__":
    import argparse

    actions = {
        "compile": compile,
        "clean": clean,
        "sort_modlist": lambda: sort_modlist(MODPACK_DIR),
        "sort_manifest": lambda: sort_manifest(MODPACK_DIR, keep_comments=True),
        "add_links": lambda: add_info_to_manifest(MODPACK_DIR, load_links_from_file(LINK_FILE), load_names_from_file(f"{MODPACK_DIR}/modlist.html")),
    }

    parser = argparse.ArgumentParser(description="Modpack Builder")
    parser.add_argument(
        "action",
        choices=list(actions.keys()),
        help="Action to perform: compile or clean",
    )
    args = parser.parse_args()

    if args.action in actions:
        actions[args.action]()
    else:
        print(f"Unknown action: {args.action}")
        parser.print_help()
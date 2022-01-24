from importlib import resources

VERSION = resources.read_text("alco_map", "version.txt").strip()

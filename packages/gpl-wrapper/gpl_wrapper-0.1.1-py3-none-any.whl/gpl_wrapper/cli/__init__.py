from pathlib import Path

from snk.cli import CLI

gpl_wrapper = CLI(pipeline_dir_path = Path(__file__).parent.parent)

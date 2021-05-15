"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import shutil
import pprint

from invoke import task
import webbrowser
from pathlib import Path

Path().expanduser()

ROOT_DIR = Path(__file__).parent
HELM_CHART_DIR = ROOT_DIR / "helm" / "url-shortener"

@task(help={})
def template(c, release="url-shortener"):
    """Template the helm chart
    """
    c.run(f"helm template {release} {HELM_CHART_DIR} > ./generated-deployment.yml")

import subprocess
import re
from typing import Tuple


def get_current_branch_name_and_detached_head_status() -> Tuple[str, bool]:
    current_branch = subprocess.getoutput("git rev-parse --symbolic-full-name HEAD")
    if current_branch == "HEAD":
        detached_head_state = True
        current_branch = ""
    elif current_branch.startswith("refs/heads/"):
        detached_head_state = False
        current_branch = current_branch.replace("refs/heads/", "")
    return current_branch, detached_head_state


def retrieve_and_parse_git_describe_long_text():
    describe_result = subprocess.getoutput("git describe --long")
    tag_stuff_pattern = re.compile("^(?P<tag_name>.+)[-](?P<commit_count>[0-9]+)[-](?P<short_hash>[0-9a-z]+)$")
    describe_match = tag_stuff_pattern.match(describe_result)
    if not describe_match:
        raise RuntimeError(
            f"Could not determine the version tag from VCS; `git describe --long` replied with: {describe_result}")
    tag_captures = describe_match.groupdict()
    return tag_captures["tag_name"], tag_captures["commit_count"]


def transform_describe_result_to_version_string(tag_name, commit_count, branch_name, detached_head_state) -> str:
    if detached_head_state or branch_name in {"main", "refs/heads/main"}:
        if commit_count == '0':
            extra_version_text = ""
        else:
            extra_version_text = f".post{commit_count}"
    else:
        cleaned_branch_name = re.sub("[^0-9a-zA-Z.-]", "", branch_name).replace('-', '.').strip(".")
        extra_version_text = f".dev{commit_count}+branch.{cleaned_branch_name}"
    return f"{tag_name}{extra_version_text}"


def get_version_for_pyproject_toml():
    current_branch, detached_head_state = get_current_branch_name_and_detached_head_status()
    tag_name, commit_count = retrieve_and_parse_git_describe_long_text()
    return transform_describe_result_to_version_string(
        tag_name=tag_name,
        commit_count=commit_count,
        branch_name=current_branch,
        detached_head_state=detached_head_state
    )


if __name__ == "__main__":
    print(get_version_for_pyproject_toml())

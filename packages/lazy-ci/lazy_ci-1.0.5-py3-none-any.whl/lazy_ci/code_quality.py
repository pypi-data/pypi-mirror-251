"""Code quality checks for lazy-ci."""
import subprocess

from loguru import logger


def run_code_quality():
    """Run code quality checks"""
    commands = [
        ["pytest", "-v"],
        ["black", "--check", "."],
        ["pylint", "--ignore-paths", ".*test.*", "--recursive", "y", "."],
        ["lizard", "."],
    ]

    # Run commands in parallel
    issues_found = False
    issues_found_with = []
    processes = []
    for command in commands:
        process = subprocess.Popen(  # pylint: disable=consider-using-with
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        processes.append(process)
    for process in processes:
        stdout, stderr = process.communicate()
        return_code = process.wait()
        if return_code != 0:
            issues_found_with.append(
                f"Issue found with command: {' '.join(process.args)}"
            )
            issues_found = True
        if stderr:
            logger.error(stderr.decode("utf-8"))
        if stdout:
            logger.info(stdout.decode("utf-8"))
    if issues_found:
        logger.error("Issues found with the following commands:")
        for issue_found_with in issues_found_with:
            logger.error(issue_found_with)

    return not issues_found

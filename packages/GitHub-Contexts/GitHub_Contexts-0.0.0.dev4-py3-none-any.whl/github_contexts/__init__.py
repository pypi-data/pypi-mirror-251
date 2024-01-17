from github_contexts.github.context import GitHubContext


def context_github(context: dict):
    return GitHubContext(context=context)

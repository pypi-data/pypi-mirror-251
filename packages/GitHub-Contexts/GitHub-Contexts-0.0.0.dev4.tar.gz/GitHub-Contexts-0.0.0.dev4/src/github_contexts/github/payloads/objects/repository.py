from github_contexts.github.payloads.objects.license import LicenseObject
from github_contexts.github.payloads.objects.user import UserObject
from github_contexts.github.payloads.objects.permissions import PermissionsObject
from github_contexts.github.enums import (
    RepositoryVisibility,
    MergeCommitTitle,
    MergeCommitMessage,
    SquashMergeCommitMessage,
    SquashMergeCommitTitle
)


class RepositoryObject:

    def __init__(self, repository: dict):
        self._repository = repository
        return

    @property
    def allow_auto_merge(self) -> bool | None:
        return self._repository.get("allow_auto_merge")

    @property
    def allow_forking(self) -> bool | None:
        return self._repository.get("allow_forking")

    @property
    def allow_merge_commit(self) -> bool | None:
        return self._repository.get("allow_merge_commit")

    @property
    def allow_rebase_merge(self) -> bool | None:
        return self._repository.get("allow_rebase_merge")

    @property
    def allow_squash_merge(self) -> bool | None:
        return self._repository.get("allow_squash_merge")

    @property
    def allow_update_branch(self) -> bool | None:
        return self._repository.get("allow_update_branch")

    @property
    def archive_url(self) -> str:
        return self._repository["archive_url"]

    @property
    def archived(self) -> bool:
        return self._repository["archived"]

    @property
    def assignees_url(self) -> str:
        return self._repository["assignees_url"]

    @property
    def blobs_url(self) -> str:
        return self._repository["blobs_url"]

    @property
    def branches_url(self) -> str:
        return self._repository["branches_url"]

    @property
    def clone_url(self) -> str:
        return self._repository["clone_url"]

    @property
    def collaborators_url(self) -> str:
        return self._repository["collaborators_url"]

    @property
    def comments_url(self) -> str:
        return self._repository["comments_url"]

    @property
    def commits_url(self) -> str:
        return self._repository["commits_url"]

    @property
    def compare_url(self) -> str:
        return self._repository["compare_url"]

    @property
    def contents_url(self) -> str:
        return self._repository["contents_url"]

    @property
    def contributors_url(self) -> str:
        return self._repository["contributors_url"]

    @property
    def created_at(self) -> str:
        return self._repository["created_at"]

    @property
    def custom_properties(self) -> dict | None:
        return self._repository.get("custom_properties")

    @property
    def default_branch(self) -> str:
        return self._repository["default_branch"]

    @property
    def delete_branch_on_merge(self) -> bool | None:
        return self._repository.get("delete_branch_on_merge")

    @property
    def deployments_url(self) -> str:
        return self._repository["deployments_url"]

    @property
    def description(self) -> str | None:
        return self._repository["description"]

    @property
    def disabled(self) -> bool | None:
        return self._repository.get("disabled")

    @property
    def downloads_url(self) -> str:
        return self._repository["downloads_url"]

    @property
    def events_url(self) -> str:
        return self._repository["events_url"]

    @property
    def fork(self) -> bool:
        return self._repository["fork"]

    @property
    def forks(self) -> int:
        return self._repository["forks"]

    @property
    def forks_count(self) -> int:
        return self._repository["forks_count"]

    @property
    def forks_url(self) -> str:
        return self._repository["forks_url"]

    @property
    def full_name(self) -> str:
        return self._repository["full_name"]

    @property
    def git_commits_url(self) -> str:
        return self._repository["git_commits_url"]

    @property
    def git_refs_url(self) -> str:
        return self._repository["git_refs_url"]

    @property
    def git_tags_url(self) -> str:
        return self._repository["git_tags_url"]

    @property
    def git_url(self) -> str:
        return self._repository["git_url"]

    @property
    def has_discussions(self) -> bool | None:
        return self._repository.get("has_discussions")

    @property
    def has_downloads(self) -> bool:
        return self._repository["has_downloads"]

    @property
    def has_issues(self) -> bool:
        return self._repository["has_issues"]

    @property
    def has_pages(self) -> bool:
        return self._repository["has_pages"]

    @property
    def has_projects(self) -> bool:
        return self._repository["has_projects"]

    @property
    def has_wiki(self) -> bool:
        return self._repository["has_wiki"]

    @property
    def homepage(self) -> str | None:
        return self._repository["homepage"]

    @property
    def hooks_url(self) -> str:
        return self._repository["hooks_url"]

    @property
    def html_url(self) -> str:
        return self._repository["html_url"]

    @property
    def id(self) -> int:
        "Unique identifier of the repository."
        return self._repository["id"]

    @property
    def is_template(self) -> bool | None:
        return self._repository.get("is_template")

    @property
    def issue_comment_url(self) -> str:
        return self._repository["issue_comment_url"]

    @property
    def issue_events_url(self) -> str:
        return self._repository["issue_events_url"]

    @property
    def issues_url(self) -> str:
        return self._repository["issues_url"]

    @property
    def keys_url(self) -> str:
        return self._repository["keys_url"]

    @property
    def labels_url(self) -> str:
        return self._repository["labels_url"]

    @property
    def language(self) -> str | None:
        return self._repository["language"]

    @property
    def languages_url(self) -> str:
        return self._repository["languages_url"]

    @property
    def license(self) -> LicenseObject | None:
        return LicenseObject(self._repository["license"]) if self._repository.get("license") else None

    @property
    def master_branch(self) -> str | None:
        return self._repository.get("master_branch") or self.default_branch

    @property
    def merge_commit_message(self) -> MergeCommitMessage | None:
        return MergeCommitMessage(self._repository["merge_commit_message"]) if self._repository.get("merge_commit_message") else None

    @property
    def merge_commit_title(self) -> MergeCommitTitle | None:
        return MergeCommitTitle(self._repository["merge_commit_title"]) if self._repository.get("merge_commit_title") else None

    @property
    def merges_url(self) -> str:
        return self._repository["merges_url"]

    @property
    def milestones_url(self) -> str:
        return self._repository["milestones_url"]

    @property
    def mirror_url(self) -> str | None:
        return self._repository.get("mirror_url")

    @property
    def name(self) -> str:
        return self._repository["name"]

    @property
    def node_id(self) -> str:
        return self._repository["node_id"]

    @property
    def notifications_url(self) -> str:
        return self._repository["notifications_url"]

    @property
    def open_issues(self) -> int:
        return self._repository["open_issues"]

    @property
    def open_issues_count(self) -> int:
        return self._repository["open_issues_count"]

    @property
    def organization(self) -> str | None:
        return self._repository.get("organization")

    @property
    def owner(self) -> UserObject | None:
        return UserObject(self._repository["owner"]) if self._repository.get("owner") else None

    @property
    def permissions(self) -> PermissionsObject | None:
        return PermissionsObject(self._repository["permissions"]) if self._repository.get("permissions") else None

    @property
    def private(self) -> bool:
        """Whether the repository is private (True) or public (False)."""
        return self._repository["private"]

    @property
    def public(self) -> bool:
        """Whether the repository is public (True) or private (False)."""
        return self._repository.get("public", not self.private)

    @property
    def pulls_url(self) -> str:
        return self._repository["pulls_url"]

    @property
    def pushed_at(self) -> str | int | None:
        return self._repository["pushed_at"]

    @property
    def releases_url(self) -> str:
        return self._repository["releases_url"]

    @property
    def role_name(self) -> str | None:
        return self._repository.get("role_name")

    @property
    def size(self) -> int:
        return self._repository["size"]

    @property
    def squash_merge_commit_message(self) -> SquashMergeCommitMessage | None:
        return (
            SquashMergeCommitMessage(self._repository["squash_merge_commit_message"])
            if self._repository.get("squash_merge_commit_message") else None
        )

    @property
    def squash_merge_commit_title(self) -> SquashMergeCommitTitle | None:
        return (
            SquashMergeCommitTitle(self._repository["squash_merge_commit_title"])
            if self._repository.get("squash_merge_commit_title") else None
        )

    @property
    def ssh_url(self) -> str:
        return self._repository["ssh_url"]

    @property
    def stargazers(self) -> int | None:
        return self._repository.get("stargazers")

    @property
    def stargazers_count(self) -> int:
        return self._repository["stargazers_count"]

    @property
    def stargazers_url(self) -> str:
        return self._repository["stargazers_url"]

    @property
    def statuses_url(self) -> str:
        return self._repository["statuses_url"]

    @property
    def subscribers_url(self) -> str:
        return self._repository["subscribers_url"]

    @property
    def subscription_url(self) -> str:
        return self._repository["subscription_url"]

    @property
    def svn_url(self) -> str:
        return self._repository["svn_url"]

    @property
    def tags_url(self) -> str:
        return self._repository["tags_url"]

    @property
    def teams_url(self) -> str:
        return self._repository["teams_url"]

    @property
    def topics(self) -> list[str]:
        return self._repository.get("topics", [])

    @property
    def trees_url(self) -> str:
        return self._repository["trees_url"]

    @property
    def updated_at(self) -> str:
        return self._repository["updated_at"]

    @property
    def url(self) -> str:
        return self._repository["url"]

    @property
    def visibility(self) -> RepositoryVisibility:
        return RepositoryVisibility(self._repository["visibility"])

    @property
    def watchers(self) -> int:
        return self._repository["watchers"]

    @property
    def watchers_count(self) -> int:
        return self._repository["watchers_count"]

    @property
    def web_commit_signoff_required(self) -> bool | None:
        return self._repository.get("web_commit_signoff_required")

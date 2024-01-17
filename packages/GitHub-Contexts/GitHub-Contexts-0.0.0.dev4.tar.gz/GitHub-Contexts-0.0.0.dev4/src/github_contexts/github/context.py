from ruamel.yaml import YAML

from github_contexts.github.enums import RefType, SecretSource

from github_contexts.github.payloads.base import Payload
from github_contexts.github.payloads.issue_comment import IssueCommentPayload
from github_contexts.github.payloads.issues import IssuesPayload
from github_contexts.github.payloads.pull_request import PullRequestPayload
from github_contexts.github.payloads.push import PushPayload
from github_contexts.github.payloads.schedule import SchedulePayload
from github_contexts.github.payloads.workflow_dispatch import WorkflowDispatchPayload
from github_contexts.github.enums import EventType, ActionType


class GitHubContext:
    """
    The 'github' context of the workflow run.

    It contains information about the workflow run and the event that triggered the run.

    References
    ----------
    - [GitHub Docs](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context)
    """

    def __init__(self, context: dict):
        payload_manager = {
            EventType.ISSUES: IssuesPayload,
            EventType.PUSH: PushPayload,
            EventType.ISSUE_COMMENT: IssueCommentPayload,
            EventType.PULL_REQUEST: PullRequestPayload,
            EventType.PULL_REQUEST_TARGET: PullRequestPayload,
            EventType.SCHEDULE: SchedulePayload,
            EventType.WORKFLOW_DISPATCH: WorkflowDispatchPayload,
        }
        payload = context.pop("event")
        self._token = context.pop("token")
        self._context = dict(sorted(context.items()))
        self._payload = (
            payload_manager[self.event_name](payload=payload) if self.event_name in payload_manager
            else Payload(payload=payload)
        )
        return

    def __str__(self):
        return YAML(typ=["rt", "string"]).dumps(self._context, add_final_eol=True)

    def __getitem__(self, item):
        return self._context[item]

    @property
    def action(self) -> str | None:
        """The name of the action currently running, or the id of a step.

        GitHub removes special characters, and uses the name `__run` when the current step
        runs a script without an id.
        If you use the same action more than once in the same job,
        the name will include a suffix with the sequence number with underscore before it.

        For example, the first script you run will have the name` __run`,
        and the second script will be named `__run_2`.
        Similarly, the second invocation of `actions/checkout` will be `actionscheckout2`.
        """
        return self._context.get("action")

    @property
    def action_path(self) -> str | None:
        """The path where an action is located. This property is only supported in composite actions.

        You can use this path to access files located in the same repository as the action,
        for example by changing directories to the path.
        """
        return self._context.get("action_path")

    @property
    def action_ref(self) -> str | None:
        """For a step executing an action, this is the ref of the action being executed. For example, `v2`."""
        return self._context.get("action_ref")

    @property
    def action_repository(self) -> str | None:
        """For a step executing an action, this is the owner and repository name of the action being executed.
        For example, `actions/checkout`.
        """
        return self._context.get("action_repository")

    @property
    def action_status(self) -> str | None:
        """For a composite action, the current result of the composite action."""
        return self._context.get("action_status")

    @property
    def actor(self) -> str:
        """The username of the user that triggered the initial workflow run.

        If the workflow run is a re-run, this value may differ from `triggering_actor`.
        Any workflow re-runs will use the privileges of `actor`,
        even if the actor initiating the re-run (`triggering_actor`) has different privileges.
        """
        return self._context["actor"]

    @property
    def actor_id(self) -> str:
        """The account ID of the person or app that triggered the initial workflow run, e.g., 1234567."""
        return self._context["actor_id"]

    @property
    def api_url(self) -> str:
        """The URL of the GitHub REST API."""
        return self._context["api_url"]

    @property
    def base_ref(self):
        """The base reference (i.e., target branch) of the pull request in a workflow run.

        This property is only available when the event that triggers a workflow run
        is either pull_request or pull_request_target.
        """
        return self._context["base_ref"]

    @property
    def env(self) -> str:
        """Path on the runner to the file that sets environment variables from workflow commands.

        This file is unique to the current step and is a different file for each step in a job.
        """
        return self._context["env"]

    @property
    def event(self) -> IssueCommentPayload | IssuesPayload | PullRequestPayload | PushPayload | SchedulePayload | Payload:
        """The full event webhook payload.

        This is identical to the webhook payload of the event that triggered the workflow run,
        and is different for each event.
        The webhooks for each GitHub Actions event is linked in
        [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).
        For example, for a workflow run triggered by the [push event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#push),
        this object contains the contents of the [push webhook payload](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#push).
        """
        return self._payload

    @property
    def event_name(self) -> EventType:
        """The event type that triggered the workflow."""
        return EventType(self._context["event_name"])

    @property
    def event_path(self) -> str:
        """The path to the file on the runner that contains the full event webhook payload."""
        return self._context["event_path"]

    @property
    def graphql_url(self) -> str:
        """The URL of the GitHub GraphQL API."""
        return self._context["graphql_url"]

    @property
    def head_ref(self) -> str | None:
        """The head reference (i.e., source branch) of the pull request in a workflow run.

        This is only available when the event that triggers a workflow run is
        either 'pull_request' or 'pull_request_target'.
        """
        return self._context.get("head_ref")

    @property
    def job(self) -> str | None:
        """The [`job_id`](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_id)
        of the current job.

        This is set by the Actions runner, and is only available within the execution steps of a job.
        """
        return self._context.get("job")

    @property
    def path(self) -> str:
        """Path on the runner to the file that sets system PATH variables from workflow commands.

        This file is unique to the current step and is a different file for each step in a job.
        """
        return self._context["path"]

    @property
    def ref(self) -> str:
        """
        The fully formed reference of the branch or tag that triggered the workflow run,
        e.g. 'refs/heads/main', 'refs/tags/v1.0' etc.

        Notes
        -----
        - For workflows triggered by push, this is the branch or tag ref that was pushed.
        - For workflows triggered by pull_request, this is the pull request merge branch.
        - For workflows triggered by release, this is the release tag created.
        - For other triggers, this is the branch or tag ref that triggered the workflow run.
        - This is only set if a branch or tag is available for the event type.
        - The ref given is fully-formed, meaning that for branches the format is `refs/heads/<branch_name>`,
          for pull requests it is `refs/pull/<pr_number>/merge`,
          and for tags it is `refs/tags/<tag_name>`.
        """
        return self._context["ref"]

    @property
    def ref_name(self) -> str:
        """The short reference name of the branch or tag that triggered the event.

         Notes
         -----
         - This value matches the branch or tag name shown on GitHub, e.g., `main`, `dev/1`.
         - For pull requests, the format is `refs/pull/<pr_number>/merge`.
         """
        return self._context["ref_name"]

    @property
    def ref_protected(self) -> bool:
        """Whether the branch or tag that triggered the workflow run is protected."""
        return self._context["ref_protected"]

    @property
    def ref_type(self) -> RefType:
        """The type of the ref that triggered the event, either 'branch' or 'tag'."""
        return RefType(self._context["ref_type"])

    @property
    def repository(self) -> str:
        """Full name of the repository, i.e. `<owner_username>/<repo_name>`,
        e.g., 'RepoDynamics/RepoDynamics'.
        """
        return self._context["repository"]

    @property
    def repository_id(self) -> str:
        """The ID of the repository, e.g., `123456789`."""
        return self._context["repository_id"]

    @property
    def repository_owner(self) -> str:
        """GitHub username of the repository owner."""
        return self._context["repository_owner"]

    @property
    def repository_owner_id(self) -> str:
        """The account ID of the repository owner, e.g., `1234567`."""
        return self._context["repository_owner_id"]

    @property
    def repository_url(self) -> str:
        """The Git URL of the repository, e.g., `git://github.com/RepoDynamics/GitHub-Contexts.git`."""
        return self._context["repositoryUrl"]

    @property
    def retention_days(self) -> str:
        """The number of days that workflow run logs and artifacts are kept."""
        return self._context["retention_days"]

    @property
    def run_id(self) -> str:
        """A unique number for each workflow run within a repository.

        This number does not change when the workflow is re-run.
        """
        return self._context["run_id"]

    @property
    def run_number(self) -> str:
        """A unique number for each run of a particular workflow in a repository.

        This number begins at 1 for the workflow's first run,
        and increments with each new run.
        This number does not change when the workflow is re-run.
        """
        return self._context["run_number"]

    @property
    def run_attempt(self) -> str:
        """A unique number for each attempt of a particular workflow run in a repository.

        This number begins at 1 for the workflow run's first attempt, and increments with each re-run.
        """
        return self._context["run_attempt"]

    @property
    def secret_source(self) -> SecretSource:
        """The source of a secret used in a workflow."""
        return SecretSource(self._context["secret_source"])

    @property
    def server_url(self) -> str:
        """The URL of the GitHub server, e.g., `https://github.com`."""
        return self._context["server_url"]

    @property
    def sha(self) -> str:
        """The SHA hash of the most recent commit on the branch that triggered the workflow.

        The value of this commit SHA depends on the event that triggered the workflow.
        For more information, see References.

        References
        ----------
        - [GitHub Docs: Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
        """
        return self._context["sha"]

    @property
    def token(self) -> str:
        """
        A token to authenticate on behalf of the GitHub App installed on your repository.

        This is functionally equivalent to the `GITHUB_TOKEN` secret.
        """
        return self._token

    @property
    def triggering_actor(self) -> str:
        """The username of the user that initiated the workflow run.

        If the workflow run is a re-run, this value may differ from `actor`.
        Any workflow re-runs will use the privileges of `actor`,
        even if the actor initiating the re-run (`triggering_actor`) has different privileges.
        """
        return self._context["triggering_actor"]

    @property
    def workflow(self) -> str:
        """The name of the workflow.

        If the workflow file doesn't specify a name,
        the value of this property is the full path of the workflow file in the repository.
        """
        return self._context["workflow"]

    @property
    def workflow_ref(self) -> str:
        """The ref path to the workflow,
        e.g., `octocat/hello-world/.github/workflows/my-workflow.yml@refs/heads/my_branch`.
        """
        return self._context["workflow_ref"]

    @property
    def workflow_sha(self) -> str:
        """The commit SHA hash of the workflow file."""
        return self._context["workflow_sha"]

    @property
    def workspace(self) -> str:
        """The default working directory on the runner for steps,
        and the default location of your repository when using the
        [checkout action](https://github.com/actions/checkout).
        """
        return self._context["workspace"]

    @property
    def repository_name(self) -> str:
        """Name of the repository, e.g., `GitHub-Contexts`."""
        return self.repository.removeprefix(f"{self.repository_owner}/")

    @property
    def target_repo_fullname(self) -> str:
        return (
            self.event.pull_request.head.repo.full_name
            if self.event_name == "pull_request"
            else self.repository
        )

    @property
    def target_branch_name(self) -> str:
        return self.base_ref if self.event_name is EventType.PULL_REQUEST else self.ref_name

    @property
    def ref_is_main(self) -> bool:
        return self.ref == f"refs/heads/{self.event.repository.default_branch}"

    @property
    def hash_before(self) -> str:
        """The SHA hash of the most recent commit on the branch before the event."""
        if self.event_name is EventType.PUSH:
            return self.event.before
        if self.event_name is EventType.PULL_REQUEST:
            if self.event.action is ActionType.SYNCHRONIZE:
                return self.event.before
            return self.event.pull_request.base.sha
        return self.sha

    @property
    def hash_after(self) -> str:
        """The SHA hash of the most recent commit on the branch after the event."""
        if self.event_name is EventType.PUSH:
            return self.event.after
        if self.event_name is EventType.PULL_REQUEST:
            if self.event.action is ActionType.SYNCHRONIZE:
                return self.event.after
            return self.event.pull_request.head.sha
        return self.sha

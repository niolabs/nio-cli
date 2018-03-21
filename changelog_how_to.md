# Auto-generate the CHANGELOG.md

The changelog is visible at docs.n.io/cli/changelog.html. Update the changelog after each release.
To generate the changelog from the PR history, use the command-line tool github-changelog-generator.

1. To install the github-changelog-generator, follow the directions here: [https://github.com/skywinder/github-changelog-generator](https://github.com/skywinder/github-changelog-generator)

2. Label any relevant PRs on GitHub with one or more of the following labels: bug, enhancement, deprecated, removed, security

3. Generate the CHANGELOG.md with the command:

  ```bash
  github_changelog_generator niolabs/nio-cli
  ```

  If you get an API rate-limit error, you need to get a token to make authenticated requests to the GitHub API.

  Simply [generate a token here](https://github.com/settings/tokens/new?description=GitHub%20Changelog%20Generator%20token) with only "repo" scope permissions selected.

  Copy your token and type
  ```bash
  export CHANGELOG_GITHUB_TOKEN="«your-40-digit-github-token»"
  ```
  and then repeat the command in step 3 above to generate your CHANGELOG.md.

4. You can then copy and paste the most recent changes into the release notes.

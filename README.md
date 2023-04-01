<!-- markdownlint-disable MD022 -->
# Semgrep Pre-commit Hook with diff awareness 😉

This is a pre-commit hook for [Semgrep](https://semgrep.dev) with diff-awareness. It will only run the changes made to the staged files. Yes, that's it.

## Why I wrote this?

Pre-commit hooks generally chain the names of the staged files as arguments and pass them to the pre-commit entrypoint. By doing this, our hook will run on the entire staged files. This behavior is good for things like linter or test runners. The staged files may have just specific portions of the code that are modified. I wanted Semgrep to scan that diff alone. After learning about how pre-commit works and Semgrep runs in pre-commit, I understood there's no way to do this. So, I wrote this hook.

## How does it work?

What I have done is a hack. We first make a dummy commit with the staged files. Then, we run Semgrep on the diff between the dummy commit (with a `--no-verify` flag) and the previous commit. After that, we perform a `git reset --soft <previous commit>`. Now the repo returns to its original state. We see the exit code that semgrep returns and raises the same exit code.

If there is a better way to do it, please let me know by raising an issue.

I'm hoping that one day this will be a feature in Semgrep itself. Until then feel free to use this hook in your pre-commit configuration.

## Usage

1. Add the following to your `.pre-commit-config.yaml` file

    ```yaml
    repos:
    - repo: https://github.com/navhits/semgrep-precommit
    rev: 'v0.2.0'
    hooks:
        - id: semgrep
        # See semgrep.dev/rulesets to select a ruleset and copy its URL
        # Replace auto with the ruleset
        args: ["--config", "auto", "--error", "--disable-version-check", "--quiet", "--skip-unknown-extensions"]
    ```

2. Ensure you have pre-commit installed

    ```bash
    pip3 install pre-commit
    ```

3. Install the pre-commit hook

    ```bash
    pre-commit install
    ```

## Note

The hook was written to work with Python 3.10 and above. If you are using an older version of Python, please upgrade to Python 3.10 or later.
## Troubleshooting

1. I get an error on macOS for `Library not found: libssl.1.1.dylib` on macOS
    * Try installing openssl via brew `brew install openssl@1.1`
    * Add the software to your path with `echo 'export PATH="/opt/homebrew/opt/openssl@1.1/bin:$PATH"' >> ~/.zshrc`
    * Create a symlink with `brew link openssl@1.1`

# handoff-to-owner

Reference implementation of the agent-to-human ownership handoff.

## Problem

An AI agent creates a repository from its own OS user. The human who owns the
work may not be able to use git, and the agent may lose access if ownership is
transferred without ACLs. This tool makes the handoff one operation and removes
itself when used as a one-shot copy.

## Requirements

- Linux/POSIX environment;
- `sudo`;
- `setfacl`;
- `git` is optional, but `safe.directory` handling requires it.

## Two modes

### One-shot copy

Copy the script into the target folder, add it to the local git exclude, and
run it:

```bash
cp handoff-to-owner.sh /path/to/target/handoff-to-owner.sh
chmod 755 /path/to/target/handoff-to-owner.sh
printf '%s\n' 'handoff-to-owner.sh' >> /path/to/target/.git/info/exclude

sudo bash /path/to/target/handoff-to-owner.sh \
  --owner alice \
  --agent agent-user
```

In this mode the target defaults to the script folder, and the script deletes
itself and its exclude line after a successful handoff.

### Reusable mode

Run the canonical tool with an explicit target:

```bash
sudo bash handoff-to-owner.sh \
  --owner alice \
  --agent agent-user \
  --target /path/to/target
```

In this mode the script is kept.

## What it does

- requires explicit `--owner` and `--agent`; no names are hardcoded;
- refuses `/`;
- refuses to run in the canonical tools directory without `--target`;
- `chown -R` transfers ownership to the human, using the owner's primary group;
- `setfacl` preserves agent access, including default ACLs on directories;
- adds `safe.directory` for both users when the target is a git repository;
- in one-shot mode removes its `.git/info/exclude` line and itself.

## Local exclude, not `.gitignore`

- `.git/info/exclude` is local: it is not committed and is not cloned.
- `.gitignore` is a tracked file; it would pollute the repository and become
  visible to everyone.
- The exclude entry protects from `git add .` and `git add -A`; it does not
  protect from `git add -f` or an explicit path.
- Hiding the script from `git status` is the price of that protection. Verify
  after handoff: `test ! -e handoff-to-owner.sh`.

## Safety

- only for folders created by an agent for a human owner;
- does not change file contents and does not replace backups;
- no secrets are stored in the script;
- if `setfacl` is unavailable, it stops instead of leaving the agent without
  access.

## Why this tool lives here

This is a deliberately small, self-contained helper that belongs to the
methodology's onboarding. It has no separate release cycle. If it grows tests,
dependencies or multiple consumers, extract it into its own repository.

See [the pattern note](../../docs/meta/knowledge/2026-10-25_1-KA-agent-created-repo-handoff.md).

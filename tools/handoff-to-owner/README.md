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

### Reusable (recommended)

Run the canonical tool with an explicit target. Nothing is copied into the
target, nothing is added to `.git/info/exclude`, and nothing is deleted:

```bash
sudo bash handoff-to-owner.sh \
  --owner alice \
  --agent agent-user \
  --target /path/to/target
```

This is the normal template action: replace only `--target`. It is
idempotent and can be repeated.

### One-shot copy (portable target only)

Use this only when the folder will leave the workspace and the canonical
tool will not be available. Copy only the script, not the whole directory
(the `.canonical` marker makes the script refuse to run in place):

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

## What it does

- requires explicit `--owner` and `--agent`; no names are hardcoded;
- refuses `/`;
- refuses to run in the canonical tools directory without `--target`, and
  refuses any target directory marked `.canonical`;
- applies the agent ACL and default ACLs for both users **before** changing
  ownership; if ACLs are not supported, it aborts without changing ownership;
- `chown -R` transfers ownership to the human, using the owner's primary group;
- adds `safe.directory` for both users when the target is a git repository,
  then checks `git status` for both and warns if it fails;
- replaces the repository-local `user.name`/`user.email` with the owner's
  global identity; if the owner has no global identity, removes the local one
  so commits are not authored as the agent;
- in one-shot mode removes its `.git/info/exclude` line and itself.

## runuser alternative

The tool runs as root but uses `sudo -H -u` internally to write each user's
global git config. On Linux systems where nested sudo is undesirable, the
same commands can use `runuser -u <user> --`; `runuser` is root-only and
does not show the sudo lecture. The reference implementation keeps `sudo`
for portability.

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
- does not change tracked file contents and does not replace backups;
- no secrets are stored in the script;
- if `setfacl` is unavailable or the filesystem does not support ACLs, it
  stops before changing ownership instead of leaving the agent without access.

## When a manual sequence is enough

For one local repository, three commands are often simpler and easier to
audit than this tool:

1. apply the agent ACL **before** changing ownership;
2. `chown` the repository to the human;
3. add `safe.directory` for the agent (it is no longer the owner).

Use this tool when the handoff repeats, when users or paths vary, or when the
folder must be portable and self-contained.

## Why this tool lives here

This is a deliberately small, self-contained helper that belongs to the
methodology's onboarding. It has no separate release cycle. If it grows tests,
dependencies or multiple consumers, extract it into its own repository.

See [the pattern note](../../docs/meta/knowledge/2026-10-25_1-KA-agent-created-repo-handoff.md).

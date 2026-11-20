## What is pre-commit?
Pre-commit is a tool which automatically runs before the commit is finalized. It can either clean the code or format it or outright decline the commit

## How to use it?

Install pre commit with

```
pip install pre-commit
```

Then use the following command from

```
pre-commit install
```

It will install a hook to .git

Now pre-commits will run automatically

### You can also run pre-commit in your repo manually for all files with the following command:

```
pre-commit run --all-files
```

## Information on what the installed hooks do can be found here:

`*https://github.com/pre-commit/pre-commit-hooks/blob/main/.pre-commit-hooks.yaml*`

## And information for Ruff can be found here:

`*https://github.com/astral-sh/ruff-pre-commit*`

## You can also skip hooks with:

```
git commit -m "message" --no-verify
```

But this should be used in very rare situations.

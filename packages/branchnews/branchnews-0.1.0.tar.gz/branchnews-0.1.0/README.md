`branchnews` helps you used branch-based file names with `towncrier`.

If you are not already familiar with [towncrier](https://pypi.org/project/towncrier/),
it is a great tool for generating changelogs, based on *news fragment files*.

However, a difficulty arises if you want
to record a news fragment for a PR (pull request) that does not correspond to an
existing issue.
In such cases, it is hard to choose a name for the fragment file while preparing
the PR, because you do not know the number the PR will receive, until after it has
already been opened.

The solution provided by `branchnews` is to let you instead record the fragment
under a filename based on your GitHub username and the name of your topic branch,
like this:

```
USERNAME.BRANCHNAME.branchnews.NEWS_TYPE.txt
```

The

```commandline
$ branchnews create
```

command helps you generate this file.

The one requirement is that, when the PR is merged, you accept the standard GitHub
merge commit message of the form,

```
Merge pull request #NUMBER from USERNAME/BRANCHNAME
```

Then, when you are ready to generate your changelog, first use

```commandline
$ branchnews rename
```

to rename the fragment files. This will rename files
like `USERNAME.BRANCHNAME.branchnews.NEWS_TYPE.txt`
to `NUMBER.NEWS_TYPE.txt`, using the merge commit messages from the git log to
determine the PR numbers.

After committing these renames, you can procede to use `towncrier` as normal.

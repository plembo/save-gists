# Save GitHub gists to disk

Save all gists from GitHub, including comments.
Requires the PyGithub library (``pip install PyGithub>=1.47``).
Pass a personal access token with the scope "gist" as the first
argument.

Original code by Toby Fleming. "Backup all Gists from GitHub". _tobywf_,
6 April 2020, https://tobywf.com/2020/04/backup-all-gists-from-github/
(https://gist.github.com/tobywf/d7b4378417f4a10a75dd7245ec557240).

Updated to use environment variable for token and argv for output path.

Syntax is:

```bash
$ ./save-gists.py -path /backup/github.com/plembo/gists
```


#!/usr/bin/env python
"""
Save all gists from GitHub, including comments.
Requires the PyGithub library (``pip install PyGithub>=1.47``).
Pass a personal access token with the scope "gist" as the first
argument.

Original code by Toby Fleming. "Backup all Gists from GitHub". _tobywf_,
6 April 2020, https://tobywf.com/2020/04/backup-all-gists-from-github/
(https://gist.github.com/tobywf/d7b4378417f4a10a75dd7245ec557240).

Updated to use environment variable for token and argv for output path.

SYNTAX: ./save-gists.py -path /backup/github.com/plembo/gists
"""
import os
import sys
from github import Github
from pathlib import Path

token = os.getenv('GITHUB_TOKEN')
outpath = str(sys.argv[2])
base = Path(outpath)
gh = Github(token)
user = gh.get_user()
info = [
    "# Gists",
    "",
]

for gist in user.get_gists():
    print(gist.id)
    gist_path = base / gist.id
    gist_path.mkdir(exist_ok=True)

    # index
    visibility = "" if gist.public else "🔒"
    gist_link = f"[{gist.id}]({gist.html_url})"
    info.extend([
        f"## {gist_link} {visibility}",
        "",
        f"Created: {gist.created_at.isoformat(timespec='seconds')}Z / "
        f"Updated: {gist.updated_at.isoformat(timespec='seconds')}Z",
        "",
        gist.description,
        "",
    ])
    info.extend([
        f"* `{file.filename}` - {file.language} - {file.last_modified}"
        for file in gist.files.values()
    ])
    info.append("")

    # comments
    if gist.comments:
        comments = [
            f"# Comments for {gist_link}",
            "",
        ]
        for comment in gist.get_comments():
            comments.extend([
                f"[{comment.id}]({gist.html_url}#gistcomment-{comment.id}) - "
                f"[{comment.user.login}]({comment.user.html_url}) - "
                f"Created: {comment.created_at.isoformat(timespec='seconds')}Z / ",
                f"Updated: {comment.updated_at.isoformat(timespec='seconds')}Z",
                "",
                comment.body,
                "",
            ])
        comment_path = gist_path / "comments.md"
        comment_path.write_text("\n".join(comments), encoding="utf-8")

    # files
    for file in gist.files.values():
        print("*", file.filename)
        file_path = gist_path / file.filename
        file_path.write_text(file.content, encoding="utf-8")

index_path = base / "index.md"
index_path.write_text("\n".join(info), encoding="utf-8")

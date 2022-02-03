import os
from os import listdir
import re

SUMMARY_SIZE = 300


def get_summary(content_list):
    summary = ""
    for l in content_list:
        if l.startswith("#") or l.startswith("!") or l.startswith("["):
            continue

        summary += l

        if len(summary) > SUMMARY_SIZE:
            continue

    # fix path
    summary = summary.replace("[../../authors", "[./authors")

    return summary[:SUMMARY_SIZE] + " ..."


def generate_toc():
    pattern = r"^\s*-\s*file\:\s*(.*?)$"
    
    with open("_toc.yml") as f:
        content = f.read()

    files = re.findall(pattern, content, flags=re.MULTILINE)

    content = ""

    template = """
```{admonition} {{title}}
![header]({{header-files}})
{{summary}}
[see more]({{file}})

```
    """

    for fname in files:
        if not fname.startswith("articles"):
            continue

        with open(fname) as f:
            f_content = f.readlines()
            f_title = f_content[0].replace("#", "").strip()
            header_file = os.sep.join(fname.split(os.sep)[:-1] + ["header.png"])

            if not os.path.exists(header_file):
                header_file = "images/empty.png"

            content += (
                template.replace("{{title}}", f_title)
                    .replace("{{file}}", fname)
                    .replace("{{header-files}}", header_file)
                    .replace("{{summary}}", get_summary(f_content))
            )
    
    return content


def main():
    content = ""
    with open("intro.md") as f:
        content = f.read()

    pattern = r"<!--content:start-->(.*)((\s)+(.*))+<!--content:end-->"
    toc = f"<!--content:start-->\n{generate_toc()}\n<!--content:end-->"

    content = re.sub(pattern, toc, content)

    with open("intro.md", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()

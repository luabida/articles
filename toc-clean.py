import re


def main():
    content = ""
    with open("intro.md") as f:
        content = f.read()

    pattern = r"<!--content:start-->(.*)((\s)+(.*))+<!--content:end-->"
    no_toc = f"<!--content:start-->\n<!--content:end-->"

    content = re.sub(pattern, no_toc, content)

    with open("intro.md", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()

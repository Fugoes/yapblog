import subprocess


def markdown_to_html(markdown_content):
    p = subprocess.Popen(["pandoc", "--from=markdown", "--to=html"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = p.communicate(input=markdown_content.encode())
    return output[0].decode()

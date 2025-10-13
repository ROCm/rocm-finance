from docutils import nodes
from pathlib import Path
import re


def icon_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """
    Inline role for Font Awesome icons. See
    https://fontawesome.com/search?ip=brands&o=r to find available icons.

    Example rST usage:

    :icon:`fa-brands fa-redhat fa-lg`
    :icon:`fa-brands fa-redhat fa-lg <https://redhat.com>`

    Example MyST Markdown usage:

    {icon}`fa-brands fa-redhat fa-lg`
    {icon}`fa-brands fa-redhat fa-lg <https://redhat.com>`
    """
    # Parse for optional URL in angle brackets
    match = re.match(r"^(.+?)\s*(?:<(.+?)>)?$", text.strip())
    if not match:
        msg = inliner.reporter.error(
            f"Invalid icon role format: {text}", line=lineno
        )
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    icon_classes = match.group(1).strip()
    url = match.group(2)

    icon_html = f'<i class="{icon_classes}"></i>'

    if url:
        html = f'<a href="{url}">{icon_html}</a>'
    else:
        html = icon_html

    node = nodes.raw("", html, format="html")
    return [node], []


def setup(app):
    app.add_role("icon", icon_role)

    static_assets_dir = Path(__file__).parent / "static"
    app.config.html_static_path.append(str(static_assets_dir))
    app.add_css_file("rocm-docs-custom.css")


    return {"version": "6.9", "parallel_read_safe": True}

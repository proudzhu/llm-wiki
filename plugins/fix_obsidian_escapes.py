import re
import os
import logging
import urllib.parse

from mkdocs.plugins import BasePlugin
from mkdocs.utils import get_relative_url

log = logging.getLogger(f"mkdocs.plugins.{__name__}")

AUTOLINK_RE = r'\[([^\]]+)\]\((([^)/]+\.(md|png|jpg))(#.*)*)\)'

ROAMLINK_RE = r"""(?<!\!)\[\[(.*?)(\#.*?)?(?:(?:\\\||\|)([\D][^\|\]\\]+[\d]*))?(?:(?:\\\||\|)(\d+)(?:x(\d+))?)?\]\]"""

EMBED_ROAMLINK_RE = r"""\!\[\[(.*?)(?:(?:\\\||\|)([^\|\]\\]+))?(?:(?:\\\||\|)(\d+)(?:x(\d+))?)?\]\]"""

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}


def _to_page_relative(path_from_docs_root, page_src_path):
    page_dir = os.path.dirname(page_src_path).replace("\\", "/")
    if not page_dir:
        return path_from_docs_root
    depth = page_dir.count("/") + 1
    prefix = "../" * depth
    return prefix + path_from_docs_root


def _strip_wiki_prefix(path):
    if path.startswith("wiki/"):
        return path[5:]
    while "../wiki/" in path:
        path = path.replace("../wiki/", "../")
    return path


class AutoLinkReplacer:
    def __init__(self, base_docs_url, page_url):
        self.base_docs_url = base_docs_url
        self.page_url = page_url

    def __call__(self, match):
        filename = urllib.parse.unquote(match.group(3).strip())
        rel_link_url = ''
        for root, dirs, files in os.walk(self.base_docs_url):
            for name in files:
                if name == filename:
                    abs_path = os.path.join(root, name)
                    rel_link_url = os.path.relpath(abs_path, self.base_docs_url).replace("\\", "/")
        if rel_link_url == '':
            log.warning(f"AutoLinksPlugin unable to find {filename} in directory {self.base_docs_url}")
            return match.group(0)
        rel_link_url = _to_page_relative(rel_link_url, self.page_url)
        if (match.group(5) == None):
            link = match.group(0).replace(match.group(2), rel_link_url)
        else:
            link = match.group(0).replace(match.group(2),
                                          rel_link_url + match.group(5))
        return link


class EmbedRoamLinkReplacer:
    """Resolve Obsidian embed wikilinks `![[path|alt|WxH]]` into markdown images.

    The path is treated as **vault-absolute** (relative to the project root,
    which is the Obsidian vault root). For paths under `raw/`, the file lives
    one level above `docs_dir`, so the substitution rewrites the URL to be
    relative to the page's source directory.
    """

    def __init__(self, base_docs_url, page_url):
        self.base_docs_url = base_docs_url
        self.page_url = page_url

    def __call__(self, match):
        whole = match.group(0)
        target = (match.group(1) or "").strip().rstrip("\\")
        alt = (match.group(2) or "").strip()
        width = match.group(3) or ""
        height = match.group(4) or ""

        if not target:
            return whole

        ext = os.path.splitext(target)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            return whole

        if target.startswith("wiki/"):
            url_from_docs = target[len("wiki/"):]
        else:
            url_from_docs = target

        rel_url = _to_page_relative(url_from_docs, self.page_url)

        if not alt:
            alt = os.path.basename(target)

        link = f"![{alt}]({rel_url})"
        if width and not height:
            link += f'{{ width="{width}" }}'
        elif height and not width:
            link += f'{{ height="{height}" }}'
        elif width and height:
            link += f'{{ width="{width}"; height="{height}" }}'
        return link


class RoamLinkReplacer:
    def __init__(self, base_docs_url, page_url):
        self.base_docs_url = base_docs_url
        self.page_url = page_url

    def simplify(self, filename):
        return re.sub(r"[\-_ ]", "", filename.lower()).replace(".md", "")

    def gfm_anchor(self, title):
        if title:
            title = title.strip().lower()
            title = re.sub(r'[^\w\u4e00-\u9fff\- ]', "", title)
            title = re.sub(r' +', "-", title)
            return title
        else:
            return ""

    def __call__(self, match):
        whole_link = match.group(0)
        filename = match.group(1).strip().rstrip("\\") if match.group(1) else ""
        title = match.group(2).strip() if match.group(2) else ""
        format_title = self.gfm_anchor(title)
        alias = match.group(3) if match.group(3) else ""
        width = match.group(4) if match.group(4) else ""
        height = match.group(5) if match.group(5) else ""

        rel_link_url = ''
        if filename:
            if '/' in filename:
                if 'http' in filename:
                    rel_link_url = filename
                else:
                    rel_file = filename
                    if rel_file.startswith("wiki/"):
                        rel_file = rel_file[5:]
                    if not '.' in os.path.basename(filename):
                        rel_file = rel_file + ".md"
                    rel_file = rel_file.lstrip("/")
                    abs_linker_url = os.path.dirname(os.path.join(self.base_docs_url, self.page_url))
                    if rel_file.startswith("../") or rel_file.startswith("./"):
                        abs_path = os.path.normpath(os.path.join(abs_linker_url, rel_file))
                    else:
                        abs_path = os.path.normpath(os.path.join(self.base_docs_url, rel_file))
                    if os.path.isfile(abs_path):
                        rel_link_url = os.path.relpath(abs_path, self.base_docs_url).replace("\\", "/")
                    else:
                        rel_link_url = rel_file.replace("\\", "/")
                    if title:
                        rel_link_url = rel_link_url + '#' + format_title
            else:
                for root, dirs, files in os.walk(self.base_docs_url):
                    for name in files:
                        if self.simplify(name) == self.simplify(filename):
                            abs_path = os.path.join(root, name)
                            rel_link_url = os.path.relpath(abs_path, self.base_docs_url).replace("\\", "/")
                            if title:
                                rel_link_url = rel_link_url + '#' + format_title
            if rel_link_url == '':
                log.warning(f"RoamLinksPlugin unable to find {filename} in directory {self.base_docs_url}")
                return whole_link
            if not rel_link_url.startswith('http'):
                rel_link_url = _to_page_relative(rel_link_url.split('#')[0], self.page_url) + ('#' + format_title if title else '')
        else:
            rel_link_url = '#' + format_title

        if filename:
            if alias:
                link = f'[{alias}]({rel_link_url})'
            else:
                link = f'[{filename+title}]({rel_link_url})'
        else:
            if alias:
                link = f'[{alias}]({rel_link_url})'
            else:
                link = f'[{title}]({rel_link_url})'

        if width and not height:
            link = f'{link}{{ width="{width}" }}'
        elif not width and height:
            link = f'{link}{{ height="{height}" }}'
        elif width and height:
            link = f'{link}{{ width="{width}"; height="{height}" }}'

        return link


class FixObsidianEscapesPlugin(BasePlugin):
    def on_page_markdown(self,
                         markdown,
                         page,
                         config,
                         site_navigation=None,
                         **kwargs):

        base_docs_url = config["docs_dir"]
        page_url = page.file.src_path

        placeholders = []
        def _protect(match):
            placeholders.append(match.group(0))
            return f"\x00PLACEHOLDER{len(placeholders) - 1}\x00"

        markdown = re.sub(r'```[\s\S]*?```', _protect, markdown)
        markdown = re.sub(r'`[^`]+`', _protect, markdown)

        page_dir = os.path.dirname(page_url).replace("\\", "/")
        if page_dir:
            prefix = "../" * (page_dir.count("/") + 1)
        else:
            prefix = ""

        def fix_img_path(match):
            alt = match.group(1)
            url = match.group(2)
            if url.startswith("http") or url.startswith("/") or url.startswith("#"):
                return match.group(0)
            if url.startswith("raw/"):
                return f"![{alt}]({prefix}{url})"
            return match.group(0)

        markdown = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", fix_img_path, markdown)

        def strip_wiki_link_prefix(match):
            text = match.group(1)
            url = match.group(2)
            return f'[{text}]({_strip_wiki_prefix(url)})'

        markdown = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', strip_wiki_link_prefix, markdown)

        markdown = re.sub(AUTOLINK_RE,
                          AutoLinkReplacer(base_docs_url, page_url), markdown)
        markdown = re.sub(EMBED_ROAMLINK_RE,
                          EmbedRoamLinkReplacer(base_docs_url, page_url), markdown)
        markdown = re.sub(ROAMLINK_RE,
                          RoamLinkReplacer(base_docs_url, page_url), markdown)

        for i, original in enumerate(placeholders):
            markdown = markdown.replace(f"\x00PLACEHOLDER{i}\x00", original)

        return markdown

    def on_post_page(self, output, page, config, **kwargs):
        page_url = page.file.url
        docs_dir_name = os.path.basename(config["docs_dir"])

        def fix_link_href(match):
            href = match.group(1)
            if href.startswith('http') or href.startswith('/') or href.startswith('#') or href.startswith('mailto'):
                return match.group(0)
            if '://' in href:
                return match.group(0)
            path_part = href.split('#')[0]
            anchor_part = '#' + href.split('#')[1] if '#' in href else ''
            if path_part.endswith('/'):
                return match.group(0)
            last_segment = path_part.split('/')[-1]
            if last_segment.endswith('.md'):
                target_url = path_part[:-3] + '.html'
            elif '.' not in last_segment:
                target_url = path_part + '.html'
            else:
                return match.group(0)
            if target_url.startswith(docs_dir_name + '/'):
                target_url = target_url[len(docs_dir_name) + 1:]
            if '/' in target_url and not target_url.startswith('../'):
                target_url = get_relative_url(target_url, page_url)
            return f'href="{target_url}{anchor_part}"'

        output = re.sub(r'href="([^"]+)"', fix_link_href, output)
        return output

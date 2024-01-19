from __future__ import annotations

import datetime
import platform
import os
import os.path
import shutil  # used to remove a non-empty directory, copy files


from pathlib import Path

from ..parser.MarkdownPage import MarkdownPage
from ..lib import get_rel_html_url_prefix, slugify_path, formatted_print

"""
This object class helps us with keeping track of all the paths.
There are three types of paths:

- obsidian notes: 'notes'
- proper markdown notes: 'markdown'
- html pages: 'html'

The flow within ObsidianHtml is to get obsidian notes and convert them to markdown notes,
then take the proper markdown notes and convert them to html.

When we set the note path as a source, then we will know what the markdown path will be, based on the config.
And when we know the markdown path we can set the html path.

Because the first step can be skipped, there is some complexity, but otherwise, if we give the note path as a source,
we can compile all the relevant paths in one pass.

The links have some complexity because we can configure to use absolute links or relative links.
For simplicity's sake, we just compile both link types within the same function. There are some functions to automatically
get the correct link based on the configurations.
"""


class FileObject:
    pb = None  # contains all config, paths, etc (global pass in config object)
    path = None  # hashtable with all relevant file paths
    link = None  # hashtable with all links
    metadata = None  # information on the note, such as modified_date
    md = None  # MarkdownPage object
    node = None  # Node object, filled in, linked to network_tree

    processed_ntm = False  # whether the note has already been processed in the note --> markdown flow
    processed_mth = False  # whether the note has already been processed in the markdown --> html flow

    def __init__(self, pb):
        self.pb = pb

        self.path = {}
        self.link = {}
        self.metadata = {}

        # These values are not set under self.compile_metadata()
        # So the default values need to be set here.
        self.metadata["is_entrypoint"] = False

    def load_markdown_page(self, input_type):
        self.md = MarkdownPage(self, input_type)
        return self.md

    def fullpath(self, output):
        return self.path[output]["file_absolute_path"]

    def is_valid_note(self, output):
        if self.fullpath(output).exists() is False:
            return False
        if self.fullpath(output).suffix != ".md":
            return False
        return True

    def init_note_path(self, source_file_absolute_path, compile_metadata=True):
        self.oh_file_type = "obs_to_md"

        # Configured folders
        source_folder_path = self.pb.paths["obsidian_folder"]
        target_folder_path = self.pb.paths["md_folder"]

        # Note
        self.path["note"] = {}
        self.path["note"]["folder_path"] = source_folder_path
        self.path["note"]["file_absolute_path"] = source_file_absolute_path
        self.path["note"]["file_relative_path"] = source_file_absolute_path.relative_to(source_folder_path)
        self.path["note"]["og_file_relative_path"] = self.path["note"]["file_relative_path"]
        self.path["note"]["suffix"] = self.path["note"]["file_absolute_path"].suffix[1:]

        # Markdown
        self.path["markdown"] = {}
        self.path["markdown"]["folder_path"] = target_folder_path

        ## Path rewrites
        if self.path["note"]["file_relative_path"] == self.pb.paths["rel_obsidian_entrypoint"]:
            # rewrite path to index.md if the note is configured as the entrypoint.
            self.metadata["is_entrypoint"] = True
            
            self.path["markdown"]["file_absolute_path"] = target_folder_path.joinpath("index.md")
            self.path["markdown"]["file_relative_path"] = self.path["markdown"]["file_absolute_path"].relative_to(target_folder_path)
            
            # also add self to pb.index.files under the key 'index.md' so it is findable
            self.pb.index.files["index.md"] = self
        else:
            self.path["markdown"]["file_absolute_path"] = target_folder_path.joinpath(self.path["note"]["file_relative_path"])
            self.path["markdown"]["file_relative_path"] = self.path["note"]["file_relative_path"]

        self.path["markdown"]["og_file_relative_path"] = self.path["note"]["file_relative_path"]
        self.path["markdown"]["suffix"] = self.path["markdown"]["file_absolute_path"].suffix[1:]

        # Metadata
        self.metadata["depth"] = self._get_depth(self.path["note"]["file_relative_path"])
        if compile_metadata:
            self.compile_metadata(source_file_absolute_path)  # is_note, creation_time, modified_time, is_video, is_audio, is_includable

    def init_markdown_path(self, source_file_absolute_path=None):
        self.oh_file_type = "md_to_html"

        source_folder_path = self.pb.paths["md_folder"]
        target_folder_path = self.pb.paths["html_output_folder"]

        # compile the path['markdown'] section, or reuse the section from the previous step
        if source_file_absolute_path is None:
            source_file_absolute_path = self.path["markdown"]["file_absolute_path"]
        else:
            self.path["markdown"] = {}
            self.path["markdown"]["folder_path"] = source_folder_path
            self.path["markdown"]["file_absolute_path"] = source_file_absolute_path
            self.path["markdown"]["file_relative_path"] = source_file_absolute_path.relative_to(source_folder_path)
            self.path["markdown"]["og_file_relative_path"] = source_file_absolute_path.relative_to(source_folder_path)
            self.path["markdown"]["suffix"] = source_file_absolute_path.suffix[1:]

        # html
        self.path["html"] = {}
        self.path["html"]["folder_path"] = target_folder_path

        def convert_md_to_hmtl(rel_path_posix):
            if rel_path_posix[-3:] == ".md":
                return Path(rel_path_posix[:-3] + ".html")
            return Path(rel_path_posix)

        src_rel_path_posix = self.path["markdown"]["file_relative_path"].as_posix()
        src_og_rel_path_posix = self.path["markdown"]["og_file_relative_path"].as_posix()

        if src_rel_path_posix == self.pb.paths["rel_md_entrypoint_path"]:
            # rewrite path to index.md if the markdown note is configured as the entrypoint.
            self.metadata["is_entrypoint"] = True
            target_rel_path_posix = "index.md"

        # rewrite .md to .html
        src_rel_path = convert_md_to_hmtl(src_rel_path_posix)
        src_og_rel_path = convert_md_to_hmtl(src_og_rel_path_posix)

        # calc paths
        self.path["html"]["file_absolute_path"] = target_folder_path.joinpath(src_rel_path)
        self.path["html"]["file_relative_path"] = src_rel_path
        self.path["html"]["og_file_relative_path"] = src_og_rel_path
        self.path["html"]["suffix"] = self.path["html"]["file_absolute_path"].suffix[1:]

        # slugify paths
        if self.pb.gc("toggles/slugify_html_links", cached=True):
            _slug_path = slugify_path(self.path["html"]["file_absolute_path"].as_posix())
            self.path["html"]["file_absolute_path"] = Path(_slug_path)

            _slug_path = slugify_path(self.path["html"]["file_relative_path"].as_posix())
            self.path["html"]["file_relative_path"] = Path(_slug_path)

            self.pb.index.aliased_files[_slug_path] = self
            self.pb.index.aliased_files[_slug_path[:-5] + ".md"] = self

        # Metadata
        # call to self.compile_metadata() should be done manually in the calling function
        self.metadata["depth"] = self._get_depth(self.path["html"]["file_relative_path"])

    def compile_metadata(self, path, cached=False):
        if cached and "is_note" in self.metadata:
            return
        self.set_times(path)
        self.set_file_types(path)

    def set_file_types(self, path):
        self.metadata["is_note"] = False
        self.metadata["is_video"] = False
        self.metadata["is_audio"] = False
        self.metadata["is_embeddable"] = False
        self.metadata["is_includable_file"] = False
        self.metadata["is_parsable_note"] = False

        suffix = path.suffix[1:].lower()

        if suffix == "md":
            self.metadata["is_note"] = True
        if suffix in self.pb.gc("included_file_suffixes", cached=True):
            self.metadata["is_includable_file"] = True
        if suffix in self.pb.gc("video_format_suffixes", cached=True):
            self.metadata["is_video"] = True
        if suffix in self.pb.gc("audio_format_suffixes", cached=True):
            self.metadata["is_audio"] = True
        if suffix in self.pb.gc("embeddable_file_suffixes", cached=True):
            self.metadata["is_embeddable"] = True

        if path.exists() and self.metadata["is_note"]:
            self.metadata["is_parsable_note"] = True

    def set_times(self, path):
        if platform.system() == "Windows" or platform.system() == "Darwin":
            self.metadata["creation_time"] = datetime.datetime.fromtimestamp(os.path.getctime(path)).isoformat()
            self.metadata["modified_time"] = datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
        else:
            self.metadata["modified_time"] = datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat()

    def get_depth(self, mode):
        return self._get_depth(self.path[mode]["file_relative_path"])

    def _get_depth(self, rel_path):
        return rel_path.as_posix().count("/")

    def get_link(self, link_type, origin: "FileObject" = None, origin_rel_dst_path_str=None, encode_special=True):
        link = self._get_link(link_type, origin, origin_rel_dst_path_str)

        if self.pb.gc("toggles/slugify_html_links", cached=True) and link_type == "html":
            return slugify_path(link)

        # when doing a manual url_encode on the entire link returned by this function,
        # be sure to set encode_special=False to avoid double encoding
        if encode_special:
            # escape question mark
            if link_type == "html":
                link = link.replace("?", "%3F")

        return link

    def _get_link(self, link_type, origin: "FileObject" = None, origin_rel_dst_path_str=None):
        # Get origin_rel_dst_path_str
        if origin_rel_dst_path_str is None:
            if origin is not None:
                origin_rel_dst_path_str = origin.path[link_type]["file_relative_path"].as_posix()
            else:
                origin_rel_dst_path_str = self.path[link_type]["file_relative_path"].as_posix()

        # recompile links for the given origin_path and return correct link (absolute or relative)
        if link_type == "markdown":
            self.compile_markdown_link(origin_rel_dst_path_str)

            if self.pb.gc("toggles/relative_path_md", cached=True):
                return self.link[link_type]["relative"]

        elif link_type == "html":
            self.compile_html_link(origin_rel_dst_path_str)

            if self.pb.gc("toggles/relative_path_html", cached=True):
                return self.link[link_type]["relative"]

        return self.link[link_type]["absolute"]

    def compile_markdown_link(self, origin_rel_dst_path_str):
        self.link["markdown"] = {}

        # Absolute
        web_abs_path = self.path["markdown"]["file_relative_path"].as_posix()
        self.link["markdown"]["absolute"] = "/" + web_abs_path

        # Relative
        prefix = get_rel_html_url_prefix(origin_rel_dst_path_str)
        self.link["markdown"]["relative"] = prefix + "/" + web_abs_path

    def compile_html_link(self, origin_rel_dst_path_str):
        self.link["html"] = {}

        # Absolute
        html_url_prefix = self.pb.gc("html_url_prefix")
        abs_link = self.path["html"]["file_relative_path"].as_posix()
        self.link["html"]["absolute"] = html_url_prefix + "/" + abs_link

        # Relative
        prefix = get_rel_html_url_prefix(origin_rel_dst_path_str)
        self.link["html"]["relative"] = prefix + "/" + self.path["html"]["file_relative_path"].as_posix()

    def copy_file(self, mode):
        if mode == "ntm":
            src_file_path = self.path["note"]["file_absolute_path"]
            dst_file_path = self.path["markdown"]["file_absolute_path"]
        elif mode == "mth":
            src_file_path = self.path["markdown"]["file_absolute_path"]
            dst_file_path = self.path["html"]["file_absolute_path"]

        if not src_file_path.exists():
            if self.pb.gc("toggles/warn_on_skipped_file", cached=True):
                formatted_print("ERROR", f"copying  {src_file_path} to {dst_file_path}, file not found.")
            return

        link_mode = self.pb.gc("copy_output_file_method", cached=True)
        resolve_links = self.pb.gc("resolve_output_file_links", cached=True)
        if link_mode == "default":
            link_mode = "copy"
        if link_mode != "copy" and resolve_links:
            src_file_path = os.path.realpath(src_file_path)

        if self.pb.gc("toggles/verbose_printout", cached=True):
            print(f"{'Copy' if link_mode == 'copy' else 'Link'}ing file (mode={mode}) from {src_file_path} to {dst_file_path}")

        dst_file_path.parent.mkdir(parents=True, exist_ok=True)
        if link_mode == "copy":
            shutil.copyfile(src_file_path, dst_file_path)
        elif link_mode == "symlink":
            if not os.path.exists(dst_file_path):
                os.symlink(src_file_path, dst_file_path)
        elif link_mode == "hardlink":
            if not os.path.exists(dst_file_path):
                os.link(src_file_path, dst_file_path)
        else:
            raise Exception(f'Bad copy_output_file_method "{copy_output_file_method}", expected one of: default, copy, symlink, hardlink')

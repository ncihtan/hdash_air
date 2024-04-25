"""Web Writer."""
from datetime import datetime, timedelta
from typing import List
import humanize
from jinja2 import Environment, PackageLoader, select_autoescape
from hdash.synapse.atlas_info import AtlasInfo
from hdash.util.categories import Categories


class WebWriter:
    """Web Writer."""

    def __init__(self, atlas_list: List[AtlasInfo]):
        """Create new Web Writer."""
        self.atlas_list = atlas_list
        self.atlas_html_map = {}
        self.index_html = None
        self.matrix_html_map = {}
        self.categories = Categories()
        self.total_storage = 0
        for atlas_info in self.atlas_list:
            num_errors = 0
            self.total_storage += atlas_info.stats.total_file_size
            validation_list = atlas_info.validation_list
            for validation in validation_list:
                num_errors += len(validation.error_list)
            atlas_info.num_errors = num_errors

        self.env = self._get_template_env()
        self.now = datetime.now()
        self.now_str = self.now.strftime("%Y-%m-%d %I:%M:%S %p")
        self.next_update = self.now + timedelta(hours=4)
        self.next_update_str = self.next_update.strftime("%Y-%m-%d %I:%M:%S %p")

        self._generate_index_html()
        self._generate_atlas_pages()

    def _generate_index_html(self):
        template = self.env.get_template("index.html")
        storage_human = humanize.naturalsize(self.total_storage)
        self.index_html = template.render(
            now=self.now_str,
            next_update=self.next_update_str,
            atlas_list=self.atlas_list,
            storage_human=storage_human,
        )

    def _generate_atlas_pages(self):
        for atlas_info in self.atlas_list:
            atlas_info.meta_list = sorted(
                atlas_info.meta_list, key=lambda d: d.atlas_file.category
            )
            template = self.env.get_template("atlas.html")
            html = template.render(now=self.now_str, atlas_info=atlas_info)
            self.atlas_html_map[atlas_info.info.atlas_id] = html

    def _get_template_env(self):
        return Environment(
            loader=PackageLoader("hdash", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )

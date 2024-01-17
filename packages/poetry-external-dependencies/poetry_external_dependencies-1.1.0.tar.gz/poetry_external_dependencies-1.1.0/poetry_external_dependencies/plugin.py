"""Poetry plugin to parse pyproject.toml for external dependencies and add the to the metadata of the built package"""
from cleo.io.io import IO
from poetry.core.masonry.builders.builder import METADATA_BASE, Builder
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry


class ExternalInjector(Plugin):
    """Replace the get_metadata_content method of Peetry's Builder class to include external dependencies
    The external dependency should be specified in the pyproject.toml file following the PEP725 format
    https://peps.python.org/pep-0725/

    eg.
    [external]
    dependencies = ["pkg:generic/ffmpeg"]

    The dependencies will be added as 'Requires-External' fields of the metadata
    """

    def __init__(self):
        self.default_metadata_method = None
        self.dependencies = []

    def activate(self, poetry: Poetry, io: IO):
        if 'external' in poetry.pyproject.data:
            external = poetry.pyproject.data['external']
            if 'dependencies' in external:
                self.dependencies = external['dependencies']
                self.inject_metadata_builder()

    def deactivate(self, poetry: Poetry, io: IO):
        if self.default_metadata_method:
            Builder.get_metadata_content = self.default_metadata_method

    def inject_metadata_builder(injector_plugin):
        # Copied from poetry.core.masonry.builders.builder.py.Builder
        # and modified to add the external dependencies to the metadata
        def get_metadata_content(self) -> str:
            content = METADATA_BASE.format(
                name=self._meta.name,
                version=self._meta.version,
                summary=str(self._meta.summary),
            )

            # Optional fields
            if self._meta.home_page:
                content += f'Home-page: {self._meta.home_page}\n'

            if self._meta.license:
                content += f'License: {self._meta.license}\n'

            if self._meta.keywords:
                content += f'Keywords: {self._meta.keywords}\n'

            if self._meta.author:
                content += f'Author: {self._meta.author}\n'

            if self._meta.author_email:
                content += f'Author-email: {self._meta.author_email}\n'

            if self._meta.maintainer:
                content += f'Maintainer: {self._meta.maintainer}\n'

            if self._meta.maintainer_email:
                content += f'Maintainer-email: {self._meta.maintainer_email}\n'

            if self._meta.requires_python:
                content += f'Requires-Python: {self._meta.requires_python}\n'

            for classifier in self._meta.classifiers:
                content += f'Classifier: {classifier}\n'

            for extra in sorted(self._meta.provides_extra):
                content += f'Provides-Extra: {extra}\n'

            for dep in sorted(self._meta.requires_dist):
                content += f'Requires-Dist: {dep}\n'

            for dep in sorted(injector_plugin.dependencies):
                content += f'Requires-External: {dep}\n'

            for url in sorted(self._meta.project_urls, key=lambda u: u[0]):
                content += f'Project-URL: {url}\n'

            if self._meta.description_content_type:
                content += f'Description-Content-Type: {self._meta.description_content_type}\n'

            if self._meta.description is not None:
                content += f'\n{self._meta.description}\n'

            return content

        # Override the builder method with ours
        injector_plugin.default_metadata_method = Builder.get_metadata_content
        Builder.get_metadata_content = get_metadata_content

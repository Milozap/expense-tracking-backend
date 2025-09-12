import os.path
from typing import Any, Dict, List, Tuple

import yaml
from django.core.management import BaseCommand, CommandError, CommandParser
from django.db import transaction
from django.utils.text import slugify

from apps.categories.models import Category

DEFAULT_CONFIG_PATH = "apps/categories/management/commands/config/categories.yml"
DEFAULT_COLOR = "#cccccc"


class Command(BaseCommand):
    help = "Seed categories from given config .yml (defaults to config/categories.yml)"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--file",
            type=str,
            default=DEFAULT_CONFIG_PATH,
            help="Path to config yml (defaults to config/categories.yml)",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing categories before seeding",
        )

    def _load_yml(self, path: str) -> Dict[str, List[Dict[str, Any]]]:
        if not os.path.exists(path):
            raise CommandError(f"File not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise CommandError(
                "Improper Yml config. The root must have INCOME and EXPENSE keys"
            )
        return data

    def _create_category(
        self,
        name: str,
        category_type: str,
        parent: Category | None = None,
        slug: str | None = None,
        color: str = DEFAULT_COLOR,
    ) -> Tuple[Category, bool]:
        if not slug:
            slug = slugify(name)

        category, created = Category.objects.get_or_create(
            name=str(name.strip()),
            type=category_type,
            parent=parent,
            slug=slug,
            color=color,
        )
        return category, created

    def _process_category_tree(
        self, category_data: Dict[str, Any], category_type: str
    ) -> int:
        """Process a single category node and its children."""
        # Create the parent category
        parent_category_name = category_data.get("name") or ""
        parent_category, parent_created = self._create_category(
            name=parent_category_name,
            category_type=category_type,
            slug=category_data.get("slug") or slugify(parent_category_name),
            color=category_data.get("color") or DEFAULT_COLOR,
        )

        created_count = 1 if parent_created else 0

        # Process children if they exist
        children = category_data.get("children", [])
        for child_node in children:
            child_slug = child_node.get("slug") or slugify(
                f'{category_data.get("name")}/{child_node.get("name")}'
            )
            _, child_created = self._create_category(
                name=child_node["name"],
                category_type=category_type,
                parent=parent_category,
                slug=child_slug,
                color=child_node.get("color") or DEFAULT_COLOR,
            )
            created_count += 1 if child_created else 0

        return created_count

    @transaction.atomic
    def handle(self, *args: Any, **kwargs: Any) -> None:
        data = self._load_yml(kwargs["file"])

        if kwargs["reset"]:
            deleted, _ = Category.objects.all().delete()
            self.stdout.write(f"Deleted all ({deleted}) categories")

        created_categories = 0

        for category_type, nodes in data.items():
            if category_type not in ["INCOME", "EXPENSE"]:
                raise CommandError("Improper type. Must be either INCOME or EXPENSE")

            for node in nodes:
                created_categories += self._process_category_tree(node, category_type)

        self.stdout.write(f"Created {created_categories} categories")

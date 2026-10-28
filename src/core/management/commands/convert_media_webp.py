"""Наявні JPEG/PNG у полях зображень → WebP. Без --apply лише звіт."""

from django.core.management.base import BaseCommand

from src.core.media_convert import convert_stored_images, format_report


class Command(BaseCommand):
    help = (
        "Конвертує наявні JPEG і PNG у полях зображень на WebP (якість 82). "
        "Оригінали копіює в media/_originals_backup/<дата>/ зі збереженням відносного шляху "
        "і оновлює базу. Без --apply нічого не записує. Повторний запуск пропускає вже WebP. "
        "Файли макета в static не чіпає."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Записати WebP, резервні копії й нові шляхи в базі.",
        )

    def handle(self, *args, **options):
        report = convert_stored_images(apply=options["apply"])
        self.stdout.write(format_report(report))
        for problem in report.problems:
            self.stderr.write(problem)

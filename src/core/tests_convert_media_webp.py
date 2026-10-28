import tempfile
from datetime import date
from io import BytesIO, StringIO
from pathlib import Path
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.test import TestCase, override_settings
from PIL import Image

from src.catalog.models import Category
from src.content.models import HomeBlock
from src.core.images import MAX_SIDE
from src.core.management.commands.convert_media_webp import Command
from src.core.media_convert import convert_stored_images, is_static_tree, iter_image_refs


class ConvertMediaWebpTests(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.media = override_settings(MEDIA_ROOT=self.tmp.name)
        self.media.enable()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(self.media.disable)
        self.assertEqual(
            Path(default_storage.location).resolve(),
            Path(self.tmp.name).resolve(),
        )

    def test_dry_run_is_the_default_and_writes_nothing(self):
        saved = _store("categories/dry.jpg", _image_bytes("JPEG", (12, 8)))
        category = Category.objects.create(name_uk="Сухе", slug="sukhe")
        Category.objects.filter(pk=category.pk).update(image=saved)
        out, err = StringIO(), StringIO()

        call_command("convert_media_webp", stdout=out, stderr=err)

        category.refresh_from_db()
        self.assertEqual(category.image.name, saved)
        self.assertTrue((Path(self.tmp.name) / saved).is_file())
        self.assertFalse((Path(self.tmp.name) / "_originals_backup").exists())
        text = out.getvalue()
        self.assertIn("apply=0", text)
        self.assertIn("converted=1", text)
        self.assertIn("backups=0", text)
        self.assertIn("Режим: перегляд", text)
        self.assertEqual(err.getvalue(), "")

    def test_apply_backs_up_shared_file_and_second_run_is_idle(self):
        payload = _image_bytes("JPEG", (16, 10))
        saved = _store("categories/shared.jpg", payload)
        first = Category.objects.create(name_uk="Перша", slug="persha")
        second = Category.objects.create(name_uk="Друга", slug="druha")
        Category.objects.filter(pk__in=[first.pk, second.pk]).update(image=saved)
        out, err = StringIO(), StringIO()

        with patch("src.core.media_convert.timezone.localdate", return_value=date(2026, 10, 28)):
            call_command("convert_media_webp", "--apply", stdout=out, stderr=err)

        text = out.getvalue()
        self.assertIn("converted=1", text)
        self.assertIn("references=2", text)
        self.assertIn("backups=1", text)
        self.assertIn("apply=1", text)
        self.assertEqual(err.getvalue(), "")
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual(first.image.name, second.image.name)
        self.assertTrue(first.image.name.endswith(".webp"))
        self.assertFalse((Path(self.tmp.name) / saved).exists())
        backup = Path(self.tmp.name) / "_originals_backup" / "2026-10-28" / saved
        self.assertEqual(backup.read_bytes(), payload)
        with Image.open(first.image.path) as saved_image:
            self.assertEqual(saved_image.format, "WEBP")
        webp_bytes = Path(first.image.path).read_bytes()

        again, again_err = StringIO(), StringIO()
        with patch("src.core.media_convert.timezone.localdate", return_value=date(2026, 10, 29)):
            call_command("convert_media_webp", "--apply", stdout=again, stderr=again_err)
        self.assertIn("converted=0", again.getvalue())
        self.assertIn("backups=0", again.getvalue())
        self.assertEqual(backup.read_bytes(), payload)
        self.assertEqual(Path(first.image.path).read_bytes(), webp_bytes)
        self.assertFalse((Path(self.tmp.name) / "_originals_backup" / "2026-10-29").exists())

    def test_png_keeps_alpha_and_caps_the_long_side(self):
        saved = _store("categories/wide.png", _image_bytes("PNG", (3000, 10), "RGBA"))
        category = Category.objects.create(name_uk="Широке", slug="shyroke-webp")
        Category.objects.filter(pk=category.pk).update(image=saved)

        report = convert_stored_images(apply=True, today="2026-10-28")

        category.refresh_from_db()
        self.assertEqual(report.converted, 1)
        self.assertEqual(report.errors, 0)
        with Image.open(category.image.path) as saved_image:
            self.assertEqual(saved_image.format, "WEBP")
            self.assertEqual(saved_image.mode, "RGBA")
            self.assertEqual(max(saved_image.size), MAX_SIDE)
            self.assertEqual(saved_image.size[0], MAX_SIDE)

    def test_gif_webp_missing_backup_orphan_and_escape_stay(self):
        gif = _image_bytes("GIF", (4, 4))
        webp = _image_bytes("WEBP", (6, 6))
        gif_name = _store("categories/anim.gif", gif)
        webp_name = _store("categories/keep.webp", webp)
        backup_name = "_originals_backup/2026-10-28/categories/old.jpg"
        backup_payload = _image_bytes("JPEG", (5, 5))
        _store(backup_name, backup_payload)
        orphan = Path(self.tmp.name) / "loose" / "keep.png"
        orphan.parent.mkdir()
        orphan_payload = _image_bytes("PNG", (3, 3))
        orphan.write_bytes(orphan_payload)
        outside = Path(self.tmp.name).parent / "g5-outside-gestia-probe.jpg"
        outside.write_bytes(b"keep-outside")
        self.addCleanup(outside.unlink, missing_ok=True)

        gif_row = Category.objects.create(name_uk="Гіф", slug="gif-webp")
        webp_row = Category.objects.create(name_uk="Веб", slug="webp-keep")
        backup_row = Category.objects.create(name_uk="Копія", slug="backup-keep")
        missing_row = Category.objects.create(name_uk="Немає", slug="nemaie")
        unsafe_row = Category.objects.create(name_uk="Назовні", slug="nazovni")
        Category.objects.filter(pk=gif_row.pk).update(image=gif_name)
        Category.objects.filter(pk=webp_row.pk).update(image=webp_name)
        Category.objects.filter(pk=backup_row.pk).update(image=backup_name)
        Category.objects.filter(pk=missing_row.pk).update(image="categories/missing.jpg")
        Category.objects.filter(pk=unsafe_row.pk).update(image="../g5-outside-gestia-probe.jpg")

        report = convert_stored_images(apply=True, today="2026-10-28")

        self.assertEqual(report.converted, 0)
        self.assertEqual(report.errors, 0)
        self.assertGreaterEqual(report.skipped, 2)
        self.assertGreaterEqual(report.already, 1)
        self.assertGreaterEqual(report.missing, 1)
        self.assertGreaterEqual(report.unsafe, 1)
        gif_row.refresh_from_db()
        webp_row.refresh_from_db()
        backup_row.refresh_from_db()
        unsafe_row.refresh_from_db()
        self.assertEqual(gif_row.image.name, gif_name)
        self.assertEqual(Path(gif_row.image.path).read_bytes(), gif)
        self.assertEqual(Path(webp_row.image.path).read_bytes(), webp)
        self.assertEqual(backup_row.image.name, backup_name)
        self.assertEqual(Path(self.tmp.name, backup_name).read_bytes(), backup_payload)
        self.assertEqual(orphan.read_bytes(), orphan_payload)
        self.assertEqual(unsafe_row.image.name, "../g5-outside-gestia-probe.jpg")
        self.assertEqual(outside.read_bytes(), b"keep-outside")

    def test_encode_failure_leaves_the_original(self):
        payload = _image_bytes("JPEG", (8, 8))
        saved = _store("categories/broken.jpg", payload)
        category = Category.objects.create(name_uk="Збій", slug="zbii-webp")
        Category.objects.filter(pk=category.pk).update(image=saved)

        with patch("src.core.media_convert.encode_upload", side_effect=OSError("webp")):
            report = convert_stored_images(apply=True, today="2026-10-28")

        category.refresh_from_db()
        self.assertEqual(report.converted, 0)
        self.assertEqual(report.backups, 0)
        self.assertGreaterEqual(report.errors, 1)
        self.assertEqual(category.image.name, saved)
        self.assertEqual(Path(category.image.path).read_bytes(), payload)
        self.assertFalse((Path(self.tmp.name) / "_originals_backup").exists())

    def test_proxy_models_do_not_duplicate_the_same_field(self):
        block, _created = HomeBlock.objects.get_or_create(
            key=HomeBlock.Key.HERO,
            defaults={"sort": 1},
        )
        HomeBlock.objects.filter(pk=block.pk).update(image="home/proxy-probe.jpg")

        refs = [
            ref
            for ref in iter_image_refs()
            if ref.field_name == "image" and ref.name == "home/proxy-probe.jpg"
        ]

        self.assertEqual(len(refs), 1)
        self.assertIs(refs[0].model, HomeBlock)

    def test_static_tree_is_recognized_and_command_is_registered(self):
        static_file = Path(settings_base()) / "src" / "core" / "static" / "img" / "x.jpg"
        self.assertTrue(is_static_tree(static_file))
        self.assertFalse(is_static_tree(Path(self.tmp.name) / "categories" / "a.jpg"))
        self.assertIn("--apply", Command().help)
        from django.core.management import get_commands

        self.assertEqual(get_commands()["convert_media_webp"], "src.core")


def _store(name, payload):
    return default_storage.save(name, ContentFile(payload))


def _image_bytes(fmt, size, mode="RGB"):
    color = (200, 20, 20, 128) if mode == "RGBA" else (200, 20, 20)
    image = Image.new(mode, size, color)
    buffer = BytesIO()
    image.save(buffer, format=fmt)
    return buffer.getvalue()


def settings_base():
    from django.conf import settings

    return settings.BASE_DIR

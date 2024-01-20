#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import logging
import subprocess
import re
import gzip
import shutil

from yaml import load, dump
import magic

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from coodeer.configuration.coodeer import Settings
from coodeer.configuration.coodeer import LATEST_REPOSITORY_SPECIFICATION_KEY
from coodeer.controller.s3_access import S3ObjectsControl

PATTERN_PACKAGES_FILENAME = r"^Filename\: (?P<path>.*?)$"
REGEX_PACKAGES_FILENAME = re.compile(PATTERN_PACKAGES_FILENAME)


def mk_rsync_call_args(source, destination):
    args = ["rsync", "-avrH", "--delete", source, destination]

    return args


def update_repository_metadata(repo_path, root):
    log = logging.getLogger(__name__)

    scanpackages_args = [
        "dpkg-scanpackages",
        "--multiversion",
        ".",
    ]
    packages_out = subprocess.check_output(scanpackages_args, cwd=repo_path)
    packages_gz = os.path.join(repo_path, "Packages.gz")

    with gzip.open(packages_gz, "wt") as tgt:
        for line in packages_out.decode("utf-8").split("\n"):
            matcher = REGEX_PACKAGES_FILENAME.match(line)

            if matcher:
                f_path = matcher.groupdict()["path"]
                abs_path = os.path.join(repo_path, f_path)
                rel_path = os.path.relpath(abs_path, root)
                line = f"Filename: {rel_path}"
                log.debug(f"Mangled filename {f_path!r} -> {rel_path!r}")

            tgt.write(line)
            tgt.write("\n")


class RepositoryControl:
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.cfg = Settings()
        self.soc = S3ObjectsControl()

    def upload(self, path, blacklisted=None, whitelisted_content_types=None):
        items = set()

        if os.path.isfile(path):
            items.add((os.path.basename(path), os.path.abspath(path)))
        elif os.path.isdir(path):
            for item in os.listdir(path):
                try:
                    if item in blacklisted:
                        self.log.info(f"BLACKLISTED: {item}")
                        continue
                except TypeError:
                    pass

                abs_path = os.path.abspath(os.path.join(path, item))
                items.add((item, abs_path))

        for item, abs_path in items:
            try:
                mime_type = magic.from_file(abs_path, mime=True)
            except NameError:
                self.log.warning("The magic library appears to be missing?")
                mime_type = "application/octet-stream"

            try:
                if mime_type not in whitelisted_content_types:
                    self.log.info(f"IGNORED: {item}")
                    continue
            except TypeError:
                pass

            rel_path = item
            self.log.info(f"+ {abs_path} {mime_type} --> {rel_path}")

            try:
                self.soc.push(rel_path, abs_path, mime_type)
            except Exception as exc:
                self.log.error(exc)

    def get_latest_repository_specification(self, repositories_root):
        return self.soc.pull(
            LATEST_REPOSITORY_SPECIFICATION_KEY, root=repositories_root
        )

    def validate_repository_specification(self, data):
        errors = list()

        for required_key in ("repositories_mapping", "published"):
            if required_key not in data:
                errors.append(
                    f"Specification is missing required key {required_key!r}!"
                )

        if not errors:
            repositories_mapping = data["repositories_mapping"]
            published = data["published"]

            for package, keys in published.items():
                for key in sorted(keys):
                    if key not in repositories_mapping:
                        errors.append(
                            f"Package {package!r} published to undefined repository {key!r}!"
                        )

        if errors:
            for item in errors:
                self.log.error(item)

            raise ValueError("Invalid Specification!")

        return data

    def put_latest_repository_specification(self, spec_file):
        with open(spec_file, "r") as src:
            spec = load(src, Loader=Loader)

        self.validate_repository_specification(spec)

        self.soc.push(
            LATEST_REPOSITORY_SPECIFICATION_KEY, spec_file, "application/yaml"
        )

    def create_repository_specification(self, data, spec_file):
        self.validate_repository_specification(data)

        with open(spec_file, "w") as tgt:
            tgt.write(dump(data, Dumper=Dumper))

        return spec_file

    def mk_repositories(self, repositories_root, spec_file):
        with open(spec_file, "r") as src:
            spec = load(src, Loader=Loader)

        self.validate_repository_specification(spec)

        pool_root = os.path.join(repositories_root, "pool")
        repositories_mapping = spec["repositories_mapping"]

        self.log.info(
            f"Creating repositories in {repositories_root!r}, pool in {pool_root}"
        )
        self.log.debug(f" Pool: {pool_root!r}")
        os.makedirs(pool_root, exist_ok=True)

        folder_mapping = dict()
        for repo_key, path in sorted(repositories_mapping.items()):
            folder_path = os.path.join(repositories_root, path)
            self.log.info(f" {repo_key}: {folder_path!r}")
            folder_mapping[repo_key] = folder_path

            if os.path.isdir(folder_path):
                self.log.debug(f" {repo_key}: Dropping {folder_path}")
                shutil.rmtree(folder_path)

            os.makedirs(folder_path, exist_ok=True)

        for package, published_to in sorted(spec["published"].items()):
            targets = []

            for repo_key in published_to:
                target_path = os.path.join(folder_mapping[repo_key], package)
                targets.append((repo_key, target_path))

            self.log.info(f"Package {package!r}")

            try:
                pool_target = self.soc.pull(package, pool_root)
            except KeyError as kexc:
                self.log.warning(f" Missing! IGNORED.")
                continue

            self.log.debug(f" Source: {pool_target!r}")

            for repo_key, target in sorted(targets):
                self.log.info(f" {repo_key}: {target}")

                try:
                    os.link(pool_target, target)
                except FileExistsError:
                    os.unlink(target)
                    os.link(pool_target, target)

        for repo_path in folder_mapping.values():
            update_repository_metadata(repo_path, repositories_root)

        self.log.info(
            f"You could call >> {' '.join(mk_rsync_call_args(repositories_root, '$TARGET'))} << for synchronising now."
        )

        return repositories_root

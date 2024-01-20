#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

HEAD response

    * see https://docs.aws.amazon.com/AmazonS3/latest/API/RESTCommonResponseHeaders.html

"""
import os
import logging
import hashlib

import boto3
import botocore

logging.getLogger("botocore").setLevel(logging.WARNING)

from coodeer.configuration.coodeer import Settings


def md5_sum(local_fn):
    """
    Return MD5 sum of file *local_fn*.
    """
    with open(local_fn, "rb") as handle:
        md5sum = hashlib.md5(handle.read()).hexdigest()

    return md5sum


class S3ObjectsControl:
    """
    Asset's up-/downloading Controller.
    (Based on https://github.com/doubleO8/sure-shot-static/blob/master/sure_shot_static/intergalactic.py)


    Attributes:
        log (logging.Logger): logger instance
        bucket (str): Bucket name
        base_url (str): Bucket's base URL
        base_arn (str): Bucket's base ARN
    """

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.cfg = Settings()
        self.bucket = kwargs.get("bucket", self.cfg.bucket)
        self._session = boto3.session.Session()
        self.client = boto3.client("s3")

    @property
    def base_url(self):
        return "https://{bucket}.s3.{region_name}.amazonaws.com".format(
            bucket=self.bucket, region_name=self._session.region_name
        )

    @property
    def base_arn(self):
        return "arn:aws:s3:::{bucket}".format(bucket=self.bucket)

    def head(self, rel_path):
        try:
            return self.client.head_object(Bucket=self.bucket, Key=rel_path)
        except botocore.exceptions.ClientError as bex:
            if bex.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                raise KeyError(rel_path)
            elif bex.response["ResponseMetadata"]["HTTPStatusCode"] == 403:
                self.log.error(
                    "You Gotta Fight For Your Right To ... {what:8} {rel_path!r}: {Code} {Message}".format(
                        what="get head",
                        rel_path=rel_path,
                        **bex.response["Error"],
                    )
                )
            else:
                raise

        return None

    def pull(self, rel_path, root, **kwargs):
        need_pull = True
        abs_path = os.path.abspath(os.path.join(root, rel_path))

        if os.path.exists(abs_path):
            try:
                head_response = self.head(rel_path)
            except KeyError:
                raise

            if head_response:
                need_pull = False

                try:
                    md5_digest = md5_sum(abs_path)
                    key = "ETag"
                    self.log.debug(
                        "   {:20}: me={!r} -- them={!r}".format(
                            key, md5_digest, head_response.get(key)
                        )
                    )

                    if md5_digest not in head_response["ETag"]:
                        need_pull = True
                except Exception as exc:
                    self.log.warning(
                        "MD5 sum/ETag comparison failed: {!s}".format(exc)
                    )

        if need_pull:
            parent = os.path.dirname(abs_path)
            os.makedirs(parent, exist_ok=True)

            s3_resource = boto3.resource("s3")

            try:
                s3_resource.Object(self.bucket, rel_path).download_file(
                    abs_path
                )
            except botocore.exceptions.ClientError as bex:
                if bex.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                    raise KeyError(rel_path)
                else:
                    raise

        return abs_path

    def push(self, rel_path, abs_path, mime_type, **kwargs):
        """
        Upload an object to the bucket.

        Args:
            rel_path (str): relative path (target)
            abs_path (str): absolute path (local source)
            mime_type (str): MIME type

        Returns:
            bool: ``True`` if operation succeeded
        """
        need_push = True
        head_response = None

        upload_args = {
            "Key": rel_path,
            "Bucket": self.bucket,
            "ContentType": mime_type,
        }

        try:
            head_response = self.head(rel_path)
        except KeyError:
            pass

        if head_response:
            need_push = False

            try:
                md5_digest = md5_sum(abs_path)
                key = "ETag"
                self.log.debug(
                    "   {:20}: me={!r} -- them={!r}".format(
                        key, md5_digest, head_response.get(key)
                    )
                )

                if md5_digest not in head_response["ETag"]:
                    need_push = True
            except Exception as exc:
                self.log.warning(
                    "MD5 sum/ETag comparison failed: {!s}".format(exc)
                )

            if need_push is False:
                same_size = (
                    os.path.getsize(abs_path) == head_response["ContentLength"]
                )
                if not same_size:
                    self.log.debug("   Size differs ...")
                    need_push = True

        if not need_push:
            self.log.info("   No update needed ...")
            return True

        succeeded = False
        with open(abs_path, "rb") as src:
            try:
                self.client.put_object(Body=src, **upload_args)
                succeeded = True
            except botocore.exceptions.ClientError as bex:
                if bex.response["ResponseMetadata"]["HTTPStatusCode"] == 403:
                    self.log.error(
                        "You Gotta Fight For Your Right To ... {what:8} {rel_path!r}: {Code} {Message}".format(
                            what="put",
                            rel_path=rel_path,
                            **bex.response["Error"],
                        )
                    )
                else:
                    raise

        if succeeded:
            self.log.info(" = {:s}/{:s}".format(self.base_url, rel_path))

        return succeeded

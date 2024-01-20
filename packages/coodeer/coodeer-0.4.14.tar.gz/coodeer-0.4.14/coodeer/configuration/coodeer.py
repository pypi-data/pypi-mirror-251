#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseSettings


LATEST_REPOSITORY_SPECIFICATION_KEY = "00-spec/latest.yaml"


class CoodeerSettings(BaseSettings):
    bucket: str = "coodeer"

    class Config:
        env_prefix = "COODEER_"  # defaults to no prefix, i.e. ""


class AmazonWebServicesSettings(BaseSettings):
    aws_access_key_id: str
    aws_default_region: str
    aws_secret_access_key: str

    class Config:
        fields = {
            "aws_access_key_id": {
                "env": "AWS_ACCESS_KEY_ID",
            },
            "aws_default_region": {
                "env": "AWS_DEFAULT_REGION",
            },
            "aws_secret_access_key": {
                "env": "AWS_SECRET_ACCESS_KEY",
            },
        }


class Settings(CoodeerSettings, AmazonWebServicesSettings, BaseSettings):
    language: str = "C"
    lc_all: str = "C"

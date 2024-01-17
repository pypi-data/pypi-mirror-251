import os.path
import sys

from flake8.options import config
from flake8.utils import parse_comma_separated_list


class ProfileError(Exception):
    """Error loading a profile."""


class ProfilePlugin:

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            "--profile",
            help="Enable a flake8 profile",
            comma_separated_list=False,
            parse_from_config=True,
        )

    @classmethod
    def parse_options(cls, parser, options, args):
        profile = options.profile
        if not profile:
            return
        profile_dir = os.environ.get("FLAKE8_PROFILE_DIR")
        if not profile_dir:
            raise ProfileError("No FLAKE8_PROFILE_DIR set")
        profile_file = os.path.join(profile_dir, "{}.conf".format(profile))
        conf, cfg_dir = config.load_config(profile_file, [])
        if not cfg_dir:
            raise ProfileError(
                "Profile file {} not found".format(profile_file)
            )
        print(
            "Loaded profile from",
            os.path.join(cfg_dir, f"{profile}.conf"),
            file=sys.stderr,
        )
        profile_options = dict(conf.items("flake8"))
        for k, v in profile_options.items():
            try:
                old_v = getattr(options, k)
            except AttributeError:
                setattr(options, k, v)
            else:
                # Don't overwrite local config options which aren't lists
                if old_v is None:
                    setattr(options, k, v)
                elif not isinstance(old_v, str):
                    if isinstance(v, str):
                        new_v = list(old_v) + parse_comma_separated_list(v)
                    else:
                        new_v = list(old_v) + v
                    setattr(options, k, new_v)

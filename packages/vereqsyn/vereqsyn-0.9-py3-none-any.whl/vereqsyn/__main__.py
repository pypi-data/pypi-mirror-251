import argparse

import vereqsyn


def main(argv=None):
    parser = argparse.ArgumentParser(
        "vereqsyn",
        "%(prog)s <versions.cfg> <requirements.txt>",
        "Bi-directional versions.cfg <-> requirements.txt synchronization",
    )
    parser.add_argument("versions_cfg", action="store", help="path to versions.cfg")
    parser.add_argument("requirements_txt", action="store", help="path to requirements.txt")

    args = parser.parse_args(argv)
    command = vereqsyn.VersionsCfgRequirementsTxtSync(args.requirements_txt, args.versions_cfg)
    command.update()


if __name__ == "__main__":  # pragma: no cover
    main()

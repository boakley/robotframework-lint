import sys
from .rflint import RfLint


def main(args=None):
    try:
        app = RfLint()
        result = app.run(args)
        return result

    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        return 1

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("--help")
    sys.exit(main(sys.argv[1:]))

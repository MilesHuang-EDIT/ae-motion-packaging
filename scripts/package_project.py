#!/usr/bin/env python3
"""Package only an explicit file manifest; verify ZIP CRC and member hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile


def file_digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    temporary = None
    try:
        root = args.root.resolve(strict=True)
        output = args.output.resolve()
        files = json.loads(args.manifest.read_text(encoding='utf-8'))['files']
        if not isinstance(files, list) or not files or len(set(files)) != len(files):
            raise ValueError('Manifest requires a nonempty list of unique relative file paths')
        entries = []
        member_names = set()
        for relative in files:
            rel = Path(relative)
            source = (root / rel).resolve()
            if rel.is_absolute() or '..' in rel.parts or not source.is_relative_to(root) or not source.is_file():
                raise ValueError('Missing file or path outside root: ' + str(relative))
            if rel.as_posix() in member_names:
                raise ValueError('Duplicate normalized archive path: ' + str(relative))
            member_names.add(rel.as_posix())
            if source == output:
                raise ValueError('Output ZIP cannot be an input member')
            entries.append((rel.as_posix(), source, file_digest(source)))
        if output.exists():
            raise ValueError('Output already exists; choose a new versioned ZIP path')
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix='.zip', delete=False) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for relative, source, expected in entries:
                z.write(source, relative)
        with zipfile.ZipFile(temporary) as z:
            if z.testzip() is not None:
                raise ValueError('ZIP CRC verification failed')
            for relative, source, expected in entries:
                h = hashlib.sha256()
                with z.open(relative) as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        h.update(chunk)
                if h.hexdigest() != expected or file_digest(source) != expected:
                    raise ValueError('Member hash mismatch or input changed: ' + relative)
        temporary.rename(output)
        temporary = None
        report = {'passed': True, 'output': str(output), 'files': len(entries),
                  'bytes': output.stat().st_size, 'sha256': file_digest(output),
                  'crc_verified': True, 'member_hashes_verified': True,
                  'native_ae_portability_verified': False}
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        report = {'passed': False, 'errors': [str(exc)]}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())

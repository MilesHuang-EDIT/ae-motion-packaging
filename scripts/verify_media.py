#!/usr/bin/env python3
"""Validate actual rendered files against an explicit delivery contract."""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def executable(value, default):
    result = value or shutil.which(default)
    if not result or not Path(result).is_file():
        raise ValueError('Provide --' + default + ' with an installed executable path')
    return str(Path(result).resolve())


def validate(spec, root, probe, ffmpeg, decode):
    result = {'file': spec.get('file'), 'errors': []}
    errors = result['errors']
    try:
        path = (root / spec['file']).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('File missing or outside delivery root')
        for key in ('width', 'height', 'frames'):
            if not isinstance(spec[key], int) or isinstance(spec[key], bool) or spec[key] <= 0:
                raise ValueError(key + ' must be a positive integer')
        expected_fps = Fraction(str(spec['fps']))
        if expected_fps <= 0:
            raise ValueError('fps must be positive')
        audio = spec.get('audio', 'any')
        if audio not in ('none', 'required', 'any'):
            raise ValueError('audio must be none, required or any')
        # Sibling shared libraries are needed by some portable FFmpeg bundles.
        env = dict(os.environ)
        lib = str(Path(probe).parent)
        env['DYLD_LIBRARY_PATH'] = lib + (':' + env['DYLD_LIBRARY_PATH'] if env.get('DYLD_LIBRARY_PATH') else '')
        data = json.loads(subprocess.check_output(
            [probe, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
            env=env, stderr=subprocess.PIPE, text=True))
        videos = [s for s in data['streams'] if s['codec_type'] == 'video']
        if len(videos) != 1:
            raise ValueError('Expected exactly one video stream')
        v = videos[0]
        fps = Fraction(v.get('avg_frame_rate', '0/1'))
        if fps != expected_fps:
            errors.append('fps: expected %s, got %s' % (expected_fps, fps))
        for key in ('width', 'height'):
            if v[key] != spec[key]:
                errors.append('%s: expected %s, got %s' % (key, spec[key], v[key]))
        frame_count = v.get('nb_frames')
        if frame_count in (None, 'N/A'):
            count = json.loads(subprocess.check_output(
                [probe, '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                 '-show_entries', 'stream=nb_read_frames', '-of', 'json', str(path)],
                env=env, stderr=subprocess.PIPE, text=True))
            frame_count = count['streams'][0]['nb_read_frames']
        frame_count = int(frame_count)
        if frame_count != spec['frames']:
            errors.append('frames: expected %s, got %s' % (spec['frames'], frame_count))
        duration = float(v.get('duration') or data['format']['duration'])
        expected_duration = float(Fraction(spec['frames']) / expected_fps)
        if abs(duration - expected_duration) > .002:
            errors.append('duration: expected %.6f, got %.6f' % (expected_duration, duration))
        audio_count = sum(s['codec_type'] == 'audio' for s in data['streams'])
        if audio == 'none' and audio_count:
            errors.append('Unexpected audio stream')
        if audio == 'required' and not audio_count:
            errors.append('Required audio stream missing')
        result.update(width=v['width'], height=v['height'], fps=str(fps), frames=frame_count,
                      duration=duration, audio_streams=audio_count, codec=v.get('codec_name'),
                      pixel_format=v.get('pix_fmt'), sha256=digest(path))
        if decode:
            run = subprocess.run([ffmpeg, '-v', 'error', '-nostdin', '-threads', '2',
                                  '-i', str(path), '-map', '0:v:0', '-progress', 'pipe:1',
                                  '-c:v', 'rawvideo', '-f', 'null', '-'],
                                 env=env, capture_output=True, text=True)
            decoded = [int(line.split('=', 1)[1]) for line in run.stdout.splitlines()
                       if line.startswith('frame=')]
            result['decoded_frames'] = decoded[-1] if decoded else 0
            if run.returncode or run.stderr.strip() or result['decoded_frames'] != spec['frames']:
                errors.append('Decode failed: ' + run.stderr.strip()[:1200])
    except (KeyError, ValueError, OSError, subprocess.SubprocessError, ZeroDivisionError) as exc:
        errors.append(str(exc))
    result['passed'] = not errors
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--ffprobe')
    parser.add_argument('--ffmpeg')
    parser.add_argument('--decode', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        specs = json.loads(args.contract.read_text(encoding='utf-8'))['segments']
        if not isinstance(specs, list) or not specs:
            raise ValueError('Contract requires a nonempty segments list')
        probe = executable(args.ffprobe, 'ffprobe')
        ffmpeg = executable(args.ffmpeg, 'ffmpeg') if args.decode else None
        outputs = [validate(spec, root, probe, ffmpeg, args.decode) for spec in specs]
        report = {'passed': all(o['passed'] for o in outputs), 'outputs': outputs}
    except (ValueError, OSError, KeyError, TypeError) as exc:
        report = {'passed': False, 'errors': [str(exc)]}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())

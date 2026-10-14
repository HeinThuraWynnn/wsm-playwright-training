#!/usr/bin/env python3
"""AGD 2.1 foundation: local validation, evidence, lifecycle, and safe adoption."""
import argparse
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

VERSION = '2.1'
ADAPTERS = {'wordpress': [], 'woocommerce': ['wordpress']}
RISKS = {'low', 'standard', 'high'}
CATEGORIES = {'unit', 'integration', 'e2e', 'static', 'lint', 'build', 'security', 'compatibility', 'scope', 'documentation'}
STATUSES = {'PASS', 'FAIL', 'BLOCKED', 'NOT RUN', 'NOT APPLICABLE'}
PROTECTED = {'production-deploy', 'production-database', 'destructive-migration', 'out-of-scope-deletion', 'overwrite-user-changes', 'real-payment', 'live-customer-data', 'secret-transmission', 'major-architecture', 'external-side-effect'}
STATES = ['DISCOVER', 'SPECIFY', 'PLAN', 'RED', 'GREEN', 'REFACTOR', 'VERIFY', 'REVIEW', 'HANDOFF']
SKILL_SECTIONS = ['Purpose', 'Activation', 'Inputs', 'Procedure', 'Constraints', 'Outputs', 'Completion', 'Failure handling']

class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def relative(root, value):
    require(isinstance(value, str) and value and not Path(value).is_absolute(), 'Expected a relative path')
    path = (root / value).resolve()
    require(path.is_relative_to(root.resolve()), 'Reference escapes project root: ' + value)
    return path


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', value), 'Invalid identifier')


def select_adapters(adapters):
    require(isinstance(adapters, list) and all(isinstance(a, str) for a in adapters), 'adapters must be a string list')
    require(len(set(adapters)) == len(adapters), 'Duplicate adapters')
    for adapter in adapters:
        require(adapter in ADAPTERS, 'Unknown adapter: ' + adapter)
        require(all(dep in adapters for dep in ADAPTERS[adapter]), adapter + ' requires WordPress')


def validate_config(config, root):
    require(isinstance(config, dict), 'Configuration must be an object')
    fields = {'version', 'project', 'adapters', 'skills', 'references', 'commands', 'risk', 'evidence_dir'}
    require(set(config) == fields, 'Missing or unsupported configuration fields')
    require(config['version'] == VERSION, 'Unsupported framework version')
    identifier(config['project'])
    select_adapters(config['adapters'])
    require(isinstance(config['risk'], str) and config['risk'] in RISKS, 'Unsupported risk')
    relative(root, config['evidence_dir'])
    for key in ('skills', 'references'):
        require(isinstance(config[key], list), key + ' must be a list')
        for ref in config[key]:
            path = relative(root, ref)
            require(path.is_file(), 'Missing reference: ' + str(ref))
            if key == 'skills':
                validate_skill(path)
    for adapter in config['adapters']:
        path = relative(root, '.agd/adapters/' + adapter + '/adapter.json')
        require(path.is_file(), 'Missing adapter manifest: ' + adapter)
        manifest = json.loads(path.read_text())
        require(manifest == {'name': adapter, 'version': VERSION, 'requires': ADAPTERS[adapter]}, 'Incompatible adapter manifest')
    require(isinstance(config['commands'], list), 'commands must be a list')
    ids = set()
    for command in config['commands']:
        require(isinstance(command, dict), 'Command must be an object')
        required = {'id', 'category', 'argv', 'timeout', 'operation'}
        require(required <= set(command) <= required | {'risks'}, 'Missing or unsupported command fields')
        identifier(command['id'])
        require(command['id'] not in ids, 'Duplicate command ID')
        ids.add(command['id'])
        require(isinstance(command['category'], str) and command['category'] in CATEGORIES, 'Unknown gate category')
        require(isinstance(command['operation'], str) and command['operation'] in PROTECTED | {'local-check'}, 'Unknown operation')
        argv = command['argv']
        require(isinstance(argv, list) and argv and all(isinstance(a, str) and a and '\x00' not in a for a in argv), 'argv must contain nonempty strings')
        require(type(command['timeout']) in (int, float) and 0 < command['timeout'] <= 3600, 'Invalid timeout')
        risks = command.get('risks', sorted(RISKS))
        require(isinstance(risks, list) and risks and all(isinstance(r, str) and r in RISKS for r in risks), 'Invalid command risks')
    return config


def validate_skill(path):
    text = path.read_text()
    require(path.name == 'SKILL.md', 'Skill entry point must be SKILL.md')
    require(text.startswith('---\n'), 'Missing skill frontmatter')
    parts = text.split('---', 2)
    require(len(parts) == 3, 'Unclosed skill frontmatter')
    name = re.search(r'^name: ([a-z0-9-]+)$', parts[1], re.M)
    description = re.search(r'^description: (.+)$', parts[1], re.M)
    require(name is not None and name.group(1) == path.parent.name and len(name.group(1)) < 64, 'Invalid skill name')
    require(description is not None and description.group(1).strip(), 'Missing skill description')
    for section in SKILL_SECTIONS:
        require('## ' + section + '\n' in parts[2], 'Missing skill section: ' + section)


def new_task(task_id, acceptance):
    identifier(task_id)
    require(isinstance(acceptance, list) and acceptance and all(isinstance(a, str) and a.strip() for a in acceptance), 'Acceptance criteria required')
    return {'task_id': task_id, 'state': 'DISCOVER', 'acceptance': [{'criterion': a, 'met': False} for a in acceptance], 'evidence': [], 'review': '', 'history': []}


def transition(task, target, reason=''):
    require(isinstance(task, dict) and task.get('state') in STATES + ['BLOCKED'], 'Invalid task state')
    result = copy.deepcopy(task)
    current = task['state']
    require(current != 'HANDOFF', 'Task is already handed off')
    if target == 'BLOCKED':
        require(current != 'BLOCKED' and bool(reason.strip()), 'Blocking reason required')
        result['resume_state'] = current
    elif current == 'BLOCKED':
        require(target == task.get('resume_state'), 'Resume only at the interrupted state')
        result.pop('resume_state', None)
    elif current == 'PLAN' and target == 'VERIFY':
        require(bool(reason.strip()), 'TDD exception requires a recorded rationale')
    else:
        require(target in STATES and STATES.index(target) == STATES.index(current) + 1, 'Invalid lifecycle transition')
    if target == 'HANDOFF':
        require(bool(task.get('acceptance')) and all(a.get('met') is True for a in task['acceptance']), 'Acceptance criteria remain unmet')
        require(bool(task.get('evidence')) and bool(task.get('review', '').strip()), 'Evidence and review required')
    result['state'] = target
    result.setdefault('history', []).append({'from': current, 'to': target, 'reason': reason})
    return result


def verify(config, root, task_id, trusted=False, approved=()):
    identifier(task_id)
    require(all(a in PROTECTED for a in approved), 'Unknown approval operation')
    report = {'version': VERSION, 'task_id': task_id, 'scope': config['project'], 'created_at': datetime.now(timezone.utc).isoformat(), 'risk': config['risk'], 'acceptance': [], 'changed_files': [], 'approvals': list(approved), 'risks': [], 'follow_up': [], 'checks': []}
    for command in config['commands']:
        check = {'id': command['id'], 'category': command['category'], 'argv': command['argv'], 'status': 'BLOCKED', 'returncode': None, 'detail': ''}
        if config['risk'] not in command.get('risks', RISKS):
            check.update(status='NOT APPLICABLE', detail='Outside selected risk; confirm relevance during review')
        elif not trusted:
            check['detail'] = 'Command execution requires explicit configuration trust'
        elif command['operation'] in PROTECTED and command['operation'] not in approved:
            check['detail'] = 'Explicit operation approval required: ' + command['operation']
        else:
            try:
                completed = subprocess.run(command['argv'], cwd=root, capture_output=True, text=True, errors='replace', timeout=command['timeout'], shell=False)
                check.update(status='PASS' if completed.returncode == 0 else 'FAIL', returncode=completed.returncode, detail=(completed.stdout + completed.stderr)[-16000:])
            except FileNotFoundError:
                check['detail'] = 'Executable unavailable: ' + command['argv'][0]
            except subprocess.TimeoutExpired:
                check['detail'] = 'Command exceeded timeout; check descendants before retrying'
            except OSError as error:
                check['detail'] = str(error)
        report['checks'].append(check)
    if not report['checks']:
        report['checks'].append({'id': 'tooling', 'category': 'compatibility', 'argv': [], 'status': 'NOT RUN', 'returncode': None, 'detail': 'No project verification commands configured'})
    validate_evidence(report)
    return report


def validate_evidence(report):
    require(isinstance(report, dict), 'Evidence must be an object')
    fields = {'version', 'task_id', 'scope', 'created_at', 'risk', 'acceptance', 'changed_files', 'approvals', 'risks', 'follow_up', 'checks'}
    require(set(report) == fields, 'Missing or unsupported evidence fields')
    require(report['version'] == VERSION, 'Unsupported evidence version')
    identifier(report['task_id'])
    require(isinstance(report['scope'], str) and report['scope'].strip(), 'Evidence scope required')
    require(report['risk'] in RISKS, 'Invalid evidence risk')
    require(isinstance(report['created_at'], str), 'Timestamp required')
    try:
        datetime.fromisoformat(report['created_at'])
    except ValueError as error:
        raise Invalid('Invalid evidence timestamp') from error
    for key in ('acceptance', 'changed_files', 'approvals', 'risks', 'follow_up'):
        require(isinstance(report[key], list) and all(isinstance(v, str) for v in report[key]), key + ' must be a string list')
    require(all(a in PROTECTED for a in report['approvals']), 'Unknown evidence approval')
    require(isinstance(report['checks'], list) and report['checks'], 'Check evidence required')
    ids = set()
    for check in report['checks']:
        require(isinstance(check, dict) and set(check) == {'id', 'category', 'argv', 'status', 'returncode', 'detail'}, 'Invalid check evidence fields')
        identifier(check['id'])
        require(check['id'] not in ids, 'Duplicate evidence check')
        ids.add(check['id'])
        require(check['category'] in CATEGORIES and check['status'] in STATUSES, 'Invalid check category or status')
        require(isinstance(check['argv'], list) and all(isinstance(a, str) for a in check['argv']), 'Invalid evidence argv')
        require(isinstance(check['detail'], str), 'Check detail required')
        code = check['returncode']
        if check['status'] == 'PASS':
            require(type(code) is int and code == 0 and bool(check['argv']), 'PASS requires executed command with exit zero')
        elif check['status'] == 'FAIL':
            require(type(code) is int and code != 0 and bool(check['argv']), 'FAIL requires nonzero exit')
        else:
            require(code is None and bool(check['detail']), 'Nonexecuted check requires reason and null exit code')
    return report


def success(report):
    return any(c['status'] == 'PASS' for c in report['checks']) and all(c['status'] in {'PASS', 'NOT APPLICABLE'} for c in report['checks'])


def adopt(source, target, adapters):
    """Copy a compact instruction bundle; preflight all destinations, never overwrite."""
    source, target = source.resolve(), target.resolve()
    select_adapters(adapters)
    require(target.is_dir(), 'Target must be an existing directory')
    cfg = json.loads((source / '.agd/framework.json').read_text())
    cfg.update(project='adopted-project', adapters=adapters, commands=[])
    validate_config(cfg, source)
    files = {'AGENTS.md': (source / 'AGENTS.md').read_bytes()}
    for directory in ('.agd/policies', '.agd/workflows', '.agd/templates', 'skills'):
        for path in (source / directory).rglob('*'):
            if path.is_file():
                files[path.relative_to(source).as_posix()] = path.read_bytes()
    for adapter in adapters:
        for path in (source / '.agd/adapters' / adapter).rglob('*'):
            if path.is_file():
                files[path.relative_to(source).as_posix()] = path.read_bytes()
    files['.agd/framework.json'] = (json.dumps(cfg, indent=2) + '\n').encode()
    for name in files:
        destination = relative(target, name)
        require(not destination.exists() and not (target / name).is_symlink(), 'Existing file requires manual merge: ' + name)
        require(not any(p.is_symlink() for p in (target / name).parents if p != target.parent), 'Symlinked adoption path')
    for name, content in files.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as output:
            output.write(content)
    return sorted(files)


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as output:
        json.dump(value, output, indent=2)
        output.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('validate')
    ev = sub.add_parser('evidence'); ev.add_argument('file', type=Path)
    run = sub.add_parser('verify'); run.add_argument('--task', required=True); run.add_argument('--trust-config', action='store_true'); run.add_argument('--approve', action='append', default=[])
    install = sub.add_parser('adopt'); install.add_argument('target', type=Path); install.add_argument('--adapter', action='append', default=[])
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.action == 'evidence':
            validate_evidence(json.loads(args.file.read_text()))
            print('PASS: evidence structure (not provenance)')
        elif args.action == 'adopt':
            files = adopt(root, args.target.resolve(), args.adapter)
            print(json.dumps({'status': 'PASS', 'created': files}, indent=2))
        else:
            config = validate_config(json.loads((root / '.agd/framework.json').read_text()), root)
            if args.action == 'validate':
                print('PASS: configuration, references, skills, adapter dependencies')
            else:
                path = relative(root, config['evidence_dir']) / (args.task + '.json')
                identifier(args.task)
                require(not path.exists(), 'Evidence already exists; choose a new task ID')
                report = verify(config, root, args.task, args.trust_config, args.approve)
                write_new(path, report)
                print(json.dumps(report, indent=2))
                return 0 if success(report) else 1
    except (Invalid, OSError, ValueError, TypeError, KeyError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())

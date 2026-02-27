"""Generate normalization report from log for RC_v12"""
import json
from pathlib import Path
from datetime import datetime

RC_ROOT = Path(r'c:\Users\selah\emprego\certi\bim\onto-tools\outputs\logs\RC_v12_CANON\20260203_221711')
RUN3_DIR = RC_ROOT / '20_runs/run3_normalize_canonicalize'
PROOFS_DIR = RC_ROOT / '10_proofs'

# Read normalization log
log_path = RUN3_DIR / 'normalize_log_run3.json'
with open(log_path, 'r', encoding='utf-8') as f:
    norm_log = json.load(f)

# Generate markdown report from log
report_lines = []
report_lines.append('# Normalization Report (Generated from Log)')
report_lines.append('')
report_lines.append('## Summary')
report_lines.append('')
report_lines.append('| Property | Value |')
report_lines.append('|----------|-------|')
report_lines.append(f'| **Input File** | `{norm_log["input_file"]}` |')
report_lines.append(f'| **Input Hash** | `{norm_log["input_hash"][:32]}...` |')
report_lines.append(f'| **Input Triples** | {norm_log["input_triples"]} |')
report_lines.append(f'| **Timestamp** | {norm_log["timestamp"]} |')
report_lines.append(f'| **Mode** | {norm_log["mode"]} |')
report_lines.append(f'| **Auto-fix Applied** | {norm_log["auto_fix_applied"]} |')
report_lines.append(f'| **Total Warnings** | {norm_log["warnings_count"]} |')
report_lines.append('')

# Fix stats breakdown
fix_stats = norm_log.get('fix_stats') or {}
if fix_stats:
    report_lines.append('## Fix Statistics')
    report_lines.append('')
    
    # Pending corrections
    pending_preflabel = fix_stats.get('pending_preflabel_corrections', {})
    pending_def = fix_stats.get('pending_definition_corrections', {})
    
    report_lines.append(f'- **Pending prefLabel corrections**: {len(pending_preflabel)} entities')
    report_lines.append(f'- **Pending definition corrections**: {len(pending_def)} entities')
    report_lines.append(f'- **Total pending prefLabel fixes**: {fix_stats.get("total_pending_preflabel_fixes", 0)}')
    report_lines.append(f'- **Total pending definition fixes**: {fix_stats.get("total_pending_definition_fixes", 0)}')
    report_lines.append('')

report_lines.append('## Evidence Links')
report_lines.append('')
report_lines.append('- Normalization log: `20_runs/run3_normalize_canonicalize/normalize_log_run3.json`')
report_lines.append('- Run manifest: `20_runs/run3_normalize_canonicalize/run_manifest_run3.json`')
report_lines.append('- Canonical output: `20_runs/run3_normalize_canonicalize/canonical_output_run3.ttl`')
report_lines.append('')
report_lines.append('---')
report_lines.append(f'*Report generated: {datetime.now().isoformat()}*')

# Save report
report_path = PROOFS_DIR / 'NORMALIZATION_REPORT_FROM_LOG.md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print('Report generated:', report_path)
print('Total lines:', len(report_lines))

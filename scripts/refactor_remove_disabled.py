"""
Script de refatoração: remove métodos de features desabilitadas.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).parent.parent

def remove_methods(filepath: Path, methods_to_remove: set[str]) -> int:
    """Remove métodos específicos de uma classe Python, preservando formatação."""
    src = filepath.read_text(encoding="utf-8")
    tree = ast.parse(src)
    lines = src.splitlines(keepends=True)
    
    # Coletar ranges de linhas a remover (1-based)
    remove_ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in methods_to_remove:
                # Inclui decoradores
                start = node.lineno
                if node.decorator_list:
                    start = node.decorator_list[0].lineno
                end = node.end_lineno
                remove_ranges.append((start, end))
    
    if not remove_ranges:
        print(f"  Nenhum método encontrado em {filepath.name}")
        return 0
    
    # Ordenar por posição (de baixo para cima para não invalidar índices)
    remove_ranges.sort(reverse=True)
    
    result_lines = list(lines)
    for start, end in remove_ranges:
        # Remove blank line before method if present
        before = start - 2  # 0-based index of line before method
        if before >= 0 and result_lines[before].strip() == "":
            del result_lines[before:end]  # inclui blank line antes
        else:
            del result_lines[start-1:end]  # só o método
    
    new_src = "".join(result_lines)
    filepath.write_text(new_src, encoding="utf-8")
    print(f"  Removidos {len(remove_ranges)} métodos de {filepath.name}")
    return len(remove_ranges)


def remove_test_classes(filepath: Path, classes_to_remove: set[str]) -> int:
    """Remove classes de teste específicas."""
    src = filepath.read_text(encoding="utf-8")
    tree = ast.parse(src)
    lines = src.splitlines(keepends=True)
    
    remove_ranges = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name in classes_to_remove:
            start = node.lineno
            end = node.end_lineno
            remove_ranges.append((start, end))
    
    if not remove_ranges:
        print(f"  Nenhuma classe encontrada em {filepath.name}")
        return 0
    
    remove_ranges.sort(reverse=True)
    result_lines = list(lines)
    for start, end in remove_ranges:
        before = start - 2
        if before >= 0 and result_lines[before].strip() == "":
            del result_lines[before:end]
        else:
            del result_lines[start-1:end]
    
    new_src = "".join(result_lines)
    filepath.write_text(new_src, encoding="utf-8")
    print(f"  Removidas {len(remove_ranges)} classes de {filepath.name}")
    return len(remove_ranges)


def remove_imports_from_file(filepath: Path, names_to_remove: set[str]) -> int:
    """Remove nomes específicos de imports (from x import y, z)."""
    src = filepath.read_text(encoding="utf-8")
    lines = src.splitlines(keepends=True)
    new_lines = []
    removed = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Detectar import multi-linha com parênteses
        if stripped.startswith("from ") and "import" in stripped and "(" in stripped:
            block = line
            j = i + 1
            while j < len(lines) and ")" not in lines[j-1]:
                block += lines[j]
                j += 1
            if j < len(lines):
                block += lines[j-1]
            # Parse os nomes do import
            # Reconstruir removendo os names_to_remove
            import_names = []
            in_parens = False
            for il in lines[i:j]:
                content = il.strip().rstrip(",").rstrip()
                if "(" in content:
                    in_parens = True
                    content = content.split("(", 1)[1].rstrip(",").rstrip()
                if ")" in content:
                    content = content.split(")")[0].rstrip(",").rstrip()
                    in_parens = False
                for name in content.split(","):
                    n = name.strip()
                    if n and n not in names_to_remove:
                        import_names.append(n)
                    elif n in names_to_remove:
                        removed += 1
            
            if import_names:
                # Reconstruir import
                from_part = lines[i].split("(")[0].rstrip()
                if len(import_names) == 1:
                    new_lines.append(f"{from_part}{import_names[0]},\n")
                else:
                    new_lines.append(f"{from_part}(\n")
                    for name in import_names:
                        new_lines.append(f"    {name},\n")
                    new_lines.append(")\n")
            # else: skip the whole import block
            i = j
        else:
            new_lines.append(line)
        i += 1
    
    new_src = "".join(new_lines)
    filepath.write_text(new_src, encoding="utf-8")
    print(f"  Removidos {removed} imports de {filepath.name}")
    return removed


print("=== Refatoração: Remoção de features desabilitadas ===\n")

# 1. facade.py
print("1. facade.py")
facade_path = ROOT / "src/onto_tools/application/facade.py"
facade_disabled = {
    "reorder_ontology",
    "query_ontology",
    "edit_ontology",
    "apply_changes",
    "normalize_and_canonicalize",
    "validate_naming_syntax",
    "execute_sparql",
    "list_sparql_categories",
    "process_sparql_params",
    "execute_sparql_from_file",
    "execute_all_extraction_queries",
    "list_sparql_queries",
    "get_sparql_query_info",
    "_get_or_create_sparql_query_service",
    "_detect_project_root",
    "export_ontology",
    "export_json_structural",
    "export_json_hierarchical",
    "export_json_from_sparql",
    "export_xlsx_catalog",
    "export_xlsx_comments",
    "export_xlsx_comments_from_sparql",
    "export_xlsx_bsdd",
    "ingest_external_source",
    "validate_source",
    "load_source",
    "compare_artifacts",
    "compare_external_ttl",
    "compare_ttl_versions",
}
remove_methods(facade_path, facade_disabled)

# 2. test_facade.py
print("\n2. test_facade.py")
test_facade_path = ROOT / "tests/1-uc-ontology/unit/test_facade.py"
test_facade_disabled = {
    "TestReorderOntology",
    "TestQueryOntology",
    "TestEditOntology",
    "TestApplyChanges",
    "TestExecuteSparql",
    "TestExportOperations",
    "TestComparisonOperations",
}
remove_test_classes(test_facade_path, test_facade_disabled)

# 3. commands.py — remover comandos de features desabilitadas
print("\n3. commands.py")
commands_path = ROOT / "src/onto_tools/adapters/cli/commands.py"
commands_disabled = {
    "ontology_reorder",
    "ontology_query",
    "ontology_edit", 
    "ontology_apply",
    "query_execute",
    "query_list_categories",
    "query_process_params",
    "export_ontology",
    "export_json_structural",
    "export_json_hierarchical",
    "export_json_from_sparql",
    "export_xlsx_catalog",
    "export_xlsx_comments",
    "export_xlsx_bsdd",
    "data_input_ingest",
    "data_input_validate",
    "data_input_load",
    "comparison_compare",
    "comparison_compare_external",
    "comparison_compare_versions",
}
remove_methods(commands_path, commands_disabled)

# 4. test_cli_commands.py  
print("\n4. test_cli_commands.py")
test_cli_path = ROOT / "tests/1-uc-ontology/cli/test_cli_commands.py"
test_cli_disabled = {
    "TestOntologyReorder",
    "TestOntologyQuery",
    "TestOntologyEdit",
    "TestOntologyApply",
    "TestQueryCommands",
    "TestExportCommands",
    "TestComparisonCommands",
}
remove_test_classes(test_cli_path, test_cli_disabled)

print("\n=== Concluído ===")
print("Execute: pytest tests/ para validar")

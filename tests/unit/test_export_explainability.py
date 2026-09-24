from pathlib import Path
from types import SimpleNamespace

from pert_analyzer.reporting.export.explainability import interpretation_lines
from pert_analyzer.reporting.export.excel import export_excel
from pert_analyzer.reporting.export.pdf import export_pdf


class _Section:
    title = "Summary"
    is_available = True
    rows = []


class _Report:
    metadata = SimpleNamespace(
        project_name="Demo Project",
        source_image="diagram.png",
        created_at="2026-09-24T00:00:00Z",
        analysis_type="CPM",
        row_count=0,
    )
    summary = SimpleNamespace(project_duration=54, critical_path_count=2)
    cpm = SimpleNamespace(is_valid=True)
    validation = SimpleNamespace(status="VALID")
    review = SimpleNamespace(
        graph_validation_status="VALID",
        available=True,
        decisions=[{"action": "ACCEPT"}],
    )

    def sections(self):
        return [_Section()]

    def section_names(self):
        return ["summary"]


def test_interpretation_lines_preserve_authority_and_source() -> None:
    lines = interpretation_lines(_Report())
    assert any("diagram.png" in line for line in lines)
    assert any("backend CPM result" in line for line in lines)


def test_excel_contains_interpretation_sheet(tmp_path: Path) -> None:
    result = export_excel(_Report(), str(tmp_path / "report.xlsx"))
    assert result.ok
    assert "Interpretation" in result.metadata["sheets"]
    assert (tmp_path / "report.xlsx").exists()


def test_pdf_export_contains_interpretation_section(tmp_path: Path) -> None:
    result = export_pdf(_Report(), str(tmp_path / "report.pdf"))
    assert result.ok
    assert (tmp_path / "report.pdf").exists()
    assert "summary" in result.metadata["sections"]


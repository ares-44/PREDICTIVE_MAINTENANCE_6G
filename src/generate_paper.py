
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "reports" / "research_paper.md"
OUTPUT = ROOT / "reports" / "research_paper.pdf"


def clean_inline(text):
    """Convert common Markdown and LaTeX remnants into clean PDF text."""
    text = text.strip()

    # Remove accidental escaping before Markdown symbols.
    text = re.sub(r"\\([#*_`%&-])", r"\1", text)

    # Convert common LaTeX notation to readable text.
    text = text.replace(r"\Delta", "Delta ")
    text = text.replace(r"\mu", "mu")
    text = text.replace(r"\sigma", "sigma")
    text = text.replace(r"\frac", "frac")
    text = re.sub(r"\\text\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\mathrm\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[()\[\]]", "", text)
    text = text.replace("$", "")
    text = text.replace(r"\_", "_")
    text = text.replace(r"\%", "%")

    # Escape XML-sensitive characters before adding ReportLab markup.
    text = escape(text)

    # Format Markdown bold, italics, and inline code.
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(
        r"`([^`]+)`",
        r"<font name='Courier'>\1</font>",
        text,
    )

    return text


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(
        A4[0] / 2,
        0.45 * inch,
        f"Page {doc.page}",
    )
    canvas.restoreState()


def build_pdf():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Research paper not found: {SOURCE}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    markdown = SOURCE.read_text(encoding="utf-8")

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="PaperTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#183153"),
        spaceAfter=18,
    ))

    styles.add(ParagraphStyle(
        name="PaperSubtitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#53657d"),
        spaceAfter=14,
    ))

    styles.add(ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontSize=14,
        leading=19,
        textColor=colors.HexColor("#183153"),
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#28527a"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="PaperBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name="PaperBullet",
        parent=styles["PaperBody"],
        leftIndent=18,
        firstLineIndent=-10,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="TableText",
        parent=styles["BodyText"],
        fontSize=8,
        leading=10,
        spaceAfter=0,
    ))

    story = []
    lines = markdown.splitlines()
    in_table = False
    table_rows = []
    first_title = True

    def flush_table():
        nonlocal table_rows

        if not table_rows:
            return

        data = []

        for row in table_rows:
            cells = [
                cell.strip()
                for cell in row.strip().strip("|").split("|")
            ]

            # Ignore Markdown table separator rows.
            if all(
                re.fullmatch(r":?-{3,}:?", cell)
                for cell in cells
            ):
                continue

            data.append([
                Paragraph(clean_inline(cell), styles["TableText"])
                for cell in cells
            ])

        if data:
            col_count = max(len(row) for row in data)

            for row in data:
                while len(row) < col_count:
                    row.append(Paragraph("", styles["TableText"]))

            available_width = A4[0] - 1.5 * inch

            table = Table(
                data,
                colWidths=[available_width / col_count] * col_count,
                repeatRows=1,
                hAlign="LEFT",
            )

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.HexColor("#183153")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.white, colors.HexColor("#F3F6FA")]),
            ]))

            story.extend([Spacer(1, 6), table, Spacer(1, 8)])

        table_rows = []

    for raw in lines:
        line = raw.strip()

        if line.startswith("|") and line.endswith("|"):
            in_table = True
            table_rows.append(line)
            continue

        if in_table:
            flush_table()
            in_table = False

        if not line:
            continue

        # Horizontal separator.
        if line == "---":
            story.append(HRFlowable(
                width="100%",
                thickness=0.6,
                color=colors.lightgrey,
                spaceBefore=6,
                spaceAfter=8,
            ))
            continue

        # Main title and title page.
        if line.startswith("# "):
            title = clean_inline(line[2:])

            if first_title:
                story.append(Spacer(1, 1.1 * inch))
                story.append(Paragraph(title, styles["PaperTitle"]))
                story.append(Spacer(1, 10))
                story.append(Paragraph(
                    "Research Paper | Internship Project",
                    styles["PaperSubtitle"],
                ))
                story.append(Spacer(1, 0.35 * inch))
                story.append(HRFlowable(
                    width="65%",
                    thickness=1.2,
                    color=colors.HexColor("#28527a"),
                    hAlign="CENTER",
                    spaceAfter=22,
                ))
                story.append(Paragraph(
                    "Predictive Maintenance | Anomaly Detection | Smart Manufacturing",
                    styles["PaperSubtitle"],
                ))
                story.append(PageBreak())
                first_title = False
            else:
                story.append(Paragraph(title, styles["Section"]))

            continue

        if line.startswith("## "):
            story.append(Paragraph(
                clean_inline(line[3:]),
                styles["Section"],
            ))
            continue

        if line.startswith("### "):
            story.append(Paragraph(
                clean_inline(line[4:]),
                styles["Subsection"],
            ))
            continue

        # Remove accidental escaped numbered-list markers.
        line = re.sub(r"^(\\)?(\d+)\.\s+", r"\2. ", line)

        if line.startswith("- "):
            story.append(Paragraph(
                "- " + clean_inline(line[2:]),
                styles["PaperBullet"],
            ))
            continue

        if re.match(r"^\d+\.\s", line):
            story.append(Paragraph(
                clean_inline(line),
                styles["PaperBullet"],
            ))
            continue

        # Display equations without raw LaTeX delimiters.
        if line in (r"\[", r"\]", r"\(", r"\)"):
            continue

        line = line.replace(r"\[", "").replace(r"\]", "")
        line = line.replace(r"\(", "").replace(r"\)", "")
        line = line.replace(r"\frac", "")
        line = line.replace(r"\_", "_")

        story.append(Paragraph(clean_inline(line), styles["PaperBody"]))

    if in_table:
        flush_table()

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="Predictive Maintenance and Anomaly Detection",
        author="Internship Project",
    )

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    print("Research paper PDF generated successfully!")
    print(f"Output: {OUTPUT}")
    print(f"Source: {SOURCE}")


if __name__ == "__main__":
    build_pdf()

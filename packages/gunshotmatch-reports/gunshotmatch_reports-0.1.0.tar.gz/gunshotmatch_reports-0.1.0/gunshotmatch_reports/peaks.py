#!/usr/bin/env python3
#
#  peaks.py
"""
PDF Peak Report Generator.
"""
#
#  Copyright © 2024 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import os
from io import BytesIO
from typing import List, Optional, Tuple

# 3rd party
from domdf_python_tools.paths import PathLike
from libgunshotmatch.consolidate import ConsolidatedPeak
from libgunshotmatch.project import Project
from libgunshotmatch_mpl.peakviewer import draw_peaks
from libgunshotmatch_mpl.peakviewer import load_project as load_project
from matplotlib import pyplot as plt  # type: ignore[import]
from matplotlib.figure import Figure  # type: ignore[import]
from reportlab.graphics.shapes import Drawing  # type: ignore[import]
from reportlab.lib import colors  # type: ignore[import]
from reportlab.lib.pagesizes import A4  # type: ignore[import]
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # type: ignore[import]
from reportlab.lib.units import inch  # type: ignore[import]
from reportlab.pdfgen.canvas import Canvas  # type: ignore[import]
from reportlab.platypus import (  # type: ignore[import]
		BaseDocTemplate,
		PageBreak,
		Paragraph,
		SimpleDocTemplate,
		Spacer,
		Table
		)
from svglib.svglib import svg2rlg  # type: ignore[import]

__all__ = ("load_project", "build_peak_report", "figure_to_drawing", "scale")


def _get_peak_figure(project: Project, consolidated_peak: ConsolidatedPeak) -> Figure:

	# figsize = (6.4, 4.8)
	figsize = (10.5, 5)
	figure = plt.figure(figsize=figsize)
	axes = figure.subplots(
			len(project.datafile_data),
			1,
			sharex=True,
			)

	draw_peaks(project, consolidated_peak.meta["peak_number"], figure, axes)

	return figure


def scale(drawing: Drawing, scale: float) -> Drawing:
	"""
	Scale reportlab.graphics.shapes.Drawing() object while maintaining aspect ratio.

	:param drawing:
	:param scale:
	"""

	scaling_x = scaling_y = scale

	drawing.width = drawing.minWidth() * scaling_x
	drawing.height = drawing.height * scaling_y
	drawing.scale(scaling_x, scaling_y)

	return drawing


styles = getSampleStyleSheet()
title_style = ParagraphStyle(
		"Title",
		parent=styles["Heading1"],
		alignment=1,
		)
title_spacer_style = ParagraphStyle(
		"TitleSpacer",
		parent=title_style,
		textColor=colors.HexColor("#ffffff"),
		)


def figure_to_drawing(figure: Figure) -> Drawing:
	"""
	Convert a matplotlib figure to a reportlab drawing.

	:param figure:
	"""

	imgdata = BytesIO()
	figure.savefig(imgdata, format="svg")
	plt.close(fig=figure)
	imgdata.seek(0)  # go to start of BytesIO
	return svg2rlg(imgdata)


def build_peak_report(project: Project, pdf_filename: Optional[PathLike] = None) -> str:
	"""
	Construct a peak report for the given project and write to the chosen file.

	:param project:
	:param pdf_filename: Optional output filename. Defaults to :file:`{project_name}_peak_report.pdf`.
	:no-default pdf_filename:
	"""

	if pdf_filename is None:
		pdf_filename = project.name + "_peak_report.pdf"
	else:
		pdf_filename = os.fspath(pdf_filename)

	pageinfo = f"GunShotMatch Peak Report – {project.name}"

	def draw_footer(canvas: Canvas, doc: BaseDocTemplate) -> None:
		canvas.saveState()
		canvas.setFont("Times-Roman", 9)
		canvas.drawString(inch, 0.75 * inch, "Page %d – %s" % (doc.page, pageinfo))
		canvas.restoreState()

	doc = SimpleDocTemplate(
			pdf_filename,
			pagesize=A4[::-1],
			leftMargin=0.5 * inch,
			righMargin=0.5 * inch,
			topMargin=0.5 * inch,
			bottomMargin=0.5 * inch,
			title=pageinfo,
			)

	doc_elements = [Paragraph(pageinfo, style=title_style)]

	assert project.consolidated_peaks is not None
	max_peak_number = len(project.consolidated_peaks)

	for peak_idx, consolidated_peak in enumerate(project.consolidated_peaks):
		figure = _get_peak_figure(project, consolidated_peak)
		drawing = figure_to_drawing(figure)

		peak_metadata: List[Tuple[str, str]] = [
				("Peak", f"{peak_idx+1} / {max_peak_number}"),
				("Retention Time", f"{consolidated_peak.rt / 60}"),
				("Match Factor", f"{consolidated_peak.hits[0].match_factor}"),
				("Rejected", f"{not consolidated_peak.meta.get('acceptable_shape', True)}"),
				('', ''),
				]

		hits_data: List[Tuple[str, str, str]] = []
		for hit in consolidated_peak.hits[:5]:
			hits_data.append((hit.name, f"{hit.match_factor:.1f}", str(len(hit))))

		while len(hits_data) < 5:
			hits_data.append(('', '', ''))

		table_data = []
		for peak_row, hits_row in zip(peak_metadata, hits_data):
			table_row = peak_row + ('', ) + hits_row
			table_data.append(table_row)

		t = Table(table_data)
		doc_elements.append(t)

		doc_elements.append(scale(drawing, scale=0.8))
		doc_elements.append(Spacer(1, 0.2 * inch))
		doc_elements.append(PageBreak())
		doc_elements.append(Paragraph('a', style=title_spacer_style))
		# doc_elements.append(Spacer(1,1*inch))

	# Remove last page break to prevent blank page
	doc_elements.pop()
	doc_elements.pop()

	doc.build(doc_elements, onFirstPage=draw_footer, onLaterPages=draw_footer)

	return pdf_filename

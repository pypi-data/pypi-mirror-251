#!/usr/bin/env python3
#
#  chromatogram.py
"""
Common chromatogram drawing functionality.
"""
#
#  Copyright © 2023-2024 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import List, Optional, Union

# 3rd party
import matplotlib.transforms  # type: ignore[import]
from libgunshotmatch.project import Project
from matplotlib.axes import Axes  # type: ignore[import]
from matplotlib.figure import Figure  # type: ignore[import]

__all__ = ("add_repeat_name", "draw_chromatograms", "draw_peak_arrows", "draw_peak_vlines", "ylabel_use_sci")


def draw_peak_arrows(
		figure: Figure,
		axes: Axes,
		rt: float,
		intensity: float,
		colour: Optional[str] = None,
		) -> None:
	"""
	Draw an arrow above the peak at the given retention time.

	:param figure:
	:param axes:
	:param rt: Retention time in minutes.
	:param intensity: Peak apex height.
	"""

	trans_offset = matplotlib.transforms.offset_copy(
			axes.transData,
			fig=figure,
			x=-0.01,
			y=0.15,
			units="inches",
			)

	axes.plot(
			rt,
			intensity,
			marker="$\\downarrow$",
			markersize=10,
			linewidth=0,
			transform=trans_offset,
			color=colour,
			)


def draw_peak_vlines(
		axes: Axes,
		rt: Union[float, List[float]],
		intensity: Union[float, List[float]],
		colour: str = "red",
		) -> None:
	"""
	Draw a vertical line to the apex of the peak at the given retention time.

	:param axes:
	:param rt: Retention time in minutes.
	:param intensity: Peak apex height.
	"""

	axes.vlines(rt, 0, intensity, colors=colour)


def ylabel_use_sci(axes: Axes) -> None:
	"""
	Set matplotlib axes to use scientific notation (with math text).

	:param axes:
	"""

	axes.ticklabel_format(axis='y', scilimits=(0, 0), useMathText=True)


def add_repeat_name(axes: Axes, repeat_name: str) -> None:
	"""
	Add a repeat name label to the top left of the given axes.
	"""

	axes.annotate(repeat_name, (0.01, 0.8), xycoords="axes fraction")


def draw_chromatograms(project: Project, figure: Figure, axes: List[Axes]) -> None:
	"""
	Draw chromatogram for each repeat in the project.

	:param project:
	:param figure:
	:param axes:
	"""

	assert project.consolidated_peaks is not None

	for idx, (repeat_name, repeat) in enumerate(project.datafile_data.items()):
		# for peak in repeat.qualified_peaks:
		# 	print(peak.rt/60, peak.hits[0].name)
		# for peak in repeat.peaks:
		# 	print(peak.rt/60, peak.area)
		# print(repeat_name)
		# print(project.alignment.get_peak_alignment(minutes=True)[repeat_name])
		assert repeat.datafile.intensity_matrix is not None
		tic = repeat.datafile.intensity_matrix.tic

		times = []
		intensities = []
		for time, intensity in zip(tic.time_list, tic.intensity_array):
			time /= 60  # To minutes
			if time >= 3:
				times.append(time)
				intensities.append(intensity)

		ax = axes[idx]

		ax.plot(times, intensities)

		# peak_rts, peak_heights = [], []
		for cp in project.consolidated_peaks:
			peak_rt = cp.rt_list[idx] / 60
			peak_height = intensities[times.index(peak_rt)]
			# peak_rts.append(peak_rt)
			# peak_heights.append(peak_height)
			draw_peak_vlines(ax, peak_rt, peak_height)
			draw_peak_arrows(figure, ax, peak_rt, peak_height)
		# draw_peak_vlines(ax, peak_rts, peak_heights)
		# draw_peak_arrows(fig, ax, peak_rts, peak_heights)

		ax.set_xlim(times[0], times[-1])
		ax.xaxis.set_tick_params(which="both", labelbottom=True)
		# ax.set_ylim([0, ax.get_ylim()[1]*1.2])
		ax.set_ylim([ax.get_ylim()[0] * 0.5, ax.get_ylim()[1] * 1.2])

		ylabel_use_sci(ax)
		add_repeat_name(ax, repeat_name)

	figure.supylabel("Intensity", fontsize="medium")
	axes[-1].set_xlabel("Retention Time (mins)")
	figure.suptitle(project.name)

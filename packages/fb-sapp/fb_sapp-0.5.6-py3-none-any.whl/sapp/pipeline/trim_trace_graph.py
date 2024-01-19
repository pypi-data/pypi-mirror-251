# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from typing import Tuple

from ..trace_graph import TraceGraph
from ..trimmed_trace_graph import TrimmedTraceGraph
from . import PipelineStep, Summary

log: logging.Logger = logging.getLogger("sapp")


class TrimTraceGraph(PipelineStep[TraceGraph, TraceGraph]):
    def run(self, input: TraceGraph, summary: Summary) -> Tuple[TraceGraph, Summary]:
        if summary.get("affected_files") is None:
            return input, summary

        log.info("Trimming graph to affected files.")
        trimmed_graph = TrimmedTraceGraph(
            summary["affected_files"], summary.get("affected_issues_only", False)
        )
        trimmed_graph.populate_from_trace_graph(input)
        return trimmed_graph, summary

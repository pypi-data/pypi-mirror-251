from typing import Dict, Union, TypedDict, List
from typing_extensions import Required


class IngestSpan(TypedDict, total=False):
    """ ingest_span. """

    description: str
    exclusive_time: "_PositiveFloat"
    is_segment: bool
    measurements: Dict[str, "_MeasurementValue"]
    _metrics_summary: Dict[str, List["_MetricSummaryValue"]]
    op: str
    parent_span_id: str
    profile_id: "_Uuid"
    received: "_PositiveFloat"
    segment_id: str
    sentry_tags: Dict[str, str]
    span_id: str
    start_timestamp: Required["_PositiveFloat"]
    """ Required property """

    status: str
    tags: Dict[str, str]
    timestamp: Required["_PositiveFloat"]
    """ Required property """

    trace_id: Required["_Uuid"]
    """ Required property """



class IngestSpanMessage(TypedDict, total=False):
    """ ingest_span_message. """

    event_id: "_Uuid"
    organization_id: Required[int]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    retention_days: Required[int]
    """ Required property """

    span: Required["IngestSpan"]
    """ Required property """



class _MeasurementValue(TypedDict, total=False):
    value: Required[Union[int, float]]
    """ Required property """

    unit: str


class _MetricSummaryValue(TypedDict, total=False):
    min: Union[int, float]
    max: Union[int, float]
    sum: Union[int, float]
    count: Union[int, float]
    tags: Dict[str, str]


_PositiveFloat = Union[int, float]
""" minimum: 0 """



_Uuid = str
"""
minLength: 32
maxLength: 36
"""


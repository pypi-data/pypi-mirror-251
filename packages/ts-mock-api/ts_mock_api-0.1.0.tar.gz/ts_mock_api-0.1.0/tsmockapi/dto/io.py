import datetime
import random
import typing
from enum import Enum
from pathlib import Path
from typing import NamedTuple


class Input(NamedTuple):
    # Should be something like "path/to/S1A_IW_GRDH_1SDV_20210102T224803_20210102T224828_035965_04368F_4953_COG.SAFE"
    product_path: typing.Union[str, Path]


class LabelType(Enum):
    SHIP = 1
    OIL = 2


class BBox(NamedTuple):
    x: float  # Object center position in pixel
    y: float  # Object center position in pixel
    width: float  # Object width in pixel
    height: float  # Object height in pixel


class Label(NamedTuple):
    # The Label provides the proposed label and probability
    # For the detections it is a predefined LabelType
    # For vessels it is an unstructured AIS type
    label: str
    probability: float


class Labels(NamedTuple):
    # Proposed label
    label: Label
    # All labels and their probabilities.
    labels: typing.List[Label]


# The distribution can for all intended purposes can be seen as gaussian.
# However, the parameters may not describe a gaussian distribution
class Distributed(NamedTuple):
    mean: float
    std: float


class LatLon(NamedTuple):
    latitude: float
    longitude: float


class VesselInfo(NamedTuple):
    lat_lon: typing.Optional[LatLon]

    heading: typing.Optional[float]  # 0-360 clockwise from NORTH as the heading provided by AIS
    velocity: typing.Optional[float]  # velocity in m/s TODO knob?

    label: typing.Optional[Labels]

    # properties as probability distributions
    velocity_dist: typing.Optional[Distributed]
    length_dist: typing.Optional[Distributed]
    beam_dist: typing.Optional[Distributed]
    heading_dist: typing.Optional[Distributed]


#
class Detection(NamedTuple):
    label: Labels
    bbox: BBox  # In center_x,center_y,width,height format
    vessel_info: VesselInfo


class Output(NamedTuple):
    version: str  # String denoting version in a semver format, i.e. 1.2 or 1.2.3
    processing_start_time: datetime.datetime
    processing_stop_time: datetime.datetime
    description: str  # TODO describe

    # List of strings denoting the labels utilized in the output
    label_names: typing.List[LabelType]

    # TODO are the 5 fields above usefull?

    # All detected ships, oil spill
    detections: typing.List[Detection]
    count: int  # Length of the detections list


class VesselInfoBuilder:
    def __init__(self):
        self.lat_lon = None
        self.heading = None
        self.velocity = None
        self.velocity_dist = None
        self.length_dist = None
        self.heading_dist = None
        self.beam_dist = None
        self.label = None

    def with_lat_lon(self):
        self.lat_lon = LatLon(latitude=56.234334, longitude=10.2429914)
        return self

    def with_heading(self):
        self.heading = 123.9
        return self

    def with_velocity(self):
        self.velocity = 123.9
        return self

    def with_distributions(self):
        dist = Distributed(random.random(), random.random())
        if bool(random.getrandbits(1)):
            self.velocity_dist = dist
        if bool(random.getrandbits(1)):
            self.length_dist = dist
        if bool(random.getrandbits(1)):
            self.heading_dist = dist
        if bool(random.getrandbits(1)):
            self.beam_dist = dist
        return self

    def with_label(self):
        names = ['Ro-Ro-Cargo', 'Fishing vessel', 'Tanker', 'Refrigerated Cargo ship', 'Wood chips carrier',
                 'Cruise ship', 'Pleasure Craft', 'Tug']
        random.shuffle(names)
        labels = [Label(t, random.random()) for t in names[0:random.randint(0, len(names))]]
        if len(labels) > 0:
            self.label = Labels(labels[0], labels=labels)
        return self

    def build(self):
        if bool(random.getrandbits(1)):
            self.with_label()
        if bool(random.getrandbits(1)):
            self.with_distributions()
        if bool(random.getrandbits(1)):
            self.with_velocity()
        if bool(random.getrandbits(1)):
            self.with_heading()
        if bool(random.getrandbits(1)):
            self.with_lat_lon()
        return VesselInfo(
            lat_lon=self.lat_lon,
            heading=self.heading,
            velocity=self.velocity,
            velocity_dist=self.velocity_dist,
            length_dist=self.length_dist,
            heading_dist=self.heading_dist,
            beam_dist=self.beam_dist,
            label=self.label
        )


class DetectionBuilder:
    def __init__(self):
        self.bbox = BBox(*[k for k in range(4)])
        self.vessel_info = VesselInfoBuilder()
        labels = [Label(t.name, random.random()) for t in LabelType]
        self.labels = Labels(labels[0], labels=labels)

    def build(self):
        return Detection(
            bbox=self.bbox,
            vessel_info=self.vessel_info.build(),
            label=self.labels,
        )


class OutputBuilder:
    def __init__(self):
        self.detections = []

    def with_detections(self, num_detections):
        detection_builder = DetectionBuilder()
        self.detections = [detection_builder.build() for _ in range(num_detections)]
        return self

    def build(self):
        return Output(
            version="0.1.0",
            processing_start_time=datetime.datetime.utcnow(),
            processing_stop_time=datetime.datetime.utcnow(),
            description="Mock output",
            label_names=[t for t in LabelType],
            detections=self.detections,
            count=len(self.detections)
        )

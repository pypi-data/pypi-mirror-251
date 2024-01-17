class BBox:
    in_formats = {
        'x1y1x2y2': lambda x1, y1, x2, y2: ((x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1),
        'x1y1wh': lambda x1, y1, w, h: (x1 + w / 2, y1 + h / 2, w, h),
        'xywh': lambda x, y, w, h: (x, y, w, h)
    }

    def __init__(self, **kwargs):
        if 'x1' in kwargs and 'x2' in kwargs and 'y1' in kwargs and 'y2' in kwargs:
            bbox = (kwargs['x1'], kwargs['y1'], kwargs['x2'], kwargs['y2'])
            bbox_format = 'x1y1x2y2'
            self._x, self._y, self._w, self._h = self.in_formats[bbox_format](*bbox)
        elif 'x' in kwargs and 'y' in kwargs and 'w' in kwargs and 'h' in kwargs:
            bbox = (kwargs['x'], kwargs['y'], kwargs['w'], kwargs['h'])
            bbox_format = 'xywh'
            self._x, self._y, self._w, self._h = self.in_formats[bbox_format](*bbox)
        elif 'x1' in kwargs and 'y1' in kwargs and 'w' in kwargs and 'h' in kwargs:
            bbox = (kwargs['x1'], kwargs['y1'], kwargs['w'], kwargs['h'])
            bbox_format = 'x1y1wh'
            self._x, self._y, self._w, self._h = self.in_formats[bbox_format](*bbox)
        else:
            raise ValueError(f"Could not format input {kwargs}")
        keys = {'x1', 'x2', 'y1', 'y2', 'x', 'y', 'w', 'h'}
        self._meta = {key: value for key, value in kwargs.items() if key not in keys}

    def intersects(self, other: "BBox") -> bool:
        return self.intersection(other) > 0

    def overlaps(self, other: "BBox"):
        return self.intersects(other)

    def reference(self, x, y):
        self._x -= x
        self._y -= y
        return self

    def normalize(self, xn: float, yn: float = None):
        if yn is None:
            x, y, w, h = map(lambda f: f * xn, self.xywh)
        else:
            x, y, w, h = self.xywh
            x, w = map(lambda f: f * xn, (x, w))
            y, h = map(lambda f: f * yn, (y, h))
        self._x, self._y, self._w, self._h = x, y, w, h
        return self

    def iou(self, other: "BBox", wh_only=False) -> float:
        intersection_area = self.intersection(other, wh_only=wh_only)
        union_area = self.area + other.area - intersection_area
        iou = intersection_area / union_area if union_area > 0 else 0
        return iou

    def intersection(self, other: "BBox", wh_only=False) -> float:
        bbox = self
        if wh_only:
            bbox = BBox(**self.bbox_dict)
            bbox._x = 0
            bbox._y = 0
            other = BBox(**other.bbox_dict)
            other._x = 0
            other._y = 0
        intersection_area = bbox.get_intersecting_box(other).area
        return intersection_area

    def get_intersecting_box(self, other: "BBox") -> "BBox":
        x1 = max(self.x1, other.x1)
        y1 = max(self.y1, other.y1)
        x2 = min(self.x2, other.x2)
        y2 = min(self.y2, other.y2)
        return BBox(x1=x1, y1=y1, x2=x2, y2=y2, **self.meta)

    @property
    def area(self):
        return self.w * self.h

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def x1(self):
        return self.x - self.w / 2

    @property
    def y1(self):
        return self.y - self.h / 2

    @property
    def x2(self):
        return self.x + self.w / 2

    @property
    def y2(self):
        return self.y + self.h / 2

    @property
    def bbox(self):
        return self.xywh

    @property
    def bbox_dict(self):
        return {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h, **self.meta}

    @property
    def x1y1x2y2(self):
        return self.x1, self.y1, self.x2, self.y2

    @property
    def x1y1wh(self):
        return self.x1, self.y1, self.w, self.h

    @property
    def x1x2y1y2(self):
        return self.x1, self.x2, self.y1, self.y2

    @property
    def xywh(self):
        return self.x, self.y, self.w, self.h

    @property
    def meta(self):
        return self._meta

    def __repr__(self):
        return f"{self.bbox}"

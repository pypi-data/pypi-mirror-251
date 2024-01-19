import random

from .colors import fade, RED, blend, YELLOW, BLACK
from .models import Model, MultiGradient, Map


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Pulsate(Model):
    """
    Adjusts the brightness of the underlying model from dimmest to brightest and back again.
    For example, the brightness may increase from 20% to 100% over 3 seconds and then dim
    back down to 20% over 1.5 seconds.

    Requires underlying model
    Position independent, time dependent
    """
    dimness = 0.0

    def __init__(self, name: str, dimmest: float, brightest: float, dim_ms: float, brighten_ms: float,
                 model: Model):
        """
        :param name: Name of this model, shown in debug messages
        :param dimmest: The min brightness (0.0 - 1.0)
        :param brightest: The max brightness (0.0 - 1.0)
        :param dim_ms: Dimming period in milliseconds
        :param brighten_ms: Brightening period in milliseconds
        :param model: The underlying model to be pulsated
        """
        self.dimmest = dimmest
        self.brightest = brightest
        self.dim_ms = dim_ms
        self.brighten_ms = brighten_ms
        self.period_ms = self.dim_ms + self.brighten_ms
        self.model = model

        super().__init__(name)

    def update(self, timestamp_ms: float):
        mod_timestamp_ms = timestamp_ms % self.period_ms
        if mod_timestamp_ms < self.brighten_ms:
            # We're getting brighter
            self.dimness = map_value(mod_timestamp_ms, 0.0, self.brighten_ms, self.brightest, self.dimmest)
        else:
            # We're getting dimmer
            self.dimness = map_value(mod_timestamp_ms, self.brighten_ms, self.period_ms, self.dimmest, self.brightest)

        self.model.update(timestamp_ms)

    def render(self, pos: float):
        old_color = self.model.render(pos)
        new_color = fade(old_color, self.dimness)
        return new_color


class Rotate(Model):
    """
    An animation that rotates or shifts lights to the left or right.
    Wraps around so that once a color reaches the end, then it wraps around.
    The frequency of rotation is given in cycles per second (Hz). Positive
    frequency rotates up, negative frequency rotates down.
    """
    rotation_offset = 0.0
    prev_timestamp_ms = 0

    def __init__(self, name: str, freq: float, model: Model):
        """
        :param name: Name of this model, shown in debug messages
        :param freq: Frequency of rotation in cycles per second
        :param model: The model to rotate
        """
        self.freq = freq
        self.model = model
        super().__init__(name)

    def update(self, timestamp_ms: int):
        # New timestamp, calculate the new offset and save the new timestamp
        delta_time_ms = timestamp_ms - self.prev_timestamp_ms
        self.prev_timestamp_ms = timestamp_ms

        # How far should we rotate given the time delta. Handle wrapping to keep
        # offset between 0.0 and 1.0. If the frequency is zero, don't rotate.
        if self.freq == 0:
            delta_pos = 0.0
        else:
            period_ms = 1000 / self.freq
            delta_pos = -delta_time_ms / period_ms

        self.rotation_offset = (self.rotation_offset + delta_pos) % 1.0
        if self.rotation_offset < 0.0:
            self.rotation_offset += 1.0

        # Update the wrapped model as well.
        self.model.update(timestamp_ms)

    def render(self, pos: float):
        # If there's no predecessor, then there's nothing to rotate. Bail out.
        if not self.model:
            return RED

        # Add the offset to the position, then correct for wrap-around
        rotated_pos = (pos + self.rotation_offset) % 1.0
        if rotated_pos < 0.0:
            rotated_pos += 1.0

        return self.model.render(rotated_pos)

    def set_period(self, new_period_ms: float):
        """ Set the period of one rotation cycle in ms """
        self.period_ms = new_period_ms

    def set_model(self, new_model: Model):
        """ Set the model to be rotated """
        self.model = new_model


class Flame(Model):
    COLOR1 = blend(RED, YELLOW, 0.5)
    COLOR2 = blend(RED, YELLOW, 0.7)
    COLOR3 = blend(RED, YELLOW, 0.9)
    PERIOD_MS = 110

    last_update_ms = 0.0
    gradient = MultiGradient("flame-multigradient", [BLACK, COLOR1, COLOR2, COLOR3, COLOR2, COLOR1, BLACK])
    model = Map("flame-map", 0.0, 1.0, 0.0, 1.0, gradient)

    def __init__(self, name: str):
        super().__init__(name)

    def update(self, timestamp_ms):
        # Only update the model occasionally to create the "flickering" effect
        if (timestamp_ms - self.last_update_ms) > self.PERIOD_MS:
            self.last_update_ms = timestamp_ms

            lower = random.uniform(0.0, 0.2)
            upper = random.uniform(0.8, 1.0)

            self.model.set_from_range(lower, upper)

            self.model.update(timestamp_ms)

    def render(self, pos: float):
        return self.model.render(pos)

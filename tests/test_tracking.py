import unittest
from types import SimpleNamespace

from ez2cv.detection.tracking import NoteTracker, TrackedEdge


class NoteTrackerTest(unittest.TestCase):
    def test_extrapolation_uses_recent_local_trajectory(self):
        calibration = SimpleNamespace(
            trigger_template_y_top=800.0,
            fps=60.0,
            pixels_per_frame=30.0,
            lanes=[],
            note_height=22.0,
            tail_release_offset_px=0.0,
        )
        tracker = NoteTracker(calibration)
        edge = TrackedEdge(
            id=0,
            lane=0,
            type="note",
            trajectory=[(frame, 710.0 + 10.0 * frame, 0.9)
                        for frame in range(8)],
            last_seen=7,
        )

        event = tracker._extrapolate_trigger(edge)

        self.assertIsNotNone(event)
        self.assertAlmostEqual(event.cross_frame, 9.0)
        self.assertGreater(event.timing_sigma_ms, 0.0)
        self.assertTrue(event.extrapolated)

    def test_longnote_endpoint_keeps_global_projection(self):
        calibration = SimpleNamespace(
            trigger_template_y_top=800.0,
            fps=60.0,
            pixels_per_frame=30.0,
            lanes=[],
            note_height=22.0,
            tail_release_offset_px=0.0,
        )
        tracker = NoteTracker(calibration)
        edge = TrackedEdge(
            id=0,
            lane=0,
            type="lnhead",
            trajectory=[(frame, 710.0 + 10.0 * frame, 0.9)
                        for frame in range(8)],
            last_seen=7,
        )

        event = tracker._extrapolate_trigger(edge)

        self.assertAlmostEqual(event.cross_frame, 7.0 + 20.0 / 30.0)


if __name__ == "__main__":
    unittest.main()

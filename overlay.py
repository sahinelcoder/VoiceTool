"""Recording-Overlay — Waveform-Visualizer über dem Dock."""

import logging
import random
import threading
import time

from AppKit import (
    NSApplication,
    NSBackingStoreBuffered,
    NSBezierPath,
    NSColor,
    NSFont,
    NSMakeRect,
    NSScreen,
    NSView,
    NSWindow,
    NSWindowStyleMaskBorderless,
)
import objc

logger = logging.getLogger(__name__)

# Layout
PILL_WIDTH = 200
PILL_HEIGHT = 48
PILL_CORNER_RADIUS = 24
BAR_COUNT = 24
BAR_WIDTH = 3
BAR_GAP = 2.5
BAR_MIN_HEIGHT = 3
BAR_MAX_HEIGHT = 28
DOCK_OFFSET = 80
ANIMATION_FPS = 30

# Shared audio level — wird direkt vom AudioRecorder geschrieben
_shared_level = 0.0
_shared_lock = threading.Lock()


def set_shared_level(level: float) -> None:
    global _shared_level
    _shared_level = level


def get_shared_level() -> float:
    return _shared_level


class WaveformView(NSView):
    """Custom View: Waveform-Bars die auf Audio-Level reagieren."""

    def initWithFrame_(self, frame):
        self = objc.super(WaveformView, self).initWithFrame_(frame)
        if self is None:
            return None
        self._bar_heights = [BAR_MIN_HEIGHT] * BAR_COUNT
        self._target_heights = [BAR_MIN_HEIGHT] * BAR_COUNT
        self._phase = 0
        return self

    def updateLevel(self):
        """Liest shared level und berechnet neue Ziel-Höhen."""
        level = get_shared_level()
        self._phase += 1

        for i in range(BAR_COUNT):
            center_factor = 1.0 - abs(i - BAR_COUNT / 2) / (BAR_COUNT / 2)
            center_factor = center_factor ** 0.6
            variation = random.uniform(0.5, 1.0)
            target = BAR_MIN_HEIGHT + (BAR_MAX_HEIGHT - BAR_MIN_HEIGHT) * level * center_factor * variation
            self._target_heights[i] = max(BAR_MIN_HEIGHT, target)

        # Smooth interpolation
        smoothing = 0.35
        for i in range(BAR_COUNT):
            self._bar_heights[i] += (self._target_heights[i] - self._bar_heights[i]) * smoothing

        self.setNeedsDisplay_(True)

    def drawRect_(self, rect):
        # Hintergrund
        bg = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.08, 0.08, 0.10, 0.92)
        bg.setFill()
        pill = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
            self.bounds(), PILL_CORNER_RADIUS, PILL_CORNER_RADIUS
        )
        pill.fill()

        # Subtiler Border
        border_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 1.0, 1.0, 0.08)
        border_color.setStroke()
        pill.setLineWidth_(0.5)
        pill.stroke()

        # Waveform-Bars
        total_bars_width = BAR_COUNT * BAR_WIDTH + (BAR_COUNT - 1) * BAR_GAP
        start_x = (PILL_WIDTH - total_bars_width) / 2
        center_y = PILL_HEIGHT / 2

        for i in range(BAR_COUNT):
            h = self._bar_heights[i]
            x = start_x + i * (BAR_WIDTH + BAR_GAP)
            y = center_y - h / 2

            intensity = 0.3 + 0.7 * ((h - BAR_MIN_HEIGHT) / max(1, BAR_MAX_HEIGHT - BAR_MIN_HEIGHT))
            bar_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 1.0, 1.0, intensity)
            bar_color.setFill()

            bar_rect = NSMakeRect(x, y, BAR_WIDTH, h)
            bar_path = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
                bar_rect, BAR_WIDTH / 2, BAR_WIDTH / 2
            )
            bar_path.fill()


class RecordingOverlay:
    """Verwaltet das Recording-Overlay-Fenster über dem Dock."""

    def __init__(self):
        self._window = None
        self._view = None
        self._timer = None
        self._running = False

    def show(self):
        """Zeigt das Overlay an."""

        def _create_on_main():
            screen = NSScreen.mainScreen()
            if screen is None:
                return
            screen_frame = screen.frame()

            x = (screen_frame.size.width - PILL_WIDTH) / 2
            y = DOCK_OFFSET

            window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                NSMakeRect(x, y, PILL_WIDTH, PILL_HEIGHT),
                NSWindowStyleMaskBorderless,
                NSBackingStoreBuffered,
                False,
            )
            window.setLevel_(25)
            window.setOpaque_(False)
            window.setBackgroundColor_(NSColor.clearColor())
            window.setIgnoresMouseEvents_(True)
            window.setCollectionBehavior_(1 << 4)
            window.setHasShadow_(True)

            view = WaveformView.alloc().initWithFrame_(
                NSMakeRect(0, 0, PILL_WIDTH, PILL_HEIGHT)
            )
            window.setContentView_(view)
            window.orderFrontRegardless()

            self._window = window
            self._view = view
            self._running = True

            # NSTimer auf dem Main Thread Run Loop für garantierte UI-Updates
            from Foundation import NSTimer, NSRunLoop, NSDefaultRunLoopMode
            self._timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                1.0 / ANIMATION_FPS,
                view,
                objc.selector(WaveformView.updateLevel, signature=b"v@:@"),
                None,
                True,
            )
            NSRunLoop.currentRunLoop().addTimer_forMode_(self._timer, NSDefaultRunLoopMode)
            logger.info("Overlay angezeigt + Timer gestartet")

        if threading.current_thread() is threading.main_thread():
            _create_on_main()
        else:
            from PyObjCTools import AppHelper
            AppHelper.callAfter(_create_on_main)

    def hide(self):
        """Versteckt das Overlay."""
        self._running = False
        set_shared_level(0.0)

        def _close_on_main():
            if self._timer is not None:
                self._timer.invalidate()
                self._timer = None
            if self._window is not None:
                self._window.orderOut_(None)
                self._window = None
                self._view = None

        if threading.current_thread() is threading.main_thread():
            _close_on_main()
        else:
            from PyObjCTools import AppHelper
            AppHelper.callAfter(_close_on_main)

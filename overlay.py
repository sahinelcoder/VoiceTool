"""Recording-Overlay — zeigt visuelles Feedback während der Aufnahme."""

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


# Konstanten
PILL_WIDTH = 120
PILL_HEIGHT = 36
PILL_CORNER_RADIUS = 18
DOT_RADIUS = 5
ANIMATION_INTERVAL = 0.5


class RecordingDotView(NSView):
    """Custom View: rote pulsierende Dot + "Recording" Text."""

    def initWithFrame_(self, frame):
        self = objc.super(RecordingDotView, self).initWithFrame_(frame)
        if self is None:
            return None
        self._dot_visible = True
        return self

    def drawRect_(self, rect):
        # Hintergrund: dunkle Pill
        bg = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.1, 0.1, 0.1, 0.85)
        bg.setFill()
        path = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
            self.bounds(), PILL_CORNER_RADIUS, PILL_CORNER_RADIUS
        )
        path.fill()

        # Roter Dot (pulsiert)
        if self._dot_visible:
            dot_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.2, 0.2, 1.0)
        else:
            dot_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.5, 0.1, 0.1, 0.6)
        dot_color.setFill()
        dot_rect = NSMakeRect(14, (PILL_HEIGHT - DOT_RADIUS * 2) / 2, DOT_RADIUS * 2, DOT_RADIUS * 2)
        dot_path = NSBezierPath.bezierPathWithOvalInRect_(dot_rect)
        dot_path.fill()

        # Text
        text_color = NSColor.whiteColor()
        text_color.set()
        font = NSFont.systemFontOfSize_(13)
        attrs = {
            "NSFontAttributeName": font,
            "NSForegroundColorAttributeName": text_color,
        }
        from Foundation import NSString, NSMakePoint

        text = NSString.stringWithString_("Recording")
        text.drawAtPoint_withAttributes_(NSMakePoint(32, 10), attrs)

    def toggle_dot(self):
        self._dot_visible = not self._dot_visible
        self.setNeedsDisplay_(True)


class RecordingOverlay:
    """Verwaltet das Recording-Overlay-Fenster."""

    def __init__(self):
        self._window = None
        self._view = None
        self._animation_thread = None
        self._running = False

    def show(self):
        """Zeigt das Overlay an (muss vom Main Thread aufgerufen werden oder via performSelectorOnMainThread)."""
        from Foundation import NSObject

        def _create_on_main():
            screen = NSScreen.mainScreen()
            if screen is None:
                return
            screen_frame = screen.frame()

            # Oben-mittig positionieren
            x = (screen_frame.size.width - PILL_WIDTH) / 2
            y = screen_frame.size.height - PILL_HEIGHT - 60  # 60px vom oberen Rand

            window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                NSMakeRect(x, y, PILL_WIDTH, PILL_HEIGHT),
                NSWindowStyleMaskBorderless,
                NSBackingStoreBuffered,
                False,
            )
            window.setLevel_(25)  # NSStatusWindowLevel
            window.setOpaque_(False)
            window.setBackgroundColor_(NSColor.clearColor())
            window.setIgnoresMouseEvents_(True)
            window.setCollectionBehavior_(1 << 4)  # NSWindowCollectionBehaviorCanJoinAllSpaces

            view = RecordingDotView.alloc().initWithFrame_(NSMakeRect(0, 0, PILL_WIDTH, PILL_HEIGHT))
            window.setContentView_(view)
            window.orderFrontRegardless()

            self._window = window
            self._view = view

        # Auf Main Thread ausführen
        if threading.current_thread() is threading.main_thread():
            _create_on_main()
        else:
            from PyObjCTools import AppHelper
            AppHelper.callAfter(_create_on_main)

        # Animation starten
        self._running = True
        self._animation_thread = threading.Thread(target=self._animate, daemon=True)
        self._animation_thread.start()

    def hide(self):
        """Versteckt das Overlay."""
        self._running = False

        def _close_on_main():
            if self._window is not None:
                self._window.orderOut_(None)
                self._window = None
                self._view = None

        if threading.current_thread() is threading.main_thread():
            _close_on_main()
        else:
            from PyObjCTools import AppHelper
            AppHelper.callAfter(_close_on_main)

    def _animate(self):
        """Pulsiert den roten Dot."""
        while self._running and self._view is not None:
            time.sleep(ANIMATION_INTERVAL)
            if self._view is not None and self._running:
                from PyObjCTools import AppHelper
                AppHelper.callAfter(self._view.toggle_dot)

import enum

class BrowserType(enum.Enum):
    CHROME = "chrome"  # Or any string that AsyncSession expects
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"
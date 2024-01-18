import pytest
import regex
import re
from pyimportcyclefinder.protocol.re import PatternProtocol, MatchProtocol, ScannerProtocol
from pyimportcyclefinder.protocol.regex import ExtendedPatternProtocol, ExtendedMatchProtocol, ExtendedScannerProtocol, SplitterProtocol
from as3lib import toplevel as as3
from as3lib import configmodule
import platform
from typing import Union
import sys

class ApplicationDomain:
    pass
class Capabilities:
    #!get actual values later
    #!document changes from original
    avHardwareDisable = True
    def _getCPUBits():
        return as3.Number(configmodule.cpuAddressSize)
    cpuAddressSize = property(fget=_getCPUBits) #returns 32 (32bit system) or 64 (64bit system)
    def _getCPUArch():
        return configmodule.cpuArchitecture
    cpuArchitecture = property(fget=_getCPUArch) #returns "PowerPC","x86","SPARC",or "ARM"
    #hasAccessibility
    hasAudio = True #value is always True
    #hasAudioEncoder
    #hasEmbeddedVideo
    #hasIME
    #hasMP3
    #hasPrinting
    #hasScreenBroadcast
    #hasScreenPlayback
    #hasStreamingAudio
    #hasStreamingVideo
    #hasTLS
    #hasVideoEncoder
    def _getDebug():
        return configmodule.as3DebugEnable
    isDebugger = property(fget=_getDebug)
    #isEmbeddedInAcrobat
    #language
    #languages
    #localFileReadDisable
    def _getManuf():
        return configmodule.manufacturer
    manufacturer = property(fget=_getManuf)
    #maxLevelIDC
    def _getOS():
        return configmodule.os
    os = property(fget=_getOS)
    #pixelAspectRatio
    #playerType
    #screenColor
    #screenDPI
    #screenResolutionX
    #screenResolutionY
    #serverString
    #supports32BitProcesses
    #supports64BitProcesses
    #touchscreenType
    def _getVer():
        return configmodule.version
    version = property(fget=_getVer)
    def hasMultiChannelAudio(type:Union[str,as3.String]):
        pass
class ImageDecodingPolicy:
    ON_DEMAND = "onDemand"
    ON_LOAD = "onLoad"
class IME:
    pass
class IMEConversionMode:
    ALPHANUMERIC_FULL = "ALPHANUMERIC_FULL"
    ALPHANUMERIC_HALF = "ALPHANUMERIC_HALF"
    CHINESE = "CHINESE"
    JAPANESE_HIRAGANA = "JAPANESE_HIRAGANA"
    JAPANESE_KATAKANA_FULL = "JAPANESE_KATAKANA_FULL"
    JAPANESE_KATAKANA_HALF = "JAPANESE_KATAKANA_HALF"
    KOREAN = "KOREAN"
    UNKNOWN = "UNKNOWN"
class JPEGLoaderContex:
    pass
class LoaderContext:
    pass
class MessageChannel:
    pass
class MessageChannelState:
    CLOSED = "closed"
    CLOSING = "closing"
    OPEN = "open"
class Security:
    pass
class SecurityDomain:
    pass
class SecurityPanel:
    pass
class System:
    #freeMemory
    #ime
    #privateMemory
    #totalMemory
    #totalMemoryNumber
    #useCodePage
    def disposeXML():
        pass
    def exit(code:Union[int,as3.int,as3.uint]=0):
        sys.exit(int(code))
    def gc():
        pass
    def pause():
        pass
    def pauseForGCIfCollectionImminent():
        pass
    def resume():
        pass
    def setClipboard():
        pass
class SystemUpdater:
    pass
class SystemUpdaterType:
    DRM = "drm"
    SYSTEM = "system"
class TouchscreenType:
    FINGER = "finger"
    NONE = "none"
    STYLUS = "stylus"
class Worker:
    pass
class WorkerDomain:
    pass
class WorkerState:
    NEW = "new"
    RUNNING = "running"
    TERMINATED = "terminated"
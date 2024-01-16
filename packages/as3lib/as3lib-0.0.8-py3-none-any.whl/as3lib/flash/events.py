
class Event:
   ACTIVATE = "activate"
   ADDED = "added"
   ADDED_TO_STAGE = "addedToStage"
   BROWSER_ZOOM_CHANGE = "browerZoomChange"
   CANCEL = "cancel"
   CHANGE = "change"
   CHANNEL_MESSAGE = "channelMessage"
   CHANNEL_STATE = "channelState"
   CLEAR = "clear"
   CLOSE = "close"
   CLOSING = "closing"
   COMPLETE = "complete"
   CONNECT = "connect"
   CONTEXT3D_CREATE = "context3DCreate"
   COPY = "copy"
   CUT = "cut"
   DEACTIVATE = "deactivate"
   DISPLAYING = "displaying"
   ENTER_FRAME = "enterFrame"
   EXIT_FRAME = "exitFrame"
   EXITING = "exiting"
   FRAME_CONSTRUCTED = "frameConstructed"
   FRAME_LABEL = "frameLabel"
   FULLSCREEN = "fullscreen"
   HTML_BOUNDS_CHANGE = "htmlBoundsChange"
   HTML_DOM_INITIALIZE = "htmlDOMInitialize"
   HTML_RENDER = "htmlRender"
   ID3 = "id3"
   INIT = "init"
   LOCATION_CHANGE = "locationChange"
   MOUSE_LEAVE = "mouseLeave"
   NETWORK_CHANGE = "networkChange"
   OPEN = "open"
   PASTE = "paste"
   PREPARING = "preparing"
   REMOVED = "removed"
   REMOVED_FROM_STAGE = "removeFromStage"
   RENDER = "render"
   RESIZE = "resize"
   SCROLL = "scroll"
   SELECT = "select"
   SELECT_ALL = "selectAll"
   SOUND_COMPLETE = "soundComplete"
   STANDARD_ERROR_CLOSE = "standardErrorClose"
   STANDARD_INPUT_CLOSE = "standardInputClose"
   STANDARD_OUTPUT_CLOSE = "standardOutputClose"
   SUSPEND = "suspend"
   TAB_CHILDREN_CHANGE = "tabChildrenChange"
   TAB_ENABLE_CHANGE = "tabEnableChange"
   TAB_INDEX_CHANGE = "tabIndexChange"
   TEXT_INTERACTION_MODE_CHANGE = "textInteractionModeChange"
   TEXTURE_READY = "textureReady"
   UNLOAD = "unload"
   USER_IDLE = "userIdle"
   USER_PRESENT = "userPresent"
   VIDEO_FRAME = "videoFrame"
   WORKER_STATE = "workerState"
   def __init__(self, type, bubbles=False, cancelable=False):
      pass

class IEventDispatcher:
   def __init__(self):
      self.eventobjects = {}
   def addEventListener(type, listener, useCapture=False, priority=0, useWeakReference=False):
      pass
   def dispatchEvent(event):
      pass
   def hasEventListener(type):
      pass
   def removeEventListener(type, listener, useCapture=False):
      pass
   def willTrigger(type):
      pass
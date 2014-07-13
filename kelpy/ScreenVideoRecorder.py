# Linux/pygame video capture utility by Christopher Night - public domain
# Requires mogrify, oggenc (if there's audio), and mencoder

# BASIC USAGE: record your gameplay from start to finish in real time
#    During the game, simply import this file as a module (import vidcap) from your main module.
#    A frame will be recorded every time you call pygame.display.flip(). After the game, execute
#    this file directly to encode the AVI:
#       python vidcap.py [viddir]
#    This will produce the file viddir/vidcap.avi.
#    Make sure you call pygame.init() early in your program (but after you import vidcap). This is
#    how vidcap knows to start the recording, and it's necessary for timing to work.

# To delete a video and all of its files, simply remove the directory.

# TODO: document calling the functions manually

# TODO: how to start and stop recording during gameplay

# TODO: draw mouse cursor

import pygame, datetime, os, inspect, subprocess, glob

wrappygame = True  # Should this module wrap pygame.display.flip and pygame.init so that the video
                   # is automatically recorded when you call these functions? If this is false,
                   # you'll need to call vidcap.cap() once per frame

viddir = None  # You can set this to an explicit directory path if you like
               # Otherwise it will default to a directory with a current timestamp

recordsymbol = False  # Put a "recording" symbol in the corner when recording
                     # The symbol itself doesn't get recorded

usepng = False  # Use png rather than bmp (takes less disk space but is slower)


_recording = True
_recordaudio = True

def timestamp(t = None):
    """10-digit timestamp"""
    return str(10000000000 + (pygame.time.get_ticks() if t is None else t))[1:]

def defaultdir():
    """Default (timestamp-based) directory name"""
    return datetime.datetime.now().strftime("vidcap-%Y%m%d%H%M%S")

def checkdir():
    """Make sure viddir is set and the path exists"""
    global viddir
    if viddir is None: viddir = defaultdir()
    if not os.path.exists(viddir):
        os.mkdir(viddir)

def lastdir():
    """The latest timestamp-based directory"""
    dirs = [d for d in os.listdir(".") if d.startswith("vidcap-")]
    return max(dirs) if dirs else None

def currentimagepath(exten = None, t = None):
    checkdir()
    if exten is None: exten = "png" if usepng else "bmp"
    fname = "frame-" + timestamp(t) + "." + exten
    return os.path.join(viddir, fname)

def isimagepath(path, exten = "png"):
    """Does the path describe a timestamped image?"""
    return path.endswith("." + exten) and path[-14:-4].isdigit() and path[-20:-14] == "frame-"

def isaudiopath(path, exten = "ogg"):
    """Does the path describe a timestamped image?"""
    return path.endswith("." + exten) and path[-14:-4].isdigit() and path[-20:-14] == "audio-"

def blankpath():
    checkdir()
    return os.path.join(viddir, "frame-blank.png")

def makeblankframe(anyframe, color=(0,0,0)):
    surf = pygame.image.load(anyframe)
    surf.fill(color)
    pygame.image.save(surf, blankpath())

def framelistpath():
    return os.path.join(viddir, "framelist.txt")

def currentaudiopath():
    checkdir()
    return os.path.join(viddir, "audio-%s.raw" % timestamp())

def logpath():
    checkdir()
    return os.path.join(viddir, "log.txt")

def log(line):
    f = open(logpath(), "a")
    f.write(timestamp() + " " + line + "\n")
    f.close()

def getmonitorsource():
    p = subprocess.Popen("pactl list".split(), stdout = subprocess.PIPE)
    out, err = p.communicate()
    mline = [line for line in out.splitlines() if "Monitor Source: " in line][0]
    _, _, monitorsource = mline.partition("Monitor Source: ")
    return monitorsource

def unmutemonitorsource(monitorsource = None):
    if monitorsource is None: monitorsource = getmonitorsource()
    stdin = "set-source-mute %s false" % monitorsource
    p = subprocess.Popen(["pacmd"], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    _, _ = p.communicate(stdin)

_audioprocess = None  # Set to None when audio recording is off
                      # Set to the AudioProcess instance when audio recording is in progress
                      # Module-level private because we need it to be GC'd, so please don't make
                      #   reference to it.
class AudioProcess(object):
    """Use RAII to make sure the audio recording gets shut down when we're done"""
    format = "s16le"
    def __init__(self, filename = None, monitorsource = None):
        self.filename = filename or currentaudiopath()
        self.monitorsource = monitorsource or getmonitorsource()
        self.com = "parec --format=%s --device=%s" % (self.format, self.monitorsource)
        log("audiostart %s %s" % (self.filename, self.format))
        self.file = open(self.filename, "wb")
        self.process = subprocess.Popen(self.com.split(), stdout = self.file)
    def terminate(self):
        if self.process:
            log("audiostop")
            self.process.terminate()
            self.process, self.file = None, None
    def __del__(self):
        self.terminate()

def startaudiorecording(monitorsource = None):
    global _audioprocess
    if not _recordaudio: return
    if _audioprocess: return  # Already recording
    log("audio 1")
    if monitorsource is None: monitorsource = getmonitorsource()
    log("audio 2")
    unmutemonitorsource(monitorsource)
    log("audio 3")
    _audioprocess = AudioProcess(monitorsource = monitorsource)
    log("audio 4")

def stopaudiorecording():
    global _audioprocess
    _audioprocess.terminate()
    _audioprocess = None

def cap(screen = None):
    """Call this once a frame to capture the screen"""
    global _recordaudio
    if not _recording: return
    if screen is None: screen = pygame.display.get_surface()
    fname = currentimagepath()
    pygame.image.save(screen, fname)
    if recordsymbol and pygame.time.get_ticks() / 250 % 2:
        pygame.draw.circle(screen, (255, 0, 0), (14, 14), 10, 0)
    startaudiorecording()

pdflip = pygame.display.flip
def capandflip():
    cap()
    pdflip()

pinit = pygame.init
def init():
    log("init")
    startaudiorecording()
    pinit()

def convertallbmps():
    """Convert all bmps in the vidcap directory into pngs (requires mogrify) - slow!"""
    if not glob.glob(os.path.join(viddir, "*.bmp")): return
    print "mogrify -format png " + os.path.join(viddir, "*.bmp")
    os.system("mogrify -format png " + os.path.join(viddir, "*.bmp"))
    os.system("rm " + os.path.join(viddir, "*.bmp"))

def convertaudio():
    """Convert raw audio in the vidcap directory into oggs"""
    for f in os.listdir(viddir):
        if not f.endswith(".raw"): continue
        rawfile = os.path.join(viddir, f)
        oggfile = rawfile[:-4] + ".ogg"
        if os.path.exists(oggfile): continue
        os.system("oggenc --raw --quiet -o %s %s" % (oggfile, rawfile))

def interpolateframes(fts, nframes, dt, t0 = 0):
    # TODO: better interpolation function
    iframes = []
    index = 1  # The first frame that's later than the current timestamp 
    for jframe in range(nframes):
        t = float(jframe) * dt + t0
        while index < len(fts) and t > fts[index][0]:
            index += 1
        iframes.append(fts[index-1][1])
    return iframes

# The following class is used for audio logging. We use a wrapper around pygame.mixer that logs all
#   access to the module. Later, this can be reconstructed by reading the log.

class LogAlias(object):
    """An alias to an object that logs all calls made."""
    _aliasList = {}
    _listname = "objs"  # How the array should be written in the log
    _nAlias = 0
    def __init__(self, obj, name, ongetattr = None):
        self._obj = obj
        self._name = name  # This is a string that can be eval'd to give self._obj later
        self._n = self._nAlias
        self._aliasList[LogAlias._nAlias] = self
        self._log("%s[%s] = %s" % (self._listname, self._n, self._name))
        self._ongetattr = ongetattr  # Callback when self.__getattr__ is called
        LogAlias._nAlias += 1
    @staticmethod
    def _lname(obj):
        """This is the name of this object via the alias list, if applicable"""
        return "%s[%s]" % (LogAlias._listname, obj._n) if isinstance(obj, LogAlias) else repr(obj)
    def __getattr__(self, attr):
        """self.x is a LogAlias wrapper around self._obj.x"""
        if self._ongetattr: self._ongetattr()
        if attr not in self.__dict__:
            obj = getattr(self._obj, attr)
            name = LogAlias._lname(self) + "." + attr
            self.__dict__[attr] = LogAlias(obj, name)
        return self.__dict__[attr]
    def __call__(self, *args):
        callstr = "%s(%s)" % (LogAlias._lname(self), ", ".join(LogAlias._lname(arg) for arg in args))
        ret = self._obj(*args)
        if inspect.isclass(self._obj):  # If constructing a new instance...
            return LogAlias(ret, callstr)  # ...return a LogAlias wrapping the instance
        self._log(callstr)
        return ret
    def __repr__(self):
        return "LogAlias(%r)" % repr(self._obj)
    def _log(self, text):
        """Add the specified text to the log along with timestamp"""
        log("alias " + text)

_wrapped = False
if __name__ != "__main__":
    mixer = LogAlias(pygame.mixer, "pygame.mixer")
    if wrappygame and not _wrapped:
        pygame.mixer = mixer
        pygame.display.flip = capandflip
        pygame.init = init
        _wrapped = True


if __name__ == "__main__":
    # Encode the images and audio into an AVI file
    import sys, numpy

    fps = 25
    fixedfps = False
    
    viddir = sys.argv[1] if len(sys.argv) > 1 else lastdir()
    if not viddir:
        print "Vidcap directory not found!"
        print "Please specify a directory on the command line."
        sys.exit()
    print "vidcap directory is %s" % viddir

    print "Converting BMPs into PNGs...."
    convertallbmps()
    
    # Analyze log file
    objs = {}
    logcomms = []
    t0 = None  # Start time of video
    for line in open(logpath(), "r"):
        words = line.split()
        if len(words) < 2: continue
        t = int(words[0])
        if words[1] == "init":
#            if t0 is None: t0 = t
            pass
        if words[1] == "audiostart":
            if t0 is None: t0 = t
        if words[1] == "alias":
            logcomms.append((t, " ".join(words[2:]).strip()))
    
    frames0 = sorted([f for f in os.listdir(viddir) if isimagepath(f)])
    fts = [(int(frame[6:16]), os.path.join(viddir, frame)) for frame in frames0]
    if t0 is None: t0 = fts[0][0]
    tend = fts[-1][0]
    print t0, tend

    if fixedfps:
        nframes = len(frames0)
    else:
        print "Number of input frames: %s" % len(frames0)
        nframes = int((tend - t0) * fps / 1000.)
    vidlength = nframes * 1. / fps
    print "Number of video frames: %s at %sfps" % (nframes, fps)
    print "Video duration: %.2fs" % vidlength

    makeblankframe(fts[0][1])
    fts = [(-1, blankpath())] + fts

    # TODO: handle fixedfps mode
    if fixedfps:
        pass
    else:
        framelist = interpolateframes(fts, nframes, 1000. / fps, t0)
        open(framelistpath(), "w").write("\n".join(framelist))
    
    print "Converting RAW audio into OGG format...."
    convertaudio()

    oggfile = os.path.join(viddir, sorted([f for f in os.listdir(viddir) if isaudiopath(f)])[0])
    
    com = []
    com.append("mencoder")
#    com.append("mf://%s/*.png" % viddir)
    com.append("mf://@%s" % framelistpath())
    com.append("-mf fps=%s:type=png" % fps)
    com.append("-ovc copy")
    com.append("-oac pcm -audiofile %s" % oggfile if oggfile else "-oac copy")
    com.append("-o %s/vidcap.avi" % viddir)

    com = " ".join(com)
    print
    print "Encoding video...."
    print com
    os.system(com)  # TODO: check for errors
    
    print
    print "Video created:", os.path.join(viddir, "vidcap.avi")


"""
    pygame.init()
    screen = pygame.display.set_mode(pygame.image.load(fts[1][1]).get_size())

    while fts:
        t = pygame.time.get_ticks()
        while logcomms and logcomms[0][0] < t:
            exec(logcomms[0][1])
            del logcomms[0]
        while fts and fts[0][0] < t:
            screen.blit(pygame.image.load(fts[0][1]), (0,0))
            del fts[0]
        pygame.display.flip()


    print "Creating audio track...."
    def getsndarray(filename, volume, cache = {}):
        key = filename, volume
        if key not in cache:
            s = pygame.mixer.Sound(filename)
            s.set_volume(0)
            s.play()
            cache[key] = pygame.sndarray.array(s)
            if volume != 1: cache[key] = numpy.int16(cache[key] * volume)
        return cache[key]

"""

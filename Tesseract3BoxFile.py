# -*- coding: utf-8 -*-

from utils import *
import cv2, sys, codecs, os



class Tesseract3BoxFile:
    filename=None
    imgfile=None
    boxes=None
    img=None
    writdir=None
    def __init__(self, filename=None):
        if not filename:
            return
        self.filename=filename
        self.boxes=parse_boxfile(filename)
        self.imgfile="%s.tif" % (filename[:-4])
        print "reading %s" % (self.imgfile)
        self.img=cv2.imread(self.imgfile)
        try:
            img=cv2.imread(self.imgfile)
        except:
            pass
        self.writdir=self.getDirection()
        
    def getDirection(self):
        "try to guess the writing direction from the first two boxes"
        #eliminate small differences
        b1l = (self.boxes[0].left / 10 ) * 10
        b2l = (self.boxes[1].left / 10 ) * 10
        if b2l - b1l > 0:
            return "rtl"
        else:
            return "ltr"
        
        
    def writebox(self, boxfile, box):
        bf=codecs.open(boxfile, 'w', 'utf-8')
        bf.write("%s 0 0 %d %d 0\n" % (box.text, box.width, box.height))
        bf.close()

    def writetext(self, out=None):
        if not out:
            f=codecs.getwriter('utf8')(sys.stdout)
        else:
            f=codecs.open(out, "w", "utf-8")
        f.write("\n")
        lastl=0
        for box in self.boxes:
            if self.writdir == "rtl":
                l=(box.left / 10) * 10
            else:
                l=(box.bottom / 10) * 10
            if l < lastl:
                f.write("\n")
                f.write("# l, lastl %d %d\n" % (l, lastl)), 
            lastl = l
            f.write(box.text)
        f.write("\n")
        f.close()
    def cutbox(self, no, target=None):
        #boxes are 0 based
        fn=self.filename[:-4].split('.')
        fn.insert(-2, no)
        ret=False
        try:
            thisbox=self.boxes[int(no)-1]
        except:
            print "Box not found!"
            return ret
        #out=self.img[self.img.shape[0]-thisbox.top:self.img.shape[0]-thisbox.bottom,thisbox.left:thisbox.right]
        if len(self.img) > 0:
            try:
                out=self.img[self.img.shape[0]-thisbox.top:self.img.shape[0]-thisbox.bottom,thisbox.left:thisbox.right]
            except:
                print "Error cropping box %s" % (no)
        if not target:
            #target = "%s_%s_%s.tif" % (self.filename[:-4], no, thisbox.text)
            target = "%s.tif" % (".".join(fn))
            self.writebox("%s.box" % (target[:-4]), thisbox)
            return cv2.imwrite(target, out)
        else:
            try:
                os.makedirs(target)
            except:
                pass
            tgfile = "%s/%s.tif" % (target, ".".join(fn))
            self.writebox("%s.box" % (tgfile[:-4]), thisbox)
            return cv2.imwrite(tgfile, out)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        bf= Tesseract3BoxFile(sys.argv[1])
        if sys.argv[2] == "text":
            bf.writetext("%s.txt" % (sys.argv[1][:-4]))
        else:
            bf.writetext(sys.argv[2])
    else:
        for line in codecs.open(sys.argv[1], 'r', 'utf-8'):
            if ".box" in line:
                boxfile = line[:-1]
                bf= Tesseract3BoxFile(boxfile)
            elif "Couldn't find a matching blob" in line:
                n = line.split('/')[0].split()[-1]
                bf.cutbox(n, "bx")


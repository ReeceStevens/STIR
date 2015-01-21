from PIL import Image
import sys

def viewDicom(dcmfile):
    size = (dcmfile.Columns, dcmfile.Rows);
    bits = dcmfile.BitsAllocated;
    samples = dcmfile.SamplesPerPixel;
    if (bits == 8) and (samples == 1):
        mode == "L";
    elif (bits == 8) and (samples == 3):
        mode == "RGB";
    elif (bits == 16):
        mode = "I;16"
    else:
        raise TypeError("Can't determine how to display this image!");

    im = Image.frombuffer(mode, size, dcmfile.PixelData, "raw", mode, 0, 1);
    im.show();
    im.convert('L').save('../test_image.png');

if __name__ == "__main__":
    viewDicom(sys.argv[1]);

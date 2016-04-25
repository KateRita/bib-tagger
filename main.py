import os
import cv2
import pprint

import bibtagger.bibtagger as bt

#runs the pipeline on all photos
if __name__ == "__main__":

    sourcefolder = os.path.abspath(os.path.join(os.curdir, 'photos'))
    outfolder = os.path.abspath(os.path.join(os.curdir, 'photos-out'))

    # Ensure that the directory that holds our output directories exists...
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    print 'Searching for image folders in {} folder'.format(sourcefolder)

    # Extensions recognized by opencv
    exts = ['.bmp', '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.jpeg', '.jpg',
            '.jpe', '.jp2', '.tiff', '.tif', '.png']

    bib_index = {}
    results = []
  # For every image in the source directory
    for racephoto_dir in os.listdir(sourcefolder):
        print "Collecting images from directory {}".format(racephoto_dir)
        img_list = []
        img_namelist = []
        filenames = sorted(os.listdir(os.path.join(sourcefolder, racephoto_dir)))

        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext in exts:
                img_list.append(cv2.imread(os.path.join(sourcefolder, racephoto_dir, filename)))
                img_namelist.append((racephoto_dir,filename))


        print "Extracting bibs."
        for idx,image in enumerate(img_list):
            #Do Operation
            print "======================================="
            print "Processing Image: ", img_namelist[idx]
            results.append(bt.findBibs(image,os.path.join(outfolder,img_namelist[idx][0],img_namelist[idx][1])))

            for bib_number in results[len(results) - 1].bib_numbers:
                if bib_number not in bib_index:
                    bib_index[bib_number] = []
                bib_index[bib_number].append(img_namelist[idx])


    print "======================================="
    print "FINAL STATS"
    print "Faces:", sum(result.faces for result in results )
    print "Bibs:", sum(result.bibs for result in results )
    print "SWT:", sum(result.swt for result in results )
    print "Bib Numbers:", sum(len(result.bib_numbers) for result in results )
    pprint.pprint(("Bib Index: ", bib_index), width=1)

        #make output directory
        #print "writing output to {}".format(os.path.join(outfolder, racephoto_dir))
        #if not os.path.exists(os.path.join(outfolder, racephoto_dir)):
        #    os.mkdir(os.path.join(outfolder, racephoto_dir))

        #write output image
        #for idx, image in enumerate(out_list):
        #    cv2.imwrite(os.path.join(outfolder, racephoto_dir, 'frame{0:04d}.png'.format(idx)), image)

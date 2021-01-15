import patoolib
import os
import platform
import img2pdf


#takes in a cbr file and unpacks it returning 
# the location of the exploded files 
def extract(rarfile):
    dr = "./" + rarfile[:-4]
    os.mkdir(dr)
    patoolib.extract_archive(rarfile, outdir=dr)
    lvldwn = 0
    while(True):
        if os.path.exists(dr):
            if(os.listdir(dr + "/")[0][-4] != "."):
                dr += "/" + os.listdir(dr + "/")[0]        
                os.chdir(os.listdir()[0])
                lvldwn += 1
            else:
                break
        else:
            break
    for i in range(lvldwn):
        os.chdir("..")
    return dr

def makePDF(dr, output):
    print(dr)
    if os.path.exists(dr + "/ComicInfo.xml"):
        os.remove(dr + "/ComicInfo.xml")
    images = os.listdir(dr)
    os.chdir(dr + "/")

    #directly perfoming a binary write is a lot faster than using a library
    with open(output +".pdf", "w+b") as f:
        f.write(img2pdf.convert([i for i in os.listdir() if i.endswith(".jpg")]))
    for image in images:
        os.remove(image)
    os.chdir("../") 
    

    #Legacy
    # for image in images:
    #     x,y = (Image.open(dr + "/" + image)).size
    #     pdf = FPDF(unit = "pt", format = [x,y])
    #     print(image)
    #     pdf.add_page()
    #     pdf.image(dr + "/" + image, 0, 0)
    # pdf.output("./" + output + ".pdf", "F")


def main():
    home = os.getcwd()
    cbrFile = input("Enter filename (include extension):")
    if((cbrFile[-3:].lower()) != "cbr"):
        print("Invalid File")
        exit()
    cmd = '\"' + cbrFile + '\" \"' + cbrFile[:-4] + '.rar\" '

    if (platform.system() == "Windows"):
        os.system("copy " + cmd)
    else:
        os.system("cp " + cmd)

    rarFile = cbrFile[:-4] + ".rar"
    
    dr = extract(rarFile)
    makePDF(dr, home + "/" + cbrFile[:-4])
    os.chdir(home)
    os.remove(rarFile)
    os.removedirs(dr)
    print("Done!")    

if __name__ == "__main__":
    main()
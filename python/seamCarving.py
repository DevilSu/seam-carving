
import sys
import copy

import numpy as np  

from PIL import Image

def DeleteSeams(transBitMask, size_diff, source):

    i=transBitMask.shape[0]-1
    j=transBitMask.shape[1]-1

    result=copy.deepcopy(source)
    for k in range(size_diff[0]+size_diff[1]):
        energy=energyRGB(result)
        if transBitMask[i, j]==0:
            # print('transBitMask=0')
            [optSeamMaskT, seamEnergyRow]=findOptSeam(energy.T) 
            resultT=np.transpose(result, (1,0,2))
            resultT=np.resize(resultT[optSeamMaskT], (optSeamMaskT.shape[0], optSeamMaskT.shape[1]-1, 3))
            result =np.transpose(resultT, (1,0,2))   


            i-=1
        else:
            # print('transBitMask= else')
            [optSeamMask, seamEnergyCol]=findOptSeam(energy)
            result=np.resize(result[optSeamMask], (optSeamMask.shape[0], optSeamMask.shape[1]-1, 3))
            j-=1

    return result

def findOptSeam(energy):
    # Find opt "horizontal" seam
    # print("findOptSeam")
    M=np.pad(energy, [(0, 0), (1, 1)], mode='constant', constant_values=np.finfo(np.float64).max)

    [H, W]=M.shape

    #-----SLOW-----
    # Cal energy spread
    for i in range(1, H):
        for j in range(1, W-1):
            M[i,j]=energy[i,j-1]+np.min(M[i-1, (j-1):(j+2)])
    #-----SLOW-----

    # Find min energy
    idx       =np.argmin(M[H-1, :])
    seamEnergy=M[H-1, idx]
    print('Optimal energy:', seamEnergy)

    # Init optimal seam mask
    optSeamMask=np.zeros(energy.shape, dtype=bool)
    optSeamMask[H-1, idx-1]=1

    # Traverse back the path
    for i in range(H-2, -1, -1):
        # # sys.exit()
        idxtmp=np.argmin(M[i, (idx-1):(idx+2)])
        idxtmp=idxtmp+idx-1
        optSeamMask[i, idxtmp-1]=1
        idx=idxtmp

        # print('after idx:', idx)
        # raw_input("Press Enter to continue...")

    # Convert mask to 1s & 0s
    optSeamMask=np.invert(optSeamMask)

    return [optSeamMask, seamEnergy]

def energyRGB(source):
    [Rdx, Rdy]=np.gradient(source[:,:,0])
    [Gdx, Gdy]=np.gradient(source[:,:,1])
    [Bdx, Bdy]=np.gradient(source[:,:,2])

    result= np.abs(Rdx)+np.abs(Rdy) \
           +np.abs(Gdx)+np.abs(Gdy) \
           +np.abs(Bdx)+np.abs(Bdy)

    return result

def findTransportMatrix(source, size_diff):
    # print('findTransportMatrix')

    T           =np.zeros((size_diff[0]+1, size_diff[1]+1))
    transBitMask=-1*np.ones((T.shape))

    # print('HI~')
    # print(T.shape)

    # Fill in borders
    source_NoRow=copy.deepcopy(source)
    for i in range(1, T.shape[0]):
        print('i=', i)
        energy=energyRGB(source_NoRow)
        [optSeamMaskT, seamEnergyRow]=findOptSeam(energy.T) 
        source_NoRowT=np.transpose(source_NoRow, (1,0,2))
        source_NoRowT=np.resize(source_NoRowT[optSeamMaskT], (optSeamMaskT.shape[0], optSeamMaskT.shape[1]-1, 3))
        source_NoRow =np.transpose(source_NoRowT, (1,0,2))   
        transBitMask[i, 0]=0
        T[i, 0]=T[i-1, 0]+seamEnergyRow

    source_NoCol=copy.deepcopy(source)
    for j in range(1, T.shape[1]):
        # print('j=', j)
        energy=energyRGB(source_NoCol)
        [optSeamMask, seamEnergyCol]=findOptSeam(energy)
        source_NoCol=np.resize(source_NoCol[optSeamMask], (optSeamMask.shape[0], optSeamMask.shape[1]-1, 3))
        # source_NoCol[optSeamMask].resize((optSeamMask.shape[0], optSeamMask.shape[1]-1, 3))
        transBitMask[0, j]=1
        T[0, j]=T[0, j-1]+seamEnergyCol
        # print('j=', j, T[0, j])
        # raw_input("Press Enter to continue...")
    

    # sys.exit()


    # Fill in internal
    for i in range(1, T.shape[0]):
        source_WithoutRow=source
        for j in range(1, T.shape[1]):
            print('i,j=', i, j)

            energy=energyRGB(source_WithoutRow)
            
            # [optSeamMask, seamEnergyRow]=findOptSeam(energy.T)
            # optSeamMask=optSeamMask.T
            # source_NoRow=np.resize(source_WithoutRow[optSeamMask], (optSeamMask.shape[0]-1, optSeamMask.shape[1], 3))

            [optSeamMaskT, seamEnergyRow]=findOptSeam(energy.T) 
            source_WithoutRowT=np.transpose(source_WithoutRow, (1,0,2))
            source_NoRowT=np.resize(source_WithoutRowT[optSeamMaskT], (optSeamMaskT.shape[0], optSeamMaskT.shape[1]-1, 3))
            source_NoRow =np.transpose(source_NoRowT, (1,0,2)) 




            [optSeamMask, seamEnergyCol]=findOptSeam(energy)
            source_NoCol=np.resize(source_WithoutRow[optSeamMask], (optSeamMask.shape[0], optSeamMask.shape[1]-1, 3))


            val1=T[i-1, j  ]+seamEnergyRow
            val2=T[i  , j-1]+seamEnergyCol

            if val1>val2:
                val=val2
                idx=1
            else:
                val=val1
                idx=0

            transBitMask[i, j]=idx

            source_WithoutRow=source_NoCol


        energy=energyRGB(source)
        [optSeamMaskT, seamEnergyRow]=findOptSeam(energy.T) 
        sourceT=np.transpose(source, (1,0,2))
        sourceT=np.resize(sourceT[optSeamMaskT], (optSeamMaskT.shape[0], optSeamMaskT.shape[1]-1, 3))
        source=np.transpose(sourceT, (1,0,2))   

    return [T, transBitMask]

def seamcarving(source, size_new):
    [H, W, C]=source.shape

    H_diff=H-size_new[0]
    W_diff=W-size_new[1]

    size_diff=[H_diff, W_diff]

    # reduce
    [T, transBitMask]=findTransportMatrix(source, size_diff)
    result=DeleteSeams(transBitMask, size_diff, source)

    # Convert back to uint8
    result=result.astype(np.uint8)

    return result


def main():
    # img=Image.open('../data/sea.jpg')
    # img=Image.open('../data/sea_small3.jpg')
    filename="1_portrait"
    filename="2_group"
    filename="3_sports"
    filename="4_food"
    filename="5_cat"
    filename="6_um_law_library"
    filename="7_building"
    filename="8_bird_eye"
    filename="9_long_exposure"
    img=Image.open("../data/"+filename+".jpg")
  
    # summarize some details about the image
    print('Format    :', img.format)
    print('Image size:', img.size)
    print('Mode      :', img.mode)

    [W, H]=img.size
    # img=img.resize([W/3, H/3])

    # Convert to numpy array
    source=np.asarray(img, dtype=np.float64)
    source=source
    print("Convert to ndarray")
    print('Type :', type(source))
    print('Shape:', source.shape)

    [H, W, C]=source.shape

    # New size
    H_new=int(np.floor(H))
    W_new=int(np.floor(W)-100)

    size_new=[H_new, W_new]

    print('New Shape:', size_new)

    # sys.exit()

    result=seamcarving(source, size_new)
    print('HII')
    print(result.shape)
    img_seamcarving=Image.fromarray(result)



    # Scale
    img_scale=img.resize([W_new, H_new])

    # Show the images
    # img.show()
    # img_scale.show()

    # img_seamcarving.show()
    
    print('HIII')
    print(filename)
    print(source.shape)
    print(result.shape)
    
    img_seamcarving.save("../data/"+filename+"_new.jpg")
    # sys.exit()
     
if __name__ == '__main__':
    main()
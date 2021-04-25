function image = seamCarving(image, newSize)
    sizeReductionX = size(image, 1) - newSize(1);
    sizeReductionY = size(image, 2) - newSize(2);
    
    mmax = @(left, right) max([left right]);
    
    image = seamCarvingReduce([mmax(0, sizeReductionX), mmax(0, sizeReductionY)], image);
end

function image = seamCarvingReduce(sizeReduction, image)
    if (sizeReduction == 0)
        return;
    end;
    a=1
    [T, transBitMask] = findTransportMatrix(sizeReduction, image);
    image = DeleteSeams(transBitMask, sizeReduction, image, @reduceImageByMask);
end
function imageReduced = reduceImageByMask( image, seamMask, isVertical )
    if (isVertical)
        imageReduced = reduceImageByMaskVertical(image, seamMask);
    else
        imageReduced = reduceImageByMaskHorizontal(image, seamMask');
    end;
end

function imageReduced = reduceImageByMaskVertical(image, seamMask)
    [row, col, rc]=size(image);
    imageReduced=zeros(row, col-1, rc);
    for k=1:1:row,
        [val, idx]=min(seamMask(k, :));
        imageReduced(k, 1:(idx-1), :)=image(k, 1:(idx-1), :);
        imageReduced(k, idx:(col-1), :)=image(k, (idx+1):col, :);
    end
end

function imageReduced = reduceImageByMaskHorizontal(image, seamMask)
    [row, col, rc]=size(image);
    imageReduced=zeros(row-1, col, rc);
    for k=1:1:col,
        [val, idx]=min(seamMask(:, k));
        imageReduced(1:(idx-1), k, :)=image(1:(idx-1), k, :);
        imageReduced(idx:(row-1), k, :)=image((idx+1):row, k, :);
    end
end

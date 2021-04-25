function [optSeamMask, seamEnergy] = findOptSeam(energy)
    M = padarray(energy, [0 1], realmax('double'));
    sz = size(M);
    
    for k=2:1:sz(1),
        for m=2:1:(sz(2)-1),
            M(k,m)=energy(k,m-1)+min(M(k-1,(m-1):(m+1)));
        end
    end

    [val, idx] = min(M(sz(1), :));
    seamEnergy = val;
    
    % Initial for optimal seam mask
    optSeamMask = zeros(size(energy), 'uint8');
 
    optSeamMask(sz(1), idx-1)=1;
    for k=(sz(1)-1):-1:1,
        [~, idxtmp] = min( M(k, (idx-1):(idx+1)) );
        idxtmp=idxtmp+idx-2;
        optSeamMask(k, idxtmp-1)=1;
        idx=idxtmp;
        dum=1;
    end
    
    optSeamMask = ~optSeamMask; 
end

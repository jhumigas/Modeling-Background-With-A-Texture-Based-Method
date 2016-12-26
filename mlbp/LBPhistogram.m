function [h] = LBPhistogram(xc,yc,Rregion,P,imgLBPd)
%LBPHISTOGRAM Computes LBP histogram of a region around a given pixel
%   The region to consider is a square with side equals to 2*Rregion+1
%   The region is centered in the pixel of xc,yc coordinates
%   R is the square on each to compute the LBP of a given pixel
%   imgIn is the image to process, prepocessed to be gray-scaled

% TODO : correct => LBP on the whole image then histogram
% Region considered square of side 
% - - -
% - X -
% - - -

% imgLBPdRegion = imgLBPd(xc-Rregion:xc+Rregion,yc-Rregion:yc+Rregion);

% To display computed over the region
% histogram(LBPresult, 'Normalization','probability');

h = zeros(1,2^P);

for k=1:2^P
    h(k) = length(find(imgLBPd(xc-Rregion:xc+Rregion,yc-Rregion:yc+Rregion)==k-1));
end

h = h/sum(h);

end


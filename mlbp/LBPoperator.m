function [LBPvalue] = LBPoperator(xc,yc,R,P,inputImg)
%LBPOPERATOR Summary of this function goes here
%   Detailed explanation goes here

% inputImg should contains double elements
% Check how to add R and P as input

%R = 2;
a = 3;

% Consider a Square containing the circle
% Compute the binary map on that square

LBPmap = (inputImg(xc-R:xc+R,yc-R:yc+R) - inputImg(xc,yc) + a) >=0;
LBPmap = double(LBPmap);

% Extract only the points in the perimeter
% 4 steps, one for each side


    if R==2 
        if P == 4
            LBPpins = [LBPmap(1,R+1) LBPmap(R+1,R+3) LBPmap(R+3,R+1) LBPmap(R+1,1)];
        elseif P == 8
            LBPpins = [LBPmap(1,2:2:end) LBPmap(2:2:end,end)' LBPmap(end,end-1:-2:2) LBPmap(end-1:-2:2,1)'];
        elseif P == 16
            LBPpins = [LBPmap(1,1:end) LBPmap(2:end,end)' LBPmap(end,end-1:-1:1) LBPmap(end-1:-1:2,1)'];
        else
            % Other conf of 8
            LBPpins = [LBPmap(1,1:2:end) LBPmap(3:2:end,end)' LBPmap(end,end-3:-2:1) LBPmap(end-3:-2:3,1)'];
        end
    elseif R==1
        if P==8
            LBPpins = [LBPmap(1,1:end) LBPmap(2:end,end)' LBPmap(end,end-1:-1:1) LBPmap(end-1:-1:2,1)'];
        elseif P==4
            LBPpins = [LBPmap(1,2) LBPmap(2,end) LBPmap(end,2) LBPmap(2,1)];
        else
            % Other P = 4
            LBPpins = [LBPmap(1,1:2:end) LBPmap(end,end:-2:1)];
        end
    end
    

LBPvalue = LBPpins*2.^[0:length(LBPpins)-1]';
end


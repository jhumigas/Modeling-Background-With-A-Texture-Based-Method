%% Images files

clc; clear all, close all;
sequence = dir('../sequence2/input/*.jpg');

%% Retrieving first image

img1 = imread(strcat(sequence(1).folder,'/', sequence(1).name));
% simshow(img1);
% Convert to grayscale
imgG = double(rgb2gray(img1));

% imgG = imresize(imgG, 0.4);
imshow(uint8(imgG));

%% Initialization

Tp = 0.7; % Background threshold, used to label pixels as background or foreground
Tb = 0.6; % Histograms threshold, used when learning the model of background histograms
K = 4; % Number of adaptive histograms
% B = K; % Number of selected histograms
% LBP Operator Parameters
Rregion = 5;
R = 1;
P = 8; % 4
% Todo : P, the number of binary pins is 4 by default
% Randomly initiate the k-Adaptive Histograms M and normalization
M = rand(K,2^P);
M = M./sum(M,2);
% MSelected = M;
kSelected = 1:K;
% Randomly initiate weights and normalization
W = rand(1,K);
W = W/sum(W);

alpha_b = 0.01; % Histogram learning rates
alpha_w = 0.01; % Weights learning rates
proxMeasures = zeros(1,K); % Proximity measures between a pixel and the current K background model
%% Background modelling and foreground detection on one sequence

for t=250:355
    % t = 1;
    display(t);
    img1 = imread(strcat(sequence(t).folder,'/', sequence(t).name));

    % Convert to grayscale
    imgG = double(rgb2gray(img1));

    % imgG = imresize(imgG, 0.5);

    [m, n] = size(imgG);
    % img = zeros(m-Rregion*2,n-Rregion*2);
    imgGLabelled = imgG;
    imgGLBPd = zeros(m-2*R, n-2*R);
    for k=1:m-2*R
        for l=1:n-2*R
        imgGLBPd(k, l) = LBPoperator(k+R,l+R,R,P,imgG);
        end
    end
    
    % Foreground detection
    for k=1:m-2*R-2*Rregion
        for l=1:n-2*R-2*Rregion
            % % Computing measures against Selected Models Histograms
            h = LBPhistogram(k+Rregion,l+Rregion,Rregion,P,imgGLBPd);
            proxMeasuresB = zeros(1,length(kSelected));
            for idx=1:length(kSelected)
                proxMeasuresB(idx) = sum(min(h, M(kSelected(idx),:)));
            end
            % % Labelling pixels
            if sum(proxMeasuresB > Tp) > 0
                % label background
                imgGLabelled(k+Rregion,l+Rregion) = 0;
            end
            
            imshow(uint8(imgGLabelled));
        end
    end
    
    % Background modelling
    for k=1:m-2*R-2*Rregion
        for l=1:n-2*R-2*Rregion
            % h for current pixel
            h = LBPhistogram(k+Rregion,l+Rregion,Rregion,P,imgGLBPd);

            % %Computing prox measures against K Model Histograms
            for idx=1:K
                proxMeasures(idx) = sum(min(h, M(idx,:)));
            end
            if max(proxMeasures) < Tp
                % No matches found between current pixel histogram and background
                % model histogram
                M(W == min(W),:) = h;
                W(1, W == min(W)) = 0.01;
            else
               bMatch = max(proxMeasures)== proxMeasures;
               % Unlikely to find 2 matches, otherwise further process might be
               % needed
               % Online K_means
               M(bMatch, :) = alpha_b*h + (1-alpha_b)*M(bMatch, :);
               Mk = zeros(1,K);
               Mk(1, bMatch) = 1;
               W = alpha_w*Mk+(1-alpha_w)*W;
            end
            
            % Selecting histograms
            sortedProxMeasures  =  sort(proxMeasures,'descend');
            kSelected = [];
            for b=1:K
                B = b;
                kSelected = [kSelected find(proxMeasures==sortedProxMeasures(b))];
                if (sum(sortedProxMeasures(1:b))) > Tb
                    break
                end
            end

        end
    end

end
%% Visualizing what's happening when playing with R
img1 = imread(strcat(sequence(489).folder,'/', sequence(332).name));

% Convert to grayscale
imgG = double(rgb2gray(img1));

[m, n] = size(imgG);

P = 4;
R = 1;
imgGLBP = zeros(m-2*R, n-2*R);
for k=1:m-2*R
    for l=1:n-2*R
        imgGLBP(k, l) = LBPoperator(k+R,l+R,R,P,imgG);
    end
end

imshow(uint8(imgGLBP));
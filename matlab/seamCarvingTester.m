% Clear all
clear; close all; clc;

% Load data
image = imread('../data/sea.jpg');
sz = size(image);
% resize image to half size
image = imresize(image, [floor(sz(1)/3), floor(sz(2)/3)]);
sz = size(image);
figure
imshow(image)

% Image resizing
% apply seam carving
tic
image_seamCarving = seamCarving(double(image), [floor(sz(1)), floor(sz(2)/2)]);
figure
imshow(uint8(image_seamCarving))
toc
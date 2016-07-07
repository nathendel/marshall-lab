function [ ss ] = ift_eig( M )
%UNTITLED8 Summary of this function goes here
%   Detailed explanation goes here

e=eig(M);
[v,d]=eig(M);
[a,b]=min((real(e)-1).^2);
disp(a)
ss=v(:,b);
if sum(ss)<0
    ss = ss.*-1;

end


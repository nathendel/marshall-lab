function [ output_args ] = ift_marksim( M )
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here

spots = size(M, 1);
N=zeros(spots,1);

num_p=200;
N(1)=num_p;


t=10000;
for i=1:t
% while true
    plot(M^i*N);
%     plot([L,L+.001],[0,num_p])
    
%     ylim([0,30])
    title(i);
%     drawnow;
    pause(.1);
    
    hold off
end


end


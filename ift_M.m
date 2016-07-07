function [ M,N ] = ift_M( L )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
% run commands here that call the matrix creator function


M=zeros(L*2);
% 
% for i=1:size
%     for j=1:size
%         M(ii
%         
%     end
%     
% end

% 
% 

diff=zeros(L);
diff(2:end,1:end-1)=eye(L-1)*.5;
diff=diff+diff';

M(L+1:end,L+1:end) = diff;
M(2:L+2,1:L+1)=eye(L+1);




% for i=1:L
%     for j=1:L-1
%         M(i+3,j+4)=.5;
% 
%     end
% end




M = M - diag(diag(M));

% defining recruitment/avalanching, these three must sum to 1
M(1,L*2)=.2;
M(end-1,end)=0;
M(end,end)=.8; %higher values mean higher buildup at base

N=zeros(L*2,1);

num_p=200;
N(1)=num_p;
% 
% t=10000;
% for i=1:t
% % while true
%     plot(M^i*N);
% %     plot([L,L+.001],[0,num_p])
%     
%     ylim([0,30])
%     title(i);
% %     drawnow;
%     pause(.1);
%     
%     hold off
% end


end


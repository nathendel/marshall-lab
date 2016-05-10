function [  ] = diffuse(  )
%DIFFUSE Summary of this function goes here
%   Detailed explanation goes here



m=0;
L=5;
D=1;
x=linspace(0,L,L*20);
t=linspace(0,1000,5);

% source=zeros(size(x));
% source(end-5)=1;
source=(exp(10*x)-1)/exp(10*L);



sol=pdepe(m,@pdex1pde,@pdex1ic,@pdex1bc,x,t);
u=sol(:,:,1)+3;



% A surface plot is often a good way to study a solution.
surf(x,t,u) 
title('Numerical solution computed with 20 mesh points.')
xlabel('Distance x')
ylabel('Time t')

% % A solution profile can also be illuminating.
% figure
% plot(x,u(1,:))
% title('Solution at t = 0')
% xlabel('Distance x')
% ylabel('u(x,2)')



function [c,f,s] = pdex1pde(x,t,u,DuDx)
c=1;
f=DuDx;
% s=1;


% global source
% global L



s=(exp(10*x)-1)/exp(10*5);


% s=source;



function u0 = pdex1ic(x)
% disp(x)
% u0=sin(pi*x);
% u0 = zeros(size(x));
% u0(end)=1;

% u0 = (exp(10*x)-1)/exp(10);
% disp(u0)

% global L

% u0=0;
% 
% global L


u0=0;

%u0=(exp(10*x)-1)/exp(10*L);

function [pl,ql,pr,qr] = pdex1bc(xl,ul,xr,ur,t)
pl=ul;
ql=0;
pr=0;
qr=1;



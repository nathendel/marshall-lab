% http://www.mathworks.com/help/pde/ug/applyboundarycondition.html#inputarg_model
% http://www.mathworks.com/help/pde/examples/heat-distribution-in-a-circular-cylindrical-rod.html

% numberOfPDE = 1;
% model = createpde(numberOfPDE);
% g = decsg([3 4 -1.5 1.5 1.5 -1.5 0 0 .2 .2]');
% 
% Convert the geometry and append it to the pde model
% geometryFromEdges(model,g);


% xspan = [0 1];
% y0 = 0
% [x,y]=ode23(@(x,y) 2*x, xspan, y0);
% 
% plot(x,y,'-o')

% f = @(x,y) [y(2); 0];
% [xs,yx]=ode45(f,[0,1],[1;0])
% plot(xs,yx)
% 
% f = @(x,y) [y(2);0];
% 
% [xs,ys] = ode45(f,[0,10],[0,1]);
% plot(xs,ys(:,1))
% xlabel('x')
% ylabel('y')
% 

m=0;
L=1;
D=1;
x=linspace(0,L,L*20);
t=linspace(0,2,5);

sol=pdepe(m,@pdex1pde,@bdex1ic,@pdex1bc,x,t);
u=sol(:,:,1);

function [c,f,s] = pdex1pde(x,t,u,DuDx)
c=1/D;
f=DuDx;
s=0;


function u0 = pdex1ic(x)
u0=sin(pi*x);


function [pl,ql,pr,qr] = pdex1bc(xl,ul,xr,ur,t)
pl=ul;
ql=0;
pr=pi*exp(-t);
qr=1;


% A surface plot is often a good way to study a solution.
surf(x,t,u) 
title('Numerical solution computed with 20 mesh points.')
xlabel('Distance x')
ylabel('Time t')

% A solution profile can also be illuminating.
figure
plot(x,u(end,:))
title('Solution at t = 2')
xlabel('Distance x')
ylabel('u(x,2)')
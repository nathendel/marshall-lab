
long = 200;

ss = zeros(long,1);

for i=3:long
   [m,n]=ift_M(i);
   counts = m^1000*n;
   ss(i) = counts(i);
  
end


[a,ss_L] = min((ss-1).^2);
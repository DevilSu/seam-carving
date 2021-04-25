function res = energyRGB(I)

R = I(:,:,1);
G = I(:,:,2);
B = I(:,:,3);
[Rdx, Rdy]=gradient(R);
[Gdx, Gdy]=gradient(G);
[Bdx, Bdy]=gradient(B);
res=abs(Rdx)+abs(Rdy)+abs(Gdx)+abs(Gdy)+abs(Bdx)+abs(Bdy);
end
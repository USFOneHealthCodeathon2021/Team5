au<-read.csv("Austin_data.csv",header = T)
aus<-as.matrix(data.frame(au[,c(125:237)],colnames=au$otu_id))
## dim(aus)
## N=21 T=114
pp<-c()
for (x in 1:1993) {
  t<-ts(as.vector(aus[x,]),frequency=7,start=1)
  sta<-stl(t,s.window = 21)
  trend<-as.vector(sta$time.series[,2])
  dX<-trend[94:114]-trend[93:113]
  v0=var(dX)
  dXbar=mean(dX)
  pos_mean=v0/(1/(113-1)+v0)*dXbar
  pos_var=1/(1/v0 + 21)
  p1 = pnorm(9, pos_mean, pos_var, lower.tail = FALSE)
  p2 = 1 - p1
  pp=cbind(pp,p1,p2)
} 
p=matrix(pp,ncol = 2,)
colnames(p)<-c("p1","p2")
p


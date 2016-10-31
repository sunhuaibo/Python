arg = commandArgs(T)
if (length(arg) != 1){
	cat("Usage: Rscript plot_pair_relationship.R <infile>")
	quit("no")
}
infile = arg[1]
colour = c("red","green","blue","black","yellow")
if (grepl("csv$",infile)){
	dat = read.table(infile,row.names = 1,head=T,sep=",")
}else{
	dat = read.table(infile,row.names = 1,head=T,sep="\t")
}
#dat = read.table(infile,row.names = 1,head=T,sep=",")
row_col = dim(dat)
row = row_col[1]
coloum = row_col[2]
all_max = max(dat)
all_min = min(dat)
pdf(paste(infile,"pdf",sep="."))
#plot(1:coloum,seq(0,all_max,length.out=coloum), type = "n",xaxt="n",xlab="",ylab="Frequence")
plot(1:coloum,seq(all_min,all_max,length.out=coloum), type = "n",xaxt="n",xlab="",ylab="Frequence")
axis(1,at=1:coloum,labels = colnames(dat))
for (j in 1:dim(dat)[2]){
	for (i in 1:dim(dat)[1]){
		if (dat[i,j] != 0){
			points(j,dat[i,j])
		}
	}
}
for (i in 1:row){
	for (j in 1:(coloum-1)){
		if (dat[i,j] != 0 && dat[i,j+1] != 0){
			segments(j,dat[i,j],j+1,dat[i,j+1],col=colour[j])
		}
	}
}
dev.off()

#################################################################
setwd("D:/09Limited_buffer/earlywarningbyci/gui")
csv <- read.csv("filter.csv",header=T, stringsAsFactors=F)
mystopwords<- unlist (read.table("D:/09Limited_buffer/earlywarningbyci/classification/chinese_stopword.txt",stringsAsFactors=F))
library(tm)
################################中文分词，也可以考虑使用rmmseg4j、rsmartcn
library("stringr")
sample.word<-iconv(csv$content,"utf-8","gbk")
tag<-str_extract(sample.word,"#.+?#")  
tag<-na.omit(tag)  #去除NA
tag<-unique(tag)    #去重
tag<-gsub("^#|#$","",tag)
removeNumbers = function(x) { ret = gsub("[0-9０１２３４５６７８９]","",x) }
wordsegment<- function(x) {
segmentCN(x)
}
removeStopWords = function(x,words) {
ret = character(0)
index <- 1
it_max <- length(x)
while (index <= it_max) {
if (length(words[words==x[index]]) <1) ret <- c(ret,x[index])
index <- index +1
}
ret
}
sample.words <- lapply(sample.word, removeNumbers)
sample.words<-gsub(pattern="http:[a-zA-Z\\/\\.0-9]+","",sample.words)

library("rJava")
library("Rwordseg")
#添加标签词
textwords=tag
insertWords(textwords)
sample.words <- lapply(sample.words, wordsegment)
corpus = Corpus(VectorSource(sample.words))
############################################### 创建词项-文档矩阵(TDM)
control=list(removePunctuation=T,minDocFreq=5,wordLengths = c(2, Inf),weighting = weightTfIdf)
doc.tdm=TermDocumentMatrix(corpus,control)
length(doc.tdm$dimnames$Terms)
tdm_removed=removeSparseTerms(doc.tdm, 0.9998) # 1-去除了低于 99.98% 的稀疏条目项
length(tdm_removed$dimnames$Terms)
############################################### 层次聚类
dist_tdm_removed <- dissimilarity(tdm_removed, method = 'cosine')
hc <- hclust(dist_tdm_removed, method = 'mcquitty')
cutNum = 7 #设置分割的类的数目
ct = cutree(hc,k=cutNum) #对树进行分割
sink(file="result.txt")
for(i in 1:cutNum){
  print(paste("第",i,"类： ",sum(ct==i),"个"));
  print("----------------");
  print(attr(ct[ct==i],"names"));
#   print(doc[as.integer(names(ct[ct==i]))])
  print("----------------")
}
sink()
################################################################插入
csv$clustertag<-as.character(ct)#csv$clustertag<-as.integer(ct)
################################################################词云
library(Rcpp)
library(RColorBrewer)
library(wordcloud)
sample.tdm <- TermDocumentMatrix(corpus, control = list(wordLengths = c(2, Inf)))#词长度最少为2
tdm_matrix <- as.matrix(sample.tdm)
meta(corpus,"cluster") <- csv$clustertag
unique_type <- unique(csv$clustertag)
n <- nrow(csv)
zz1 <- 1:n
cluster_matrix<-sapply(unique_type,function(type){apply(as.matrix(tdm_matrix[,zz1[csv$clustertag==type]]),1,sum)})
#矩阵二维转三维
png(paste("sample_cluster_comparison",".png", sep = ""), width = 500, height = 500 )
comparison.cloud(cluster_matrix)
title(main = "sample cluster comparision")
dev.off()
comparison.cloud(cluster_matrix)
#######################################################层次聚类过程图
#如果类数目较多，则会重合看不清楚，使用下列方法画出大像素图形
png("test.png",width=3500,height=3000) #将输出设备改为png，像素尽可能的大，但是如改的过大容易出现问题。

#cex为标签的大小,同时，可以使用cex.axis属性来改变坐标系上数字的大小，使用cex.lab改变下面矩阵名字的大小

#使用cex.main改变上方标题的大小，使用cex.sub改变下方聚类方法名称的大小，lwd是图形中线的宽度，此时图形将会在工作目录中看到
plot(hc,cex=2,cex.axis=3,cex.lab=3,cex.main=3,cex.sub=3,lwd=1.5)
rect.hclust(hc,k=15, border="red")#对聚类结果的标识
dev.off()

###################################按时刻观察事件图(待美化）
meta(corpus,"cluster") <- csv$created
unique_type <- unique(csv$created)
cluster_matrix<-sapply(unique_type,function(type){apply(as.matrix(tdm_matrix[,zz1[csv$created==type]]),1,sum)})
png(paste("sample_ cluster_comparison",".png", sep = ""), width = 800, height = 800 )
comparison.cloud(cluster_matrix)
title(main = "sample cluster comparision")
dev.off()

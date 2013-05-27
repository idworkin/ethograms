# basics of getting an ethogram set-up

trial.data <- read.csv("~/Dropbox/Dworkin_lab/Abhijna/Spider_data_NEW/May15/11_28_12_b1m.dat", 
    h=F, skip=24, col.names=c("time_mS", "behaviour"), colClasses=c("numeric", "character"), strip.white=T)
    
head(trial.data)
str(trial.data)

#convert to seconds
trial.data$time_S <- trial.data$time_mS/1000

#set initial time to zero
trial.data$time_S <- trial.data$time_S  -trial.data$time_S[1]

#make factors
trial.data$beh_factor <- as.factor(trial.data$behaviour)

beh_numb <- nlevels(trial.data$beh_factor)
beh_types <- levels(trial.data$beh_factor)

table(trial.data$behaviour)

crap <- rep(NA, nrow(trial.data))
i <- 1

# Sanity check
while(trial.data[i,2] != "3"){
    crap[i] <- print(trial.data[i,2])
    i <- i + 1}
   
# empty plot, setting up axes
par(mfrow=c(1,1))    
plot(trial.data$time_S, 
    xlim=c(0,max(trial.data$time_S)), ylim=c(0, beh_numb), type="n",
    xlab = "time in seconds", ylab = "behaviour",
    ann=F, yaxt="n", frame.plot=F)

for (i in 1:length(trial.data$beh_factor))  {
	ytop <- as.numeric(trial.data$beh_factor[i])
	ybottom <- ytop - 0.5
	rect(xleft=trial.data$time_S[i], xright=trial.data$time_S[i+1],
	     ybottom=ybottom, ytop=ytop, col = ybottom)}

axis(side=2, at = (1:beh_numb -0.25), labels=levels(trial.data$beh_factor)) 



# for (i in 1:nrow(trial.data)) {

# }        


i <- 1
while(trial.data[i,2] != "EOF"){
    print(trial.data[i,2])
    i <- i + 1}

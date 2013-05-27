# Fake ethogram data with 10 states

behav1 <- as.factor(sample(letters[1:10], 50, replace=T))

time_behav <- cumsum(rexp(length(time_behav),rate=2))

levels_behav <- nlevels(behav1)

plot(rep(1, length(time_behav)) ~ time_behav, 
    ylim=c(0, nlevels(behav1)), xlim=c(0, max(time_behav)),
    type="n", ann=F, yaxt="n", xlab = "time", frame.plot=F)
    
for (i in 1:length(behav1))  {
	ytop <- as.numeric(behav1[i])
	ybottom <- ytop - 0.5
	rect(xleft=time_behav[i], xright=time_behav[i+1],
	     ybottom=ybottom, ytop=ytop, col = ybottom)}

axis(side=2, at = (1:10 -0.25), labels=levels(behav1)) 
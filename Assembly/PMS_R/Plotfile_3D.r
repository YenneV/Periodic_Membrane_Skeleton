library(plotly)
library(plot3D)

x <- c(5, 15)
y <- c(5, 5)
z <- c(-3, 7)

data <- data.frame(x, y, z)

p1 <- scatter3D(x, y, z, bty = "g", type = "o", pch = 16, cex = 1, lwd = 4, phi = 20, theta = 40)
print(p1)

p <- plot_ly(data, x = ~x, y = ~y, z = ~z, type = 'scatter3d', mode = 'lines+markers',
             line = list(width = 6),
             marker = list(size = 3.5))


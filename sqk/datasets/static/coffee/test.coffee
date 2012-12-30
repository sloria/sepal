alert 'hello world'

comp = (Math.sqrt(i) for i in [0..10])

square = (x) -> x * x

anotherComp = (square(x) for i in [0..10] by 2)
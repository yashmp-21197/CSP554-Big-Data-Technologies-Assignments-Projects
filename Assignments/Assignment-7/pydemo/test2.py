lines=sc.textFile('/user/hadoop/cs595doc2.txt')
upper=lines.map(lambda line: line.upper())
words= lines.flatMap(lambda line: line.split(" "))


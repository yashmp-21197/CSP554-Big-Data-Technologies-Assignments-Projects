from mrjob.job import MRJob

class MRRating(MRJob):

    def mapper(self, _, line):
        (user_id,movie_id,rating,timestamp) = line.split(',')
        yield user_id, 1

    def combiner(self, user_id, counts):
        yield user_id, sum(counts)

    def reducer(self, user_id, counts):
        yield user_id, sum(counts)

if __name__ == '__main__':
    MRRating.run()

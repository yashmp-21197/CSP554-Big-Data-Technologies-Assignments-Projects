from mrjob.job import MRJob

class MRSalaries2(MRJob):

    def mapper(self, _, line):
        (name,jobTitle,agencyID,agency,hireDate,annualSalary,grossPay) = line.split('\t')
        if float(annualSalary) >= 100000.00:
            yield 'High', 1
        elif float(annualSalary) >= 50000.00 and float(annualSalary) <= 99999.99:
            yield 'Medium', 1
        elif float(annualSalary) >= 0.00 and float(annualSalary) <= 49999.99:
            yield 'Low', 1

    def combiner(self, annualSalary, counts):
        yield annualSalary, sum(counts)

    def reducer(self, annualSalary, counts):
        yield annualSalary, sum(counts)

if __name__ == '__main__':
    MRSalaries2.run()

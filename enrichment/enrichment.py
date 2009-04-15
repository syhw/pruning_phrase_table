
import enrichment_

# Calculate the probability of getting b successes in a sample of n distinct
# objects drawn without replacement from a population of N objects with B
# successes. Return the left, right and two-tailed p-values.
#
# Adapted from WordHoard project - http://wordhoard.northwestern.edu
# (edu.northwestern.at.utils.math.statistics.FishersExactTest)
def fisher_exact_test (b, n, B, N):
	assert (b <= n) and (n <= N) and (B <= N) and (b <= B)
	um, lm = min(n, B), max(0, n + B - N)

	if (um == lm):
		return 1.0, 1.0, 1.0

	cutoff = enrichment_.hypergeometric_distribution(b, n, B, N)
	left_tail, right_tail, two_tailed = 0, 0, 0

	for i in range(lm, um + 1):
		p = enrichment_.hypergeometric_distribution(i, n, B, N)

		if (i <= b):
			left_tail += p

		if (i >= b):
			right_tail += p

		if (p <= cutoff):
			two_tailed += p

	left_tail = min(left_tail, 1)
	right_tail = min(right_tail, 1)
	two_tailed = min(two_tailed, 1)

	return left_tail, right_tail, two_tailed

# Enrichment for the attribute in the query
# (< 1 if the query is depleted)
def enrichment (b, n, B, N):
	return (float(b) / n) / (float(B) / N)

def contingency_table (b, n, B, N):
	print "  %5s (b)    %5s      | %5s (n)" % (b, n - b, n)
	print "  %5s        %5s      | %5s" % (B - b, N - B - n + b, N - n)
	print "  ------------------------+-------"
	print "  %5s (B)    %5s      | %5s (N)" % (B, N - B, N)
	print
	print "         Enrichment: %.6f" % enrichment(b, n, B, N)

	left, right, two_tailed = fisher_exact_test(b, n, B, N)

	print "       Left p-value: %.6g" % left
	print "      Right p-value: %.6g" % right
	print " Two-tailed p-value: %.6g" % two_tailed

"""
TEST = (
  (1, 500, 120, 1800),
  (10, 10, 20, 100),
  (1, 5, 8, 15),
  (2, 9, 10, 19),
  (2, 12, 52, 962),
  (79, 268, 195, 195+3723),
 )

for (b, n, B, N) in TEST:
	print ':' * 80
	contingency_table(b, n, B, N)
"""
